#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index]) # 二桁以上にも対応
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal # 小数点にも対応
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_int(num):
    line = str(num)
    number = index = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index]) # 二桁以上にも対応
        index += 1
    return  number

def read_round(num):
    if num - read_int(num) >= 0.5:
         num = read_int(num) + 1
    else:
         num = read_int(num) 
    return  num

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mul(line, index):
    token = {'type':'MUL'}
    return token, index + 1

def read_div(line, index):
    token = {'type':'DIV'}
    return token, index + 1

def read_lparen(line, index):
    token = {'type':'LPAREN'}
    return token, index + 1

def read_rparen(line, index):
    token = {'type':'RPAREN'}
    return token, index + 1

def read_abs(line, index):
    if line[index + 1] == "b" and line[index + 2] == "s" :
        token = {'type':'ABS'}
    return token, index + 3

def read_int(line, index):
    if line[index + 1] == "n" and line[index + 2] == "t" :
        token = {'type':'INT'}
    return token, index + 3

def read_round(line, index):
    if line[index + 1] == "o" and line[index + 2] == "u" and line[index + 3] == "n" and line[index + 4] == "d":
        token = {'type':'ROUND'}
        print("Ifound ROUND")
    return token, index + 5


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index) # 二桁以上だったり小数の時も数値の塊として出してくれる
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mul(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        elif line[index] == '(':
            (token, index) = read_lparen(line, index)
        elif line[index] == ')':
            (token, index) = read_rparen(line, index)
        elif line[index] == 'a':
            (token, index) = read_abs(line, index)
        elif line[index] == 'i':
            (token, index) = read_int(line, index)
        elif line[index] == 'r':
            (token, index) = read_round(line, index)
        elif line[index] == ' ':
             index += 1
             continue
        else:
            print('Invalid character found: ' + line[index])
            exit(1) # プログラム終了
        tokens.append(token)
    return tokens


    # example : 40 + 20 * 9
    # tokens = [{'type': 'NUMBER', 'number': 40}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 20}, {'type':'MUL'}, {'type': 'NUMBER', 'number': 9}]

def evaluate(tokens,left,right):
    # 掛け算と割り算を計算
    index = left
    while index < right:
        if tokens[index]['type'] == "ABS" or tokens[index]['type'] == "INT" or tokens[index]['type'] == "ROUND":
             index += 1
        if tokens[index]['type'] == "LPAREN":
             stack = []
             stack.append(1)
             index += 1
             while index < right:
                  if tokens[index]['type'] == "RPAREN":
                       stack.pop()
                       if not stack:
                            break
                  elif tokens[index]['type'] == "LPAREN":
                       stack.append(1)     
                  index += 1
                  print(f"NOW : {index}")
        elif tokens[index]['type'] =='MUL' or tokens[index]['type'] =="DIV":
            ans = eval_mul_div(tokens,index,tokens[index]['type'])
            print(ans)
            tokens[index + 1]["number"] = ans
            print(f"mul or div : {tokens[index + 1]["number"]}")
            # print(index + 1)
            if tokens[index - 1]["type"] == "NUMBER":
                tokens[index - 1]["type"] = None
            elif tokens[index - 1]["type"] == "RPAREN":
                tokens[index - 1]["number"] = 0
            if tokens[index + 1]["type"] == "LPAREN":
                stack = []
                stack.append(1)
                index += 2
                while index < right:
                    if tokens[index]['type'] == "RPAREN":
                        stack.pop()
                        if not stack:
                                break
                    elif tokens[index]['type'] == "LPAREN":
                        stack.append(1)     
                    index += 1
                tokens[index]["number"] = ans
                print(f"index:{index}")
            index += 1
        index += 1

    # 足し算と引き算を計算
    is_plus = True    
    answer = 0
    index = left
    # print(f"first is_plus : {is_plus}")
    while index < right:
        if tokens[index]['type'] == "LPAREN":
             stack = []
             stack.append(1)
             index += 1
             while index < right:
                  if tokens[index]['type'] == "RPAREN":
                       stack.pop()
                       if not stack:
                            print("ready to break")
                            break
                  elif tokens[index]['type'] == "LPAREN":
                       stack.append(1) 
                  print(f" i anm {index}")    
                  index += 1
        if tokens[index]['type'] == 'NUMBER':
            num = tokens[index]['number']
            # print(f"NUM {num}")
            # print(f"is_plus : {is_plus}")
            answer = eval_add_sub(answer,is_plus,num) 
            print(f"add or sub ans : {answer}")
            # print(answer)   
            tokens[index]["type"] = None   
        elif tokens[index]['type'] == 'RPAREN':
            num = tokens[index]['number']
            # print(f"NUM {num}")
            # print(f"is_plus : {is_plus}")
            answer = eval_add_sub(answer,is_plus,num) 
             
        elif tokens[index]['type'] == "PLUS":
             is_plus = True
        elif tokens[index]['type'] == "MINUS":
             is_plus = False
            #  print("MINUS")
        #else:
            #  print("ELSE")
        index += 1
    return answer

def eval_add_sub(answer,is_plus,num):
    if is_plus:
         answer += num
    else:
         answer -= num
    return answer

def eval_mul_div(tokens,index,type):
    if type =='MUL':
                    mul_div_answer = tokens[index - 1]['number'] * tokens[index + 1]['number']
    elif type =='DIV':
                    mul_div_answer = tokens[index - 1]['number'] / tokens[index + 1]['number']
    return mul_div_answer

def test(line):
    tokens = tokenize(line)
    index = 0
    stack = []
    abs_dic = int_dic = round_dic = set()
    while index < len(tokens):
        if tokens[index]['type'] =='LPAREN':
            stack.append(index)
            if tokens[index-1]['type'] =='ABS':
                abs_dic.add(index)
            elif tokens[index-1]['type'] =='INT':
                 int_dic.add(index)
            elif tokens[index-1]['type'] =='ROUND':
                 round_dic.add(index)
            print(f"Lparent: {index}")
        elif tokens[index]['type'] =='RPAREN':
            subleft = stack.pop()
            if 'number' in tokens[index]:
              continue
            tokens[index]['number'] = tokens[subleft]['number'] = evaluate(tokens,subleft+1,index)
            if subleft in abs_dic:
                tokens[index]['number'] = tokens[subleft]['number'] =  max(tokens[index]['number'],-tokens[index]['number'])
            elif subleft in int_dic:
                tokens[index]['number'] = tokens[subleft]['number'] =  read_int(tokens[index]['number'])
            elif subleft in round_dic:
                tokens[index]['number'] = tokens[subleft]['number'] =  read_round(tokens[index]['number'])
                print("i am rounding")
            print(f"subleft : {subleft} , index : {index} ")
            print(f"recursion point : {tokens[index]['number']}")
            print(index)
        index += 1
    
    actual_answer = evaluate(tokens,0,len(tokens)) #　実装した計算
    expected_answer = eval(line) # pythonの組み込み関数による計算
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    # test("1+2")
    # test("405.9 + 0.10")
    # test("1.0+2.1-3")
    # test("2*3")
    # test("-2*3")
    # test("1.0 + 2*2")
    # test("1.0 + 2 * 2.0 * 4.0")
    # test("1/2")
    # test("-1/2")
    # test("1.0/2")
    # test("1 + 3/4")
    # test("1 - 9.0/3")
    # test("-1 - 9.0/3")
    # test("1 + 1/8 - 6*2")
    # test("1/9*3")
    # test("1.0/9.0*3.0")
    # test("1/9*5 + 4.0 - 2")
    # test("1/9*5 * 9.8 + 4.0 /9 - 2 * 8")
    #test("(1-3)")
    # test("(3.0 + 4 * 2) / 5")
    # test("(3.0 + 4 * 2) / 5 -2")
    # test("4 * (8+9)")
    test("(3.0 + 4 * 2) * 3 / 5")
    test("((3.0 + 4 * 2) / 5 + 1) * 2")
    test("((4) + 1)")
    test("((((8))))")
    test("(3.0 + 4 * 2) / 5")
    test("((2 + (5 + 9) / 14))*6 + 3")
    # test("round(9.8)")

    print("==== Test finished! ====\n")

run_test()



# 宿題１:「*」「/」に対応しよう
# 宿題２：テストケースを網羅的に作る
# 宿題３：()に対応する、テストケースも追加
# 宿題４：abs(), int(), round() に対応する、テストケースも追加


# while True:
#     print('> ', end="")
#     line = input() # rtype : str
#     tokens = tokenize(line) # rtype : list[dic]
#     answer = evaluate(tokens) # rtype : float
#     print("answer = %f\n" % answer)
