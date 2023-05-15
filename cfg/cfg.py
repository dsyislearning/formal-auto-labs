global N # 非终结符
global T # 终结符
global P # 产生式
N = []
T = []
P = []

# 主函数
def main():
    input_cfg()
    transform_cfg()
    output_cfg()

# 上下文无关文法变换算法
def transform_cfg():
    eliminate_epsilon_production()
    remove_unit_production()
    remove_useless_symbols()

###############################################################################
################################ 消 ε 产生式 ###################################
###############################################################################

# 消 ε 产生式
def eliminate_epsilon_production():
    global N, T, P
    V = set() # 可致空符号集
    # 找所有可致空符号，删除可致空
    number = -1
    while number != len(V):
        number = len(V)
        for production in P:
            start = production.split("->")[0]
            sentence = production.split("->")[1]
            if sentence == "ε": # 若直接可以推出空
                V.add(start)
                P.remove(production) # 去掉直接推出空的产生式
            elif sentence.isupper(): # 若间接可以推出空
                can_be_null = True
                for char in sentence:
                    if char not in V:
                        can_be_null = False
                        break
                if can_be_null:
                    V.add(start)
    # 对每一个含有可致空符号的产生式
    # 添加去掉可致空符号后组合出来的新产生式
    new_P = set(P) # 新产生式集合
    for production in P:
        start = production.split("->")[0]
        sentence = production.split("->")[1]
        numeber_list = []
        char_list = list(sentence)
        for i in range(len(sentence)):
            if char_list[i] in V:
                numeber_list.append(i)
        if len(numeber_list) != 0:
            new_sentences = get_combinations(sentence, numeber_list, 0)
            for new_sentence in new_sentences:
                 # 构造新产生式要先删除临时插入的 ε，但 A->ε 不能加入
                if new_sentence != "ε":
                    new_P.add(start + "->" + new_sentence.replace("ε", ""))
            numeber_list.clear()
    # 如果起始符本身就可致空，加入新产生式
    if "S" in V:
        new_P.add("S0->S")
        new_P.add("S0->ε")
        N.append("S0")
    # 终结符集合中删除 ε
    if T.count("ε") != 0:
        T.remove("ε")
    # 更新产生式
    P = sorted(new_P)

# 递归求组合出来的新产生式
def get_combinations(sentence: str, lst: list[int], u: int) -> list[str]:
    new_sentences = []
    # 终止条件：最后一个致空符 取 or 不取
    if u == len(lst) - 1:
        res = list(sentence)
        new_sentences.append("".join(res))
        res[lst[u]] = "ε"
        new_sentences.append("".join(res))
        return new_sentences
    # 当前致空符 取 or 不取
    res = list(sentence)
    new_sentences.extend(get_combinations("".join(res), lst, u + 1)) # 取
    res[lst[u]] = "ε"
    new_sentences.extend(get_combinations("".join(res), lst, u + 1)) # 不取
    # 返回最终结果
    return new_sentences

###############################################################################
################################ 消单产生式 ####################################
###############################################################################

# 消单产生式
def remove_unit_production():
    global P
    U = get_all_unit_productions(P) # 单产生式集合
    new_P = set(P) - set(U) # 非单产生式集合
    # 将单产生式右边直接给到左边
    lst = []
    for productionA in U:
        startA = productionA.split("->")[0]
        sentenceA = productionA.split("->")[1]
        if startA != sentenceA: # A->B
            for productionB in new_P: # A->B
                startB = productionB.split("->")[0]
                sentenceB = productionB.split("->")[1]
                if startB == sentenceA: # B->alpha
                    lst.append(startA + "->" + sentenceB) # A->alpha
    for string in lst:
        new_P.add(string)
    # 更新消单产生式后的产生式集合
    P = sorted(new_P)

# 获取所有单产生式
def get_all_unit_productions(productions: list[str]) -> set:
    global N
    result = set()
    for startA in N:
        Na = {startA}
        number = 0
        while number != len(Na):
            number = len(Na)
            for productionB in productions:
                startB = productionB.split("->")[0]
                sentenceB = productionB.split("->")[1]
                if len(sentenceB) == 1 and sentenceB.isupper() and startB in Na:
                    Na.add(sentenceB)
                    result.add(startA + "->" + sentenceB)
    return result

###############################################################################
################################# 消无用符号 ###################################
###############################################################################

# 消无用符号
def remove_useless_symbols():
    remove_non_generating_symbols()
    remove_unreachable_symbols()

# 消非生成符号
def remove_non_generating_symbols():
    global N, P
    new_N = set() # 新非终结符集合
    # 先将所有能够直接生成由终结符组成字符串的非终结符加入集合V
    for production in P:
        start = production.split("->")[0]
        sentence = production.split("->")[1]
        if sentence.islower():
            new_N.add(start)
    # 接下来不断迭代直至找到所有生成符号
    number = 0
    while number != len(new_N):
        number = len(new_N)
        for production in P:
            start = production.split("->")[0]
            sentence = production.split("->")[1]
            is_generating = True
            for char in sentence:
                if char.isupper() and char not in new_N:
                    is_generating = False
                    break
            if is_generating:
                new_N.add(start)
    # 将可达符号加入新生成式集合
    to_be_deleted = set()
    for production in P:
        for char in production:
            if char.isupper() and char in set(N) - new_N:
                to_be_deleted.add(production)
    for char in to_be_deleted:
        P.remove(char)
    # 更新非终结符集合
    N = sorted(new_N)

# 消不可达符号
def remove_unreachable_symbols():
    global N, T, P
    # 新非终结符集合
    if "S0" in N:
        new_N = {"S0"}
    else:
        new_N = {"S"}
    # 新终结符集合
    new_T = set()
    # 新产生式集合
    new_P = set()
    # 迭代找可达符号集合
    number = 0
    while number != len(new_N):
        number = len(new_N)
        # 遍历，找到起始符可达的生成式
        for production in P:
            start = production.split("->")[0]
            sentence = production.split("->")[1]
            # 将生成式右边的内容全部加入新的终结符、非终结符集合
            if start in new_N:
                for char in sentence:
                    if char.isupper():
                        new_N.add(char)
                    elif char.islower():
                        new_T.add(char)
    # 删除所有未使用过的生成式
    for production in P:
        start = production.split("->")[0]
        sentence = production.split("->")[1]
        if start in new_N:
            new_P.add(production)
    # 终结符不包含 ε
    if "ε" in new_T:
        new_T.remove("ε")
    # 更新非终结符、终结符、生成式集合
    N = sorted(new_N)
    T = sorted(new_T)
    P = sorted(new_P)

###############################################################################
################################ 文件输入输出 ##################################
###############################################################################

# 从 in.txt 中读取上下文无关文法
def input_cfg():
    global N, T, P
    productions = []
    with open("./cfg/in.txt", "r", encoding="utf-8") as work_data:
        productions = work_data.readlines()
        N = get_non_terminator(productions)
        T = get_terminator(productions)
        P = split_productions(productions)

# 获取非终结符
def get_non_terminator(productions: list[str]) -> list[str]:
    result = set()
    for production in productions:
        for char in production:
            if char.isupper():
                result.add(char)
    return sorted(result)

# 获取终结符
def get_terminator(productions: list[str]) -> list[str]:
    result = set()
    for production in productions:
        for char in production:
            if char.islower():
                result.add(char)
    return sorted(result)

# 将简写的生成式拆开成统一形式
def split_productions(productions: list[str]) -> list[str]:
    result = []
    for production in productions:
        production = production.strip("\n")
        start = production.split("->")[0]
        sentences = production.split("->")[1].split("|")
        for sentence in sentences:
            result.append(start + "->" + sentence)
    return result

# 向 out.txt 输出变换后的上下文无关文法
def output_cfg():
    global P
    with open("./cfg/out.txt", "w", encoding="utf-8") as work_data:
        # 输出非终结符
        work_data.write("N:\n")
        work_data.write(", ".join(N))
        work_data.write("\n\n")
        # 输出终结符
        work_data.write("T:\n")
        work_data.write(", ".join(T))
        work_data.write("\n\n")
        # 输出产生式
        work_data.write("P: \n")
        # 将拆开写的文法合并简写
        productions = wrap_up_productions(P)
        # 将生成式一条条写入输出文件
        for production in productions:
            work_data.write(production)
            work_data.write("\n")

# 将统一形式的文法进行简写
def wrap_up_productions(productions: list[str]) -> list[str]:
    result = []
    starts = set()
    # 将所有生成式左边的非终结符加到集合中
    for production in productions:
        starts.add(production.split("->")[0])
    starts = sorted(starts)
    # 将每个非终结符的产生式合并简写
    for start in starts:
        new_production = start + "->"
        for production in productions:
            if production.split("->")[0] == start:
                new_production += production.split("->")[1] + "|"
        result.append(new_production.strip("|"))
    # 将起始符放到最前面
    for i in range(len(result)):
        if result[i].split("->")[0] == "S":
            result.insert(0, result.pop(i))
            break
    for i in range(len(result)):
        if result[i].split("->")[0] == "S0":
            result.insert(0, result.pop(i))
            break
    # 返回结果
    return result

###############################################################################
################################ 程序入口 ######################################
###############################################################################

# 程序入口
main()
