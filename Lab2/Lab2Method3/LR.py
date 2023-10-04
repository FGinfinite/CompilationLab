siganl,state = 0, 0 # 移进规约压入栈的符号，以及转移到的状态
tstack = [0] * 5000 # 栈
top = -1 # 栈顶元素下标
buffer = [''] * 5000 # 输入缓冲区
number = [0] * 5000 # 将输入字符串转化为编码
pos = 0 # number数组下标
X = 0 # 当前获取到的输入符号的编码
flag = 1 # 循环标志

class Gra:
    def __init__(self, left, right, len):
        self.left = left # 产生式左侧非终结符的编码
        self.right = right # 产生式右侧的编码串
        self.len = len # 产生式右侧的长度

pro = [
    Gra(0, [], 0),
    Gra(101, [0, 102], 1), # S -> E
    Gra(102, [0, 102, 3, 103], 3), # E -> E+T
    Gra(102, [0, 102, 4, 103], 3), # E -> E-T
    Gra(102, [0, 103], 1), # E -> T
    Gra(103, [0, 103, 5, 104], 3), # T -> T*F
    Gra(103, [0, 103, 6, 104], 3), # T -> T/F
    Gra(103, [0, 104], 1), # T -> F
    Gra(104, [0, 1, 101, 2], 3), # F -> (E)
    Gra(104, [0, 7], 1), # F -> num
]

GOTO = [
    # LR分析表goto
    # 多构造一列为了下标从1开始 SETF
    [0, 0, 1, 2, 3], # 0
    [0, 0, 0, 0, 0], # 1
    [0, 0, 0, 0, 0], # 2
    [0, 0, 0, 0, 0], # 3
    [0, 0, 10, 2, 3], # 4
    [0, 0, 0, 0, 0], # 5
    [0, 0, 0, 11, 3], # 6
    [0, 0, 0, 12, 3], # 7
    [0, 0, 0, 0, 13], # 8
    [0, 0, 0, 0, 14], # 9
    [0, 0, 0, 0, 0], # 10
    [0, 0, 0, 0, 0], # 11
    [0, 0, 0, 0, 0], # 12
    [0, 0, 0, 0, 0], # 13
    [0, 0, 0, 0, 0], # 14
    [0, 0, 0, 0, 0], # 15
]

ACTION = [
    # LR分析表action
    # acc为999
    # 51期待(或运算对象首字符，但出现运算符或者$
    # 52括号不匹配，删掉右括号
    # 53期待运算符号，但出现(或运算对象
    # S为正数，R为负数
    # $()+-*/num 01234567
    [51, 4, 52, 51, 51, 51, 51, 5], # 0
    [999, 53, 52, 6, 7, 0, 0, 53], # 1
    [-4, 53, -4, -4, -4, 8, 9, 53], # 2
    [-7, 0, -7, -7, -7, -7, -7, 0], # 3
    [0, 4, 52, 51, 51, 51, 51, 5], # 4
    [-9, 0, -9, -9, -9, -9, -9, 0], # 5
    [51, 4, 52, 51, 51, 51, 51, 5], # 6
    [51, 4, 52, 51, 51, 51, 51, 5], # 7
    [51, 4, 52, 51, 51, 51, 51, 5], # 8
    [51, 4, 52, 51, 51, 51, 51, 5], # 9
    [0, 53, 15, 6, 7, 0, 0, 53], # 10
    [-2, 53, -2, -2, -2, 8, 9, 53], # 11
    [-3, 53, -3, -3, -3, 8, 9, 53], # 12
    [-5, 0, -5, -5, -5, -5, -5, 0], # 13
    [-6, 0, -6, -6, -6, -6, -6, 0], # 14
    [-8, 0, -8, -8, -8, -8, -8, 0], # 15
]

def transform():
    # 将读入缓冲区的字符数组转换为相应的编码
    # 把读入的字符串转化为编码存在number这个编码数组
    i, j = 0, 0 # i为buffer下标，j为number下标
    while buffer[i] != '$':
        if 48 <= ord(buffer[i]) <= 57:
            # 当前字符为数字，num
            while 48 <= ord(buffer[i]) <= 57:
                i += 1
            number[j] = 7
            j += 1
        else:
            case = buffer[i]
            i += 1
            if case == '&':
                number[j] = 0
            elif case == '(':
                number[j] = 1
            elif case == ')':
                number[j] = 2
            elif case == '+':
                number[j] = 3
            elif case == '-':
                number[j] = 4
            elif case == '*':
                number[j] = 5
            elif case == '/':
                number[j] = 6
            j += 1
    number[j] = 0

def get_number():
    # 获取当前输入符号串的元素
    global X, pos
    X = number[pos]
    pos += 1

def push(A, s):
    # 符号、状态入栈
    global top
    top += 1
    tstack[top] = A # 符号A入栈
    top += 1
    tstack[top] = s # 状态S入栈

def pop():
    # 出栈
    global top
    top -= 2

def shift():
    # 移进
    global X, top
    temp = ACTION[tstack[top]][X] # 查找表，确定需要移入的状态
    push(X, temp) # 当前读入字符与状态入栈
    print(f"S{temp}\t移进.")

def reduce():
    # 规约
    global X, top, pos
    x = -ACTION[tstack[top]][X]
    print(f"R{x}\t规约\t", end="")
    case = pro[x].left
    if case == 101:
        print("S -> ", end="")
    elif case == 102:
        print("E -> ", end="")
    elif case == 103:
        print("T -> ", end="")
    elif case == 104:
        print("F -> ", end="")
    for i in range(1, pro[x].len+1):
        pop() # 将栈中元素，按照产生式右边的长度依次弹出
        case = pro[x].right[i]
        if case == 0:
            print("$", end="")
        elif case == 1:
            print("(", end="")
        elif case == 2:
            print(")", end="")
        elif case == 3:
            print("+", end="")
        elif case == 4:
            print("-", end="")
        elif case == 5:
            print("*", end="")
        elif case == 6:
            print("/", end="")
        elif case == 7:
            print("num", end="")
        elif case == 101:
            print("S", end="")
        elif case == 102:
            print("E", end="")
        elif case == 103:
            print("T", end="")
        elif case == 104:
            print("F", end="")
    print()
    y = GOTO[tstack[top]][pro[x].left-100]
    push(pro[x].left, y)
    # 将规约产生式的左部压入栈，并将转移状态也压栈

def acc():
    # accept
    global flag
    flag = 0 # 不再循环
    print("ACC!")

def err1():
    # 期待(或运算对象首字符，但出现运算符或者$
    print("error1\t\t\t缺少运算符，将num入栈.")
    push(7, 5)

def err2():
    # 括号不匹配，删掉右括号 
    print("error2\t\t\t括号不匹配，请删除右括号.")

def err3():
    pointer = pos
    case = tstack[top]
    if case == 1:
        push(3, 6)
        print("error3\t\t\t缺少操作符，请添加操作符到栈里.")
    elif case in [2, 12, 13]:
        push(5, 8)
        print("error3\t\t\t缺少操作符，请添加操作符到栈里.")
    elif case == 11:
        if 3 <= number[pointer] <= 6:
            # 期待运算符
            push(2, 15)
            print("e3\t\t\t缺少右括号，请添加右括号到栈.")
        elif number[pointer] == 7:
            push(3, 6)
            print("error3\t\t\t缺少操作符，请添加操作符到栈里.")


print("请输入一个待分析串，以$结束")
buffer = input()

#ForTEST
#buffer = "8*(8-6)/4$"
#ForTEST

transform() #将字符转化为编码
push(0, 0) #状态S0入栈
get_number() #从已经变成编码的buffer读取一个字符
while flag:
    if ACTION[tstack[top]][X] > 0 and ACTION[tstack[top]][X] < 50:
        #进行移进操作
        shift()
        get_number()
    elif ACTION[tstack[top]][X] < 0:
        #进行规约操作
        reduce()
    elif ACTION[tstack[top]][X] == 999:
        #accept
        acc()
    else:
        case = ACTION[tstack[top]][X]
        if case == 51:
            err1()
        elif case == 52:
            err2()
            get_number()
        elif case == 53:
            err3()
            get_number()
#system("pause")