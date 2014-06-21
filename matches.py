marks = {True: '*', False: ''}

ops = {'+': [1], '-': []}

symbols = {
    0:[2,3,4,6,7,8], 
    1:[4,7], 
    2:[2,4,5,6,8],
    3:[2,4,5,7,8],
    4:[3,4,5,7],
    5:[2,3,5,7,8],
    6:[2,3,5,6,7,8],
    7:[2,4,7],
    8:[2,3,4,5,6,7,8],
    9:[2,3,4,5,7,8],
    ' ':[]}

results = [[] for i in xrange(30)]
digits = {}
quiz = [{},{}]

# define each line has different id (multiple to 10 for easy to understand)
for pos in xrange(4):
    digits[pos] = {}
    for symbol in symbols.keys():
        if symbol == ' ' and pos < 2:
            continue
            
        digits[pos][symbol] = [pos * 10 + line for line in symbols[symbol]]
        
for op in ops:
    for d1 in digits[0].keys():
        for d2 in digits[1].keys():
            for d3 in digits[2].keys():
                if d3 == 0: # leading 0s
                    continue
                for d4 in digits[3].keys():
                    if d3 == ' ' or d4 == ' ':
                        if d3 == ' ' and d4 == ' ':
                            continue
                        elif d3 == ' ':
                            result = d4
                        else:
                            result = d3
                    else:
                        result = d3 * 10 + d4

                    if op == '+':
                        equal = (d1 + d2 == result)
                    else:
                        equal = (d1 - d2 == result)
                
                    statement = str(d1) + op + str(d2) + \
                            '=' + str(d3) + str(d4)

                    lines = set(digits[0][d1] + ops[op] + \
                             digits[1][d2] + \
                             digits[2][d3] + digits[3][d4])
                    totallines = len(lines)

                    if equal:
                        results[totallines].insert(0, 
                            [statement, lines, equal, [], []])
                    else:
                        results[totallines].append(
                            [statement, lines, equal, [], []])

for totallines in xrange(30):
    statsize = len(results[totallines])
    if statsize < 2 or results[totallines][0][2] is False:
        continue
        
    validsize = 1
    while results[totallines][validsize][2] is True:
        validsize = validsize + 1
        
    for validindex in xrange(validsize -1):
        for statindex in xrange(validindex + 1, statsize):
            diff = results[totallines][validindex][1] - \
                    results[totallines][statindex][1]
            diffindex = len(diff) + 2
            if diffindex > 4 or diffindex == 2:
                continue

            results[totallines][validindex][diffindex].append(statindex)
            results[totallines][statindex][diffindex].append(validindex)

    for difference in xrange(3,5):
        plist = []
        for statindex in xrange(statsize):
            statinfo = results[totallines][statindex]
            if len(statinfo[difference]) == 0:
                continue
            plist.append(statinfo[0] + marks[statinfo[2]])

            quiz[difference-3][statinfo[0]] = ', '.join(
                    [results[totallines][d][0] for d in statinfo[difference]])

while True:
    try:
        movable = int(raw_input('moveable? ')) - 1
        statement = raw_input('statement? ')

        if statement in quiz[movable]:
            print(quiz[movable][statement])
    except KeyboardInterrupt:
        break
