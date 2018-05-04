

def openOrSenior(data):
    # Hmmm.. Where to start?
    return ["Senior" if (c[0] >= 55 and c[1] > 7) else "Open" for c in data]





assert openOrSenior([[45, 12],[55,21],[19, -2],[104, 20]]) == ['Open', 'Senior', 'Open', 'Senior']
assert openOrSenior([[16, 23],[73,1],[56, 20],[1, -1]]) == ['Open', 'Open', 'Senior', 'Open']
assert openOrSenior([[16, 23],[73,1],[56, 20],[55, 8]]) == ['Open', 'Open', 'Senior', 'Senior']