# 递归下降语法分析器


from LexicalAnalysis import tokenize


# 语法分析函数
def parse_expression(tokens):
    print("分析产生式E→E+T|E-T|T")
    # E→E+T|E-T|T
    left_operand = parse_term(tokens)
    while tokens and (tokens[0][0] == '+' or tokens[0][0] == '-'):
        operator = tokens.pop(0)
        right_operand = parse_term(tokens)
        left_operand = (operator[1], left_operand, right_operand)
    return left_operand


def parse_term(tokens):
    print("分析产生式T→T*F|T/F|F")
    # T→T*F|T/F|F
    left_operand = parse_factor(tokens)
    while tokens and (tokens[0][0] == '*' or tokens[0][0] == '/'):
        operator = tokens.pop(0)
        right_operand = parse_factor(tokens)
        left_operand = (operator[1], left_operand, right_operand)
    return left_operand


def parse_factor(tokens):
    print("分析产生式F→(E)|num")
    # F→(E)|num
    if tokens[0][0] == '(':
        tokens.pop(0)  # 消耗左括号
        expression = parse_expression(tokens)
        if tokens[0][0] == ')':
            tokens.pop(0)  # 消耗右括号
            return expression
        else:
            raise ValueError("缺少右括号")
    elif tokens[0][0] == 'i':
        return int(tokens.pop(0)[1])
    else:
        raise ValueError(f"无法识别的字符: {tokens[0][1]}")


# 输入样例
if __name__ == "__main__":
    input_tokens = "1+(2*(2/3))-100"
    tokens = tokenize(input_tokens)
    parsed_expression = parse_expression(tokens)
    print(parsed_expression)
