
str = ''

def repl(cc):
    l = len(cc)
    return ''.join(['#' if i < l-4 else cc[i] for i in range(0, l)])

print(repl(str))