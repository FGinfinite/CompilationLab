# 为给定文法自动构造预测分析表

# E → E+T | E-T | T
# T → T*F | T/F | F
# F → (E) | num

# 开始符号
start_symbol = ""
# 非终结符
non_terminals = []
# 终结符
terminals = []
# 产生式
productions = []
# 预测分析表
analysis_table = {}
# FIRST集
FIRST = {}
# FOLLOW集
FOLLOW = {}


def get_new_non_terminal():
    """获取一个新的非终结符"""
    global non_terminals
    new_non_terminal = 'A'
    while True:
        while new_non_terminal in non_terminals:
            new_non_terminal = chr(ord(new_non_terminal) + 1)
        yield new_non_terminal
        new_non_terminal = chr(ord(new_non_terminal) + 1)


# 获取产生式
def get_production(production_file_name: str) -> None:
    """获取产生式"""
    global non_terminals, terminals, productions, start_symbol
    with open(production_file_name, "r") as f:
        for line in f.readlines():
            line = line.strip()
            # 如果是第一行，则为开始符号
            if not start_symbol:
                start_symbol = line[0]
            if line:
                line = line.replace(" ", "")
                production = line.split("->")
                if production[0] not in non_terminals:
                    non_terminals.append(production[0])
                # 添加产生式
                for right_part in production[1].split("|"):
                    productions.append((production[0], right_part))
        for production in productions:
            for char in production[1]:
                if char not in non_terminals and char not in terminals:
                    terminals.append(char)


# 改造文法
def transform_grammar() -> None:
    """改造文法，使其适合自顶向下的分析"""
    global non_terminals, terminals, productions
    new_non_terminal_generator = get_new_non_terminal()
    # Todo: 提取左公因子

    # 消除直接左递归
    for non_terminal in non_terminals:
        # 查找所有以该非终结符开头的产生式
        productions_with_non_terminal = list(filter(lambda x: x[0] == non_terminal, productions))
        # 查找所有以该非终结符开头的产生式右部
        right_parts = list(map(lambda x: x[1], productions_with_non_terminal))
        # 查找所有以该非终结符开头的产生式右部的第一个字符
        first_chars = list(map(lambda x: x[0], right_parts))
        # 如果该非终结符的某个产生式右部的第一个字符是该非终结符，则存在直接左递归
        if non_terminal in first_chars:
            # 消除直接左递归
            productions_without_left_recursion = []
            productions_with_left_recursion = []
            for right_part in right_parts:
                if right_part[0] == non_terminal:
                    productions_with_left_recursion.append(right_part[1:] + non_terminal + "'")
                else:
                    productions_without_left_recursion.append(right_part + non_terminal + "'")
            productions_with_left_recursion.append("ε")

            productions = list(filter(lambda x: x[0] != non_terminal, productions))
            productions.extend(map(lambda x: (non_terminal, x), productions_without_left_recursion))
            productions.extend(map(lambda x: (non_terminal + "'", x), productions_with_left_recursion))
            non_terminals.append(non_terminal + "'")
    # 将产生式与符号集中的E'、T'、F'等符号替换为其他大写字母（如Z、Y、X等）
    i = 0
    while i < len(non_terminals):
        if non_terminals[i][-1] == "'":
            old_non_terminal = non_terminals[i]
            new_non_terminal = next(new_non_terminal_generator)
            non_terminals.remove(non_terminals[i])
            non_terminals.append(new_non_terminal)
            productions = list(map(lambda x: (
                x[0].replace(old_non_terminal, new_non_terminal),
                x[1].replace(old_non_terminal, new_non_terminal)),
                                   productions))

        else:
            i += 1

    # Todo: 消除间接左递归


# 获取FIRST集
def get_first_set(character: str) -> set:
    """获取FIRST集"""
    global FIRST
    # 如果已经计算过该非终结符的FIRST集，则直接返回
    if character in FIRST:
        return FIRST[character]
    # 如果该符号为终结符，则FIRST集为该终结符
    elif character in terminals:
        first_set = {character}
    # 如果该符号为ε，则FIRST集为ε
    elif character == "ε":
        raise ValueError("空串不存在FIRST集")
    # 如果该符号为字符串
    elif len(character) > 1:
        first_set = set()
        first_set.update(get_first_set(character[0]).difference({"ε"}))
        for i in range(0, len(character)):
            if "ε" in get_first_set(character[i]):
                if i == len(character) - 1:
                    first_set.add("ε")
                    break
                first_set.update(get_first_set(character[i + 1]).difference({"ε"}))
            else:
                break
    # 如果该符号为非终结符
    else:
        first_set = set()
        for production in productions:
            # 如果产生式左部为该非终结符
            if production[0] == character:
                # 如果产生式右部第一个字符为终结符或空串
                if production[1][0] in terminals or production[1][0] == "ε":
                    first_set.add(production[1][0])
                # 如果产生式右部第一个字符为该非终结符
                elif production[1][0] == character:
                    raise RecursionError(production + " 存在左递归")
                # 如果产生式右部第一个字符为非终结符
                elif production[1][0] in non_terminals:
                    first_set.update(get_first_set(production[1][0]).difference({"ε"}))
                    for i in range(0, len(production[1])):
                        # 如果产生式右部第i个字符为终结符且FIRST集存在空串
                        if "ε" in get_first_set(production[1][i]) and production[1][i] in non_terminals:
                            if i == len(production[1]) - 1:
                                # 如果产生式右部均为非终结符且FIRST集均存在空串
                                first_set.add("ε")
                            first_set.update(get_first_set(production[1][i + 1]).difference({"ε"}))
                        else:
                            break

    FIRST[character] = first_set
    return first_set


# 非充分地获取FOLLOW集
def get_follow_set(non_terminal: str) -> set:
    """获取FOLLOW集：输入为非终结符，且不为串"""
    global productions, terminals, non_terminals, FOLLOW

    if non_terminal in FOLLOW:
        follow_set = FOLLOW[non_terminal]
    else:
        follow_set = set()
        if non_terminal == start_symbol:
            follow_set.add("$")

    for production in productions:
        pos = production[1].find(non_terminal)
        while pos != -1:
            if pos == len(production[1]) - 1 and non_terminal != production[0]:
                follow_set.update(get_follow_set(production[0]))
            else:
                follow_set.update(get_first_set(production[1][pos + 1:]).difference({"ε"}))
                if "ε" in get_first_set(production[1][pos + 1:]) and non_terminal != production[0]:
                    follow_set.update(get_follow_set(production[0]))
            pos = production[1].find(non_terminal, pos + 1)

    FOLLOW[non_terminal] = follow_set
    return follow_set


# 完成FOLLOW集的构造
def complete_follow_set() -> None:
    global FOLLOW, non_terminals
    while True:
        FOLLOW_copy = FOLLOW.copy()
        for NON_TERMINAL in non_terminals:
            get_follow_set(NON_TERMINAL)
        if FOLLOW == FOLLOW_copy:
            break


def construct_analysis_table():
    global analysis_table, FOLLOW, FIRST, productions, terminals, non_terminals

    get_production("production.txt")
    transform_grammar()
    for non_terminal in non_terminals:
        get_first_set(non_terminal)
    complete_follow_set()

    for non_terminal in non_terminals:
        for terminal in terminals:
            analysis_table[(non_terminal, terminal)] = []
        analysis_table[(non_terminal, "$")] = []
    for production in productions:
        if production[1] == "ε":
            for terminal in FOLLOW[production[0]]:
                analysis_table[(production[0], terminal)].append(production)
        elif production[1][0] in terminals:
            analysis_table[(production[0], production[1][0])].append(production)
        elif production[1][0] in non_terminals:
            for terminal in FIRST[production[1][0]].difference({"ε"}):
                analysis_table[(production[0], terminal)].append(production)

    print("开始符号：" + start_symbol)
    print("非终结符：" + str(non_terminals))
    print("终结符：" + str(terminals))
    print("产生式：" + str(productions))
    print("FIRST集：" + str(FIRST))
    print("FOLLOW集：" + str(FOLLOW))
    print("预测分析表：" + str(analysis_table))


if __name__ == "__main__":
    construct_analysis_table()
