# 要求所分析算数表达式由如下的文法产生。
# E→E+T|E-T|T
# T→T*F|T/F|F
# F→(E)| num
# 其中，E表示表达式，T表示项，F表示因子，num表示数字。
# 输入样例：1+(2*(2/3))-100

# 编写递归调用程序实现自顶向下的分析。

from LexicalAnalysis import tokenize


# 语法分析函数
def parse_expression(tokens):
    # E→E+T|E-T|T
    left_operand = parse_term(tokens)
    while tokens and (tokens[0][0] == 'ADD' or tokens[0][0] == 'SUB'):
        operator = tokens.pop(0)
        right_operand = parse_term(tokens)
        left_operand = (operator[1], left_operand, right_operand)
    return left_operand


def parse_term(tokens):
    # T→T*F|T/F|F
    left_operand = parse_factor(tokens)
    while tokens and (tokens[0][0] == 'MUL' or tokens[0][0] == 'DIV'):
        operator = tokens.pop(0)
        right_operand = parse_factor(tokens)
        left_operand = (operator[1], left_operand, right_operand)
    return left_operand


def parse_factor(tokens):
    # F→(E)|num
    if tokens[0][0] == 'LPAREN':
        tokens.pop(0)  # 消耗左括号
        expression = parse_expression(tokens)
        if tokens[0][0] == 'RPAREN':
            tokens.pop(0)  # 消耗右括号
            return expression
        else:
            raise ValueError("缺少右括号")
    elif tokens[0][0] == 'NUM':
        return int(tokens.pop(0)[1])
    else:
        raise ValueError(f"无法识别的字符: {tokens[0][1]}")

# 输入样例
if __name__ == "__main__":
    input_string = "1+(2*(2/3))-100"
    tokens = tokenize(input_string)
    parsed_expression = parse_expression(tokens)
    print(parsed_expression)
