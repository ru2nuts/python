# ASW Lambda implementation. Requires:
#  - MySQL DB (accessible from this lambda),
#  - API Gateway,
#  - Lambda (triggered by API Gateway),
#  - SES Role for emailing,
#  - Weather Underground API key.
#
# Lambda environment variables are used for DB credentials, WU API key, etc.
#
# Invokation:
#   curl -H 'Content-Type: application/json' -X PUT \
#   -d '{"email":"zzz@example.com","zip_code":"96795"}' \
#   https://zzz.execute-api.us-east-1.amazonaws.com/prod/lambda_name
#
#   curl -H 'Content-Type: application/json' -X GET https://zzz.execute-api.us-east-1.amazonaws.com/prod/lambda_name
#

import boto3
import json
import os
import urllib2
import pymysql
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses = boto3.client('ses')


EMAIL_FROM = os.environ['email_from']
EMAIL_SUBJECTS_BY_TYPE = {'good': 'It''s nice out! Enjoy a discount on us.', 'bad':'Not so nice out? That''s okay, enjoy a discount on us.', 'neutral': 'Enjoy a discount on us.'}
WU_API_KEY = os.environ['wu_api_key']
DB_HOST = os.environ['db_host']
DB_NAME = os.environ['db_name']
DB_LOGIN = os.environ['db_login']
DB_PASSWORD = os.environ['db_password']
DB_PORT = 3306


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    operations = ['GET', 'PUT']
    operation = event['httpMethod']
    if operation == 'PUT':
        logger.info('method=PUT')
        parsed_json = json.loads(event['body'])
        email = parsed_json['email']
        zip_code = parsed_json['zip_code']
        #save to DB
        insert_data(make_conn(), email, zip_code)
        return respond(None, 'Email added: ' + email + ', zip code: ' + zip_code)
    elif operation == 'GET':
        logger.info('method=GET')
        #retrieve all records from DB, make WU calls, sent out emails
        fetch_data_and_email(make_conn())
        return respond(None, 'emails sent')
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))


def send_emails(email_to, subject_key, location, temp, cond):
    response = ses.send_email(
        Source = EMAIL_FROM,
        Destination={
            'ToAddresses': [
                email_to,
            ]
        },
        Message={
            'Subject': {
                'Data': EMAIL_SUBJECTS_BY_TYPE[subject_key]
            },
            'Body': {
                'Text': {
                    'Data': "%s,\n%d degrees,\n%s" % (location, temp, cond)
                }
            }
        }
    )


def call_wu_api(zip_code):
    wu_url = "http://api.wunderground.com/api/%s/conditions/q/%s.json" % (WU_API_KEY, zip_code)
    logger.info(wu_url)
    f = urllib2.urlopen(wu_url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['current_observation']['display_location']['full']
    temp_f = float(parsed_json['current_observation']['temp_f'])
    weather_descr = parsed_json['current_observation']['weather']
    precip_1hr_in = float(parsed_json['current_observation']['precip_1hr_metric'])
    f.close()

    wu_url = "http://api.wunderground.com/api/%s/almanac/q/%s.json" % (WU_API_KEY, zip_code)
    logger.info(wu_url)
    f = urllib2.urlopen(wu_url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    temp_f_hi = float(parsed_json['almanac']['temp_high']['normal']['F'])
    temp_f_low = float(parsed_json['almanac']['temp_low']['normal']['F'])
    f.close()

    weather_type = convert_weather_descr_and_tempr_to_type(weather_descr, temp_f, temp_f_hi, temp_f_low, precip_1hr_in)
    logger.info("Current temperature in %s is: %s, weather conditions: %s" % (location, temp_f, weather_descr))
    logger.info("Normal high is %s, and normal low is: %s" % (temp_f_hi, temp_f_low))
    return (weather_type, location, temp_f, weather_descr)


def make_conn():
    conn = None
    try:
        conn = pymysql.connect(DB_HOST, user=DB_LOGIN, passwd=DB_PASSWORD, db=DB_NAME, connect_timeout=5)
    except:
        logger.error("Failed connecting to MySql instance.")
        sys.exit()
    return conn


def insert_data(conn, email, zip_code):
    with conn.cursor() as cur:
        cur.execute('insert into kw_emails_zips (email, zip_code) values(%s, %s)', [email, zip_code])
        conn.commit()
        logger.info('email: %s, zip_code: %s' % (email, zip_code)


def fetch_data_and_email(conn):
    item_count = 0
    with conn.cursor() as cur:
        cur.execute("select email, zip_code from kw_emails_zips")
        for row in cur:
            item_count += 1
            logger.info(row)
            logger.info('email: ' + row[0])
            logger.info('zip code: ' + row[1])
            (weather_type, location, temp_f, condition) = call_wu_api(row[1])
            logger.info("weather type: %s" % weather_type)
            send_emails(row[0], weather_type, location, temp_f, condition)
        logger.info('Emailed messages: %d' % (item_count))


def convert_weather_descr_and_tempr_to_type(weather_descr, current_temp, avg_temp_hi, avg_temp_low, precipitation):
    if precipitation < 0.01 and (current_temp > (avg_temp_hi + 5) or ('Sunny' in weather_descr) or ('Clear' in weather_descr)):
        return 'good'
    elif precipitation > 0.01 or current_temp < (avg_temp_low - 5) or ('Rain' in weather_descr) or ('Snow' in weather_descr) or ('Sleet' in weather_descr) or ('Thunder' in weather_descr):
        return 'bad'
    else:
        return 'neutral'
