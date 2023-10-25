# 适合本文法的词法分析器
# E→E+T|E-T|T
# T→T*F|T/F|F
# F→(E)| num

import re


def tokenize(input_string: str) -> list[tuple[str, str]]:  # 词法分析器
    # 定义词法单元的正则表达式模式
    patterns = [
        ('n', r'\d+'),  # 匹配数字
        ('i', r'[a-zA-Z]'),  # 匹配标识符
        ('+', r'\+'),  # 匹配加号
        ('-', r'-'),  # 匹配减号
        ('*', r'\*'),  # 匹配乘号
        ('/', r'/'),  # 匹配除号
        ('(', r'\('),  # 匹配左括号
        (')', r'\)')  # 匹配右括号
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
    input_tokens = "(a(b(2))(c))"
    tokens = tokenize(input_tokens)
    print(tokens)
