# 要求所分析算数表达式由如下的文法产生。
# E→E+T|E-T|T
# T→T*F|T/F|F
# F→(E)| num

# 输入样例：1+(2*(2/3))-100
# 输出为元组数组，每个元组的第一个元素为token，第二个元素为token的值。例如样例的输出为：
# [('num', 1), ('+', '+'), ('(', '('),
# ('num', 2), ('*', '*'),
# ('(', '('), ('num', 2),
# ('/', '/'), ('num', 3),
# (')', ')'), (')', ')'),
# ('-', '-'), ('num', 100)]

import re


def tokenize(input_string: str) -> list[tuple[str, str]]:  # 词法分析器
    # 定义词法单元的正则表达式模式
    patterns = [
        ('NUM', r'\d+'),  # 匹配数字
        ('ADD', r'\+'),  # 匹配加号
        ('SUB', r'-'),  # 匹配减号
        ('MUL', r'\*'),  # 匹配乘号
        ('DIV', r'/'),  # 匹配除号
        ('LPAREN', r'\('),  # 匹配左括号
        ('RPAREN', r'\)')  # 匹配右括号
    ]

    tokens = []
    while input_string:
        for pattern_name, pattern in patterns:
            match = re.match(pattern, input_string)
            if match:
                token = (pattern_name, match.group())
                tokens.append(token)
                input_string = input_string[len(match.group()):]
                break
        else:
            raise ValueError(f"无法识别的字符: {input_string[0]}")

    return tokens


if __name__ == "__main__":
    input_string = "1+(2*(2/3))-100"
    tokens = tokenize(input_string)
    print(tokens)
