# LL(1)语法分析器

from AnalysisTable import construct_analysis_table
from LexicalAnalysis import tokenize

stack = []
start_symbol = ""
input_tokens = []
table = {}


def get_input_tokens(filename: str) -> list[tuple[str, str]]:
    with open(filename, "r", encoding="utf-8") as f:
        strings = f.readlines()
    for string in strings:
        tokens = tokenize(string.strip())
        tokens.append(('$', '$'))
        yield tokens


def init_table():
    global table, start_symbol
    table, start_symbol = construct_analysis_table()


def init_stack():
    global stack, start_symbol
    stack = ['$', start_symbol]


def analysis():
    global stack, input_tokens, table
    input_generator = get_input_tokens("data/input.txt")
    try:
        while True:
            input_tokens = next(input_generator)
            for token in input_tokens:
                print(token[0], end="")
            print()
            init_stack()
            while stack[-1] != '$':
                print("当前栈：", end="")
                for char in stack:
                    print(char, end="")
                print("    ", end="")
                print("当前输入：", end="")
                for token in input_tokens:
                    print(token[0], end="")
                print("    ", end="")
                stack_top = stack.pop()
                tokens_top = input_tokens[0]
                if stack_top == tokens_top[0]:
                    input_tokens.pop(0)
                    print("匹配")
                    continue
                elif (stack_top, tokens_top[0]) in table:
                    production = table[(stack_top, tokens_top[0])]
                    if production == []:
                        print("非法输入")
                        break
                    print("使用产生式：" + str(production[0][0]) + "->" + str(production[0][1]))
                    if production[0][1] == "ε":
                        continue
                    else:
                        for char in reversed(production[0][1]):
                            stack.append(char)
    except StopIteration:
        print("分析结束")


if __name__ == "__main__":
    init_table()
    analysis()
