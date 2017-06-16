def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def readLeftBra(line, index):
    token = {'type': 'LEFT'}
    return token, index + 1

def readRightBra(line, index):
    token = {'type': 'RIGHT'}
    return token, index + 1

def readMultipule(line, index):
    token = {'type': 'MULTIPLE'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '(':
            (token, index) = readLeftBra(line, index)
        elif line[index] == ')':
            (token, index) = readRightBra(line, index)
        elif line[index] == '*':
            (token, index) = readMultipule(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

def evaluateBracker(tokens,index):
    #print "a"
    if tokens[index]['type'] == 'LEFT' :
        index += 1
        answer,index=evaluatePlusMinus(tokens,index)
        #????
        index += 1
        return answer,index
    elif tokens[index]['type'] == 'NUMBER':
        answer=tokens[index]['number']
        index += 1
        return answer,index
    else:
        index += 1
        return answer,index
    #print "index=%d" %index
    #print "answer=%d" %answer
    return answer,index

def evaluateMulDiv(tokens,index):
    #print "aa"
    answer,index=evaluateBracker(tokens,index)
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLE':
            index += 1
            result,index = evaluateBracker(tokens,index)
            answer *= result
        elif tokens[index]['type'] == 'DIVIDE':
            index += 1
            result,index = evaluateBracker(tokens,index)
            answer /= result
        else:
            #print "index=%d" %index
            #print "answer=%d" %answer
            return answer,index
    #print "index=%d" %index
    #print "answer=%d" %answer
    return answer,index

def evaluatePlusMinus(tokens,index):
    #print "aaa"
    answer,index=evaluateMulDiv(tokens,index)
    while index < len(tokens):
        if tokens[index ]['type'] == 'PLUS':
            index += 1
            result,index=evaluateMulDiv(tokens,index)
            answer += result
        elif tokens[index ]['type'] == 'MINUS':
            index += 1
            result,index=evaluateMulDiv(tokens,index)
            answer -= result
        else:
            #print "index=%d" %index
            #print "answer=%d" %answer
            return answer,index
    #print "index=%d" %index
    #print "answer=%d" %answer
    return answer,index

def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluatePlusMinus(tokens,0)[0]
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("2*4*5", 40)
    test("2*4*5*0.5", 20)
    test("2*4/2", 4)
    test("2*(1+1)", 4)
    test("2*(1+1)*3", 12)
    test("2*(1+2*(1+1))", 10)
    test("(1+2*(1+1))*2", 10)
    print "==== Test finished! ====\n"

runTest()
while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluatePlusMinus(tokens,0)[0]
    print answer
    print "answer = %f\n" % answer