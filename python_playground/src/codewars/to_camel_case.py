def to_camel_case(text):
    import re
    ss = re.split(r'[_,-]', text)
    print(len(ss))
    print(ss[0])
    print(ss[1:])
    return ss[0] + "".join([s[0].capitalize() + s[1:] if len(s) > 0 else "" for s in ss][1:])


print(to_camel_case(""))
