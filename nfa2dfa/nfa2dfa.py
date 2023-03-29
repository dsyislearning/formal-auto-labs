global n # n 表示状态总数
global m # m 表示字母表中的字母个数
global alph # 字母表
alph = []
global nfa # NFA状态转移矩阵
nfa = []
global F # 终止状态集合
F = set()
global DTT # DFA状态转移矩阵
DTT = []

# 主函数
def main():
    get_nfa()
    nfa_to_dfa()
    print_dfa()

# 输入状态
def get_nfa():
    global n
    global m
    global alph
    global nfa
    global F
    print("---------- ε-NFA ----------")
    n = int(input("states number: "))
    print("alphabet: ", end="")
    alph = input().split()
    m = len(alph)
    alph.insert(0, "ε")
    for i in range(n):
        nfa.append([set()] * (m + 1))
        for j in range(m + 1):
            print("δ({}, {}): ".format(i, alph[j]), end="")
            nfa[i][j] = set(map(int, input().split()))
    print("final state(s): ", end="")
    F = set(map(int, input().split()))
    print("----------- DFA -----------")

# 求状态集的星闭包
def e_closure(T):
    global nfa
    if len(T) == 0:
        return set()
    if len(T) == 1:
        res = T
        q = T.pop()
        T.add(q)
        res = res.union(nfa[q][0])
        res = res.union(e_closure(nfa[q][0]))
        return res
    stk = []
    for i in T:
        stk.append(i)
    res = T.copy()
    while len(stk) > 0:
        t = stk.pop()
        for p in e_closure({t}):
            if not p in res:
                res.add(p)
                stk.append(p)
    return res

# 求指定转移函数后的状态集
def move(T, a):
    global nfa
    res = set()
    for q in T:
        res = res.union(nfa[q][a])
    return res

# 求DFA的状态转移矩阵
def nfa_to_dfa():
    global m
    global nfa
    global DTT
    DQ = []
    DQ_state = []
    DQ.append(e_closure({0}))
    DQ_state.append(False)
    while DQ_state.count(False) > 0:
        index = DQ_state.index(False)
        T = DQ[index]
        DQ_state[index] = True
        dtt = [T] + [set()] * m
        for a in range(1, m + 1):
            U = e_closure(move(T, a))
            if DQ.count(U) == 0 and len(U) > 0:
                DQ.append(U)
                DQ_state.append(False)
            dtt[a] = U
        DTT.append(dtt)

# 打印转换后DFA的状态转移矩阵
def print_dfa():
    global m
    global alph
    global DTT
    print("{:^16}\t".format(""), end="")
    for i in range(1, m + 1):
        print("{:^16}\t".format(alph[i]), end="")
    print()
    for i in range(len(DTT)):
        start = ""
        if i == 0:
            start += "-> "
        if is_final(DTT[i][0]):
            start += "*"
        start += str(DTT[i][0])
        print("{:^16}\t".format(start), end="")
        for j in range(1, m + 1):
            print("{:^16}\t".format(str(DTT[i][j])), end="")
        print()

# 判断DFA的某个子集状态是否为终止状态
def is_final(S):
    global F
    for i in F:
        if i in S:
            return True
    return False

# 程序入口
main()
