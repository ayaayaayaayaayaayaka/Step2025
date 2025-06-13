#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

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
    return token, index + 5

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
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
            exit(1)
        tokens.append(token)
    return tokens

def eval_add_sub(tokens,left,right):
    answer = 0
    index = left
    is_plus = True 
    while index < right and index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if is_plus:
                answer += tokens[index]['number']
            else:
                 answer -= tokens[index]['number']
        elif tokens[index]['type'] == "PLUS":
            is_plus = True
        elif tokens[index]['type'] == "MINUS":
            is_plus = False
        index += 1
    return answer

def eval_mul_div(tokens,left,right):
    index = left
    while index < right  and index < len(tokens):
        if tokens[index]['type'] =='MUL':
            tokens[index + 1]["number"] = tokens[index - 1]['number'] * tokens[index + 1]["number"]
            tokens[index - 1]["type"] = None
        elif tokens[index]['type'] =='DIV':
            if tokens[index + 1]['number'] == 0:
                exit()
            tokens[index + 1]["number"] = tokens[index - 1]['number'] / tokens[index + 1]["number"]
            tokens[index - 1]["type"] = None
        index += 1
    return

def to_abs(num):
    return max(num,-num)

def to_int(num):
    line = str(num)
    number = index = 0
    is_plus = True
    if line[0] == "-":
        is_plus = False
        index += 1
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index]) # 二桁以上にも対応
        index += 1
    return number if is_plus else -1 * number

def to_round(num):
    if num >= 0:
        if num - to_int(num) >= 0.5:
            num = to_int(num) + 1
        else:
            num = to_int(num) 
    else:
        if num - to_int(num) >= 0.5:
            num = to_int(num) 
        else:
            num = to_int(num) - 1
    return  num

def process_num(subleft,left,right,tokens,index,func_set,func,evaluate):
    func_set.remove(subleft)
    num = func(evaluate(tokens,subleft + 1,index))
    tokens = tokens[left:subleft-1] + [{'type':'NUMBER','number':num }] + tokens[index+1:right]
    index = subleft - left - 1
    return tokens,index

def eval_paren(tokens,left,right):
    index = left
    open_left_stack = []
    abs_set = set()
    int_set = set()
    round_set = set()
    while index < right and index < len(tokens):
        if tokens[index]["type"] == "LPAREN":
            open_left_stack.append(index)
            if index-1 >= 0:
                if tokens[index-1]["type"] == "ABS":
                    abs_set.add(index)
                elif tokens[index-1]["type"] == "INT":
                    int_set.add(index)
                elif tokens[index-1]["type"] == "ROUND":
                    round_set.add(index)
        elif tokens[index]["type"] == "RPAREN":
            subleft = open_left_stack.pop()
            if subleft in abs_set:
                tokens,index = process_num(subleft,left,right,tokens,index,abs_set,to_abs,evaluate)
            elif subleft in int_set:
                tokens,index = process_num(subleft,left,right,tokens,index,int_set,to_int,evaluate)
            elif subleft in round_set:
                tokens,index = process_num(subleft,left,right,tokens,index,round_set,to_round,evaluate)
            else:
                num = evaluate(tokens,subleft + 1,index)
                tokens = tokens[left:subleft] + [{'type':'NUMBER','number':num }] + tokens[index+1:right] 
                index = subleft - left
            right = len(tokens)
        index += 1
    return tokens,right

def evaluate(tokens,left,right): # ある式を演算してくれる関数
    tokens,right = eval_paren(tokens,left,right) # カッコ内を先に計算する、カッコ無しの式が返ってくる。abs.int,roundもここでまとめて処理
    eval_mul_div(tokens,left,right) # 割り算掛け算を処理
    ans = eval_add_sub(tokens,left,right) # 最後、足し算引き算をして答えを出してくれる
    return ans

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens,0,len(tokens))
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")

    test("1+2")
    test("405.9 + 0.10")
    test("1.0+2.1-3")
    test("2*3") #掛け算割り算
    test("-2*3")
    test("1.0 + 2*2")
    test("1.0 + 2 * 2.0 * 4.0")
    test("1/2")
    test("-1/2")
    test("1.0/2")
    test("1 + 3/4")
    test("1 - 9.0/3")
    test("-1 - 9.0/3")
    test("1 + 1/8 - 6*2")
    test("1/9*3")
    test("1.0/9.0*3.0")
    test("1/9*5 + 4.0 - 2")
    test("1/9*5 * 9.8 + 4.0 /9 - 2 * 8")
    test("(8)") #ここからカッコ
    test("(-2)")
    test("(1-3)")
    test("(8) + (9)")
    test("(3.0 + 4 * 2) / 5")
    test("(3.0 + 4 * 2) / 5 -2")
    test("4 * (8+9)")
    test("(8 + 9) * 4")
    test("(3.0 + 4 * 2) * 3 / 5")
    test("((8))") # 二重カッコ
    test("(((9)))")
    test("((4) + 1)")
    test("((4)) + ((8))")
    test("((3.0 + 4 * 2) / 5 + 1) * 2")
    test("((2 + (5 + 9) / 14))*6 + 3")
    test("(7 + 9)*(0.5)")                
    test("8 *9 + (9*(9))")
    test("abs(-9)") # ここからabs,int,round
    test("abs(8)")
    test("abs(-11.2)")
    test("int(7.6)")
    test("int(-9.8)")
    test("round(9.8)")
    test("round(-9.8)")
    test("(int(8.2))")
    test("abs(int(-9.8))")
    test("4*abs(round(-9.8))")   
    test("(int(2 + (5 + 9) / 14))*6 + 3")
    test("(abs(-9 + (5 + 9) / 14))*6 + 3")
    test("(int(2 + round(5.2 + 9) / 14))*6 + 3")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
