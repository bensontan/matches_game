marks = {True: '*', False: ''}

ops = {'+': [1], '-': []}

# assign a line a different number (2-8), and then a digit associate with a set of them.
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

# define each line has different id (multiple by 10 for easier to understand)
for pos in xrange(4):
    digits[pos] = {}
    for symbol in symbols.keys():
        if symbol == ' ' and pos < 2:
            continue
            
        digits[pos][symbol] = [pos * 10 + line for line in symbols[symbol]]

# Loop thru to find all valid and invalid statements, such as, '7+0= 7'
for op in ops:
    for d1 in digits[0].keys():
        for d2 in digits[1].keys():
            for d3 in digits[2].keys():
                for d4 in digits[3].keys():
                    if d3 == 0 and d4 not in [1, ' ']: # leading with 0
                        continue
                    # this is because we want to find the question, like '6+0=61'
                    if d3 == ' ' or d4 == ' ':
                        if d3 == ' ' and d4 == ' ':
                            continue
                        elif d3 == ' ':
                            result = d4
                        else:
                            result = d3
                    else:
                        result = d3 * 10 + d4

                    # check the statement is equal or not with + or - operation
                    if op == '+':
                        equal = (d1 + d2 == result)
                    else:
                        equal = (d1 - d2 == result)
                
                    statement = str(d1) + op + str(d2) + \
                            '=' + str(d3) + str(d4)

                    # count total lines of the statement
                    lines = set(digits[0][d1] + ops[op] + \
                             digits[1][d2] + \
                             digits[2][d3] + digits[3][d4])
                    totallines = len(lines)

                    # sort by the valid statement first
                    if equal:
                        results[totallines].insert(0, 
                            [statement, lines, equal, [], []])
                    else:
                        results[totallines].append(
                            [statement, lines, equal, [], []])


# besides the minus and equal sign, total of other matches are less than 2
for totallines in xrange(30):
    statsize = len(results[totallines])
    
    # skill if too less statements under it, or no valid statements
    if statsize < 2 or results[totallines][0][2] is False:
        continue

    # found the count of valid statements        
    validsize = 1
    while results[totallines][validsize][2] is True:
        validsize = validsize + 1
        
    # use set difference to find the difference matches under the same total matches (totallines)
    for validindex in xrange(validsize -1):
        for statindex in xrange(validindex + 1, statsize):

            # we use difference instead of symmetric_difference because the totallines is the same            
            diff = results[totallines][validindex][1] - \
                    results[totallines][statindex][1]
            diffindex = len(diff) + 2
            
            # 1 or 2 differences will be kept
            if diffindex > 4 or diffindex == 2:
                continue

            results[totallines][validindex][diffindex].append(statindex)
            results[totallines][statindex][diffindex].append(validindex)

    # assoicate movables and statement to its answer 
    for difference in xrange(3,5):
        plist = []
        for statindex in xrange(statsize):
            statinfo = results[totallines][statindex]
            # skip if no other statement difference from this statement in 1 or 2 moves
            if len(statinfo[difference]) == 0:
                continue
            # plist.append(statinfo[0] + marks[statinfo[2]])

            # multiple answers will be joined and separated by ', '
            quiz[difference-3][statinfo[0]] = ', '.join(
                    [results[totallines][d][0] for d in statinfo[difference]])

while True:
    try:
        # -1 is because array's index starts from 0
        movables = int(raw_input('How many matches can move [1-2] ? ')) - 1 
        statement = raw_input('What is the statement? ')

        if statement in quiz[movables]:
            print(quiz[movables][statement])
    except KeyboardInterrupt:
        break
