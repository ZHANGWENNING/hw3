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


def evaluateMulDiv(tokens,index):
    answer=1
    tokens.insert(index, {'type': 'MULTIPLE'})
    index += 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index-1]['type'] == 'MULTIPLE':
                answer *= tokens[index]['number']
            elif tokens[index-1]['type'] == 'DIVIDE':
                answer /= tokens[index]['number']
            else:
                index -=2
                return answer,index
        index += 2
    return answer,index

def evaluatePlusMinus(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens.insert(len(tokens)+1, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens.insert(len(tokens)+2, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER' :
            if tokens[index - 1]['type'] == 'PLUS':
                if tokens[index + 1]['type'] == 'PLUS' or tokens[index + 1]['type'] == 'MINUS':
                    answer += tokens[index]['number']
                else:
                    answer2,index=evaluateMulDiv(tokens,index)
                    answer+=answer2
                    index +=1
            elif tokens[index - 1]['type'] == 'MINUS':
                if tokens[index + 1]['type'] == 'PLUS' or tokens[index + 1]['type'] == 'MINUS':
                    answer -= tokens[index]['number']
                else:
                    answer2,index=evaluateMulDiv(tokens,index)
                    answer-=answer2
                    index += 1
            else:
                print 'Invalid syntax'
        index += 1
    return answer
def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluatePlusMinus(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("1.1*2.1+3", 5.31)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluatePlusMinus(tokens)
    print answer
    print "answer = %f\n" % answer