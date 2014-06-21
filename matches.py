#
# We don't create class or define function as it is for children to solve a problem with computer.
# 因為這是教小朋友用電腦解決問題，所以沒有使用 class, define 以及 # /usr/bin/python 等語法。
#


# This is not used, as it was marked '*' for the valid statement for debug purpose.
# 這原本用來依合法或不合法計算式來標註 '*' 的，是為了顯示到螢幕檢查用。
# marks = {True: '*', False: ''}

# We skip the matches of '-' and '=' signs as they are always on in wahtever statements.
# 這裡我們不去記錄 '-' 和 '=' 在運算式的線，因為不管是＋或－運算的數學式，它們都一直存在。
ops = {'+': [1], '-': []}

# Assign a line with a different number (2-8), and then a digit associate with a set of them.
# 這邊我們定義每個數字或符號所需要顯示不同的線。
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


# 這是準備存放０－２９條線所產生的數學式子用的，當然在６條線以下會是空的。
results = [[] for i in xrange(30)]


# 這是放答案用的，第一個放搬動１個的問題和對應的解答，第二個放搬動２個的問題和對應的解答。
quiz = [{},{}]

# Define each line with different id (multiple by 10 for easier to understand).
# 這是給每個在不同位置的數字裡的線（火柴棒）一個獨自的號碼；為了方便閱讀，我們直接乘１０而不是乘７。
digits = {}
for pos in xrange(4):
    digits[pos] = {}
    for symbol in symbols.keys():
        # 被加數、加數、被減數和減數（前２個數字）都不能是空白
        if symbol == ' ' and pos < 2:
            continue
            
        digits[pos][symbol] = [pos * 10 + line for line in symbols[symbol]]

# Loop thru to find all valid and invalid statements, such as, '7+0= 7'.
# 這裡我們運用電腦的計算能力，把每一個合法或不合法的數學式子都找出來。
for op in ops:
    for d1 in digits[0].keys():
        for d2 in digits[1].keys():
            for d3 in digits[2].keys():
                for d4 in digits[3].keys():
                    # 除非第４個是１（可以把１移走）或是空白，否則第３個數字不能為０，也就是我們不考慮 8-0=08 這種數學運算式。
                    if d3 == 0 and d4 not in [1, ' ']: # leading with 0
                        continue
                    # This is because we want to find the question, like '6+0=61'.
                    # 依照第３和第４個數字是否為空白來決定第３和第４個數字實際所代表的值。
                    if d3 == ' ' or d4 == ' ':
                        if d3 == ' ' and d4 == ' ':
                            continue
                        elif d3 == ' ':
                            result = d4
                        else:
                            result = d3
                    else:
                        result = d3 * 10 + d4

                    # Check the statement is valid or not by specified + or - operation.
                    # 實際做運算來檢查是否是合理的數學式。
                    if op == '+':
                        valid = (d1 + d2 == result)
                    else:
                        valid = (d1 - d2 == result)
                
                    statement = str(d1) + op + str(d2) + \
                            '=' + str(d3) + str(d4)

                    # Count total lines of the statement.
                    # 把所有線都加起來去計算總共的線數（火柴棒數）。
                    lines = set(digits[0][d1] + ops[op] + \
                             digits[1][d2] + \
                             digits[2][d3] + digits[3][d4])
                    totallines = len(lines)

                    # Sort by the valid statement first.
                    # 把合理的式子往前放，不合理的往後放；這是因為等下我們只要找出移動後會是合法數學式的式子。
                    # Here we prepare some place to hold the information of a statement.
                    #   statement: this field is for print
                    #   lines: this field is for compute differences
                    #   valid: for determine necessary statements to check
                    #   []: for store the index of a statement which has 1 difference with the current one
                    #   []: for store the index of a statement which has 2 differences with the current one
                    # 這裡我們先準備好關於這個數學式一些資訊存放的位置：
                    # 　statement: 這是可印出或顯示的數學式
                    # 　lines: 這是數學式所用到的火柴棒的號碼
                    # 　[]: 這個陣列是放與目前數學式只有１根火柴棒不同的數學式
                    # 　[]: 這個陣列是放與目前數學式只有２根火柴棒不同的數學式
                    if valid:
                        results[totallines].insert(0, 
                            [statement, lines, valid, [], []])
                    else:
                        results[totallines].append(
                            [statement, lines, valid, [], []])


# Besides the minus and equal sign, the total of other matches is less than 30.
# 可以移動的火柴棒最多有２９個
for totallines in xrange(30):
    statsize = len(results[totallines])
    
    # Skip if not many statements under it, or all is invalid statements.
    # 如果只有它一個數學式，或是在這個火柴棒數目下沒有一個是合法，都不考慮。例如：8+8=88。
    # （因為前面會把合法的式子放在前面，所以看第一個是不是合法就知道有沒有合法的數學式。）
    if statsize < 2 or results[totallines][0][2] is False:
        continue

    # Find the count of the valid statements.
    # 找出在這個火柴棒數目下，有幾個是合法的數學式。
    validsize = 0
    while results[totallines][validsize+1][2] is True:
        validsize = validsize + 1
        
    for validindex in xrange(validsize):

        # Build both relations with other statements.
        # 跟其他合法或非法的數學式建立關係（移動１根或移動２根）
        for statindex in xrange(validindex + 1, statsize):

            # We use difference instead of symmetric_difference because the totallines is the same.
            # 我們使用「差集」而不是「補集」，因為這裡兩個運算式都有相同的火柴棒數目，所以直接找差集就可以。
            # 即，(火柴棒甲，火柴棒丙）－（火柴棒乙，火柴棒丙）＝（火柴棒甲）--１個，而不需要算出所有不同處
            # (火柴棒甲，火柴棒乙）-- ２個，然後再除以２得到１個。
            diff = results[totallines][validindex][1] - \
                    results[totallines][statindex][1]

            # Skip if not 1 or 2 differences.
            # 如果數學式一樣或是差異超過２個，那就不用考慮，如 '2+2= 4' 和 '2+2=4'
            if len(diff) > 2 or len(diff) == 0:
                continue
            diffindex = len(diff) + 2

            # Create the relations for both.
            # 相互記錄對方的號碼。
            results[totallines][validindex][diffindex].append(statindex)
            results[totallines][statindex][diffindex].append(validindex)

    # Assoicate movables and statement to its answer.
    # 建立答案表，依照可以移動的火柴棒數和目前的數學式，準備好每個答案。
    for difference in xrange(3,5):
        # plist = []
        for statindex in xrange(statsize):
            statinfo = results[totallines][statindex]
            
            # Skip if no other statement difference from this statement in 1 or 2 moves.
            # 如果這個數學式移動幾個火柴棒沒有能成為另一個數學式（合法的）的話，跳過。
            # 例如：9+0=91 有移動２個的答案，卻沒有移動１個的答案。
            if len(statinfo[difference]) == 0:
                continue
            
            # plist shows all statements in specified totalines
            # plist.append(statinfo[0] + marks[statinfo[2]])

            # Multiple answers will be joined and separated by ', '.
            # 因為我們之前放的是號碼不是實際數學式，所以現在要找那個數學式把它們全部組合起來（所有可轉成的合法數學式）。
            quiz[difference-3][statinfo[0]] = ', '.join(
                    [results[totallines][d][0] for d in statinfo[difference]])

# 好了我們到這裡都有了所有可能的問題和它們的答案，所以當我們問它時，直接對照把答案顯示出來就可以了。
while True:
    try:
        # -1 is because an array's index starts from 0
        # 這裡最後有個-1，是因為陣列是從０開始。
        movables = int(raw_input('How many matches can move [1-2] ? ')) - 1 
        statement = raw_input('What is the statement? ')

        # print the result if has the answer
        # 如果有答案直接顯示它。
        if statement in quiz[movables]:
            print(quiz[movables][statement])
    
    # 按^C可以停止程式。
    except KeyboardInterrupt:
        break
    
    # 其他錯誤就重新再問。
    except Exception:
        pass
