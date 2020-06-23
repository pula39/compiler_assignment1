from syntax import *
import sys
import json
from classes import *
from pprint import pprint


def main(file_path):
    with open(file_path, "r") as f:
        tokens = json.load(f)["body"]

    print(tokens)
    tokens = list(filter(lambda token: token[0] != Token.WHITE_SPACE, tokens))

    slr_table = SLRTable()

    block_trans = [54, 55, 57, 85, 86, 87, 88, 89, 10, 11, 18]
    block_trans_with_SMTM = [32, 54, 55, 57, 85, 86, 87, 88, 89, 10, 11, 18]
    T0 = [0, 2, 4, 3, 5, 10, 11, 26]
    T1 = [1]
    T2 = [6, 3, 5, 2, 10, 11, 4, 26]
    T3 = [7, 3, 5, 2, 10, 11, 4, 26]
    T4 = [12, 13, 18, 27]  # 글자 확인 필요
    T5 = [8]
    T6 = [9]
    T7 = [14, 19, 28]
    T8 = [15]
    T9 = [16]
    T10 = [20, 21, 22, 59, 60, 65, 69, 71, 72, 73, 74]  # 59 확인 필요
    T11 = [29, 36, 40, 41]
    T12 = [17]
    T13 = [24]
    T14 = [25]
    T15 = [61, 62]
    T16 = [66, 70]
    T17 = [80]
    T18 = [79]
    T19 = [78]
    T20 = [75, 59, 60, 65, 69, 71, 72, 73, 74]  # 59 확인 필요
    T21 = [30]
    T22 = [37]
    T23 = [63, 60, 59, 65, 69, 71, 72, 73, 74]  # 69 확인 필요
    T24 = [67, 65, 69, 71, 72, 73, 74]
    T25 = [76]
    T26 = [31]
    T27 = [38, 42, 43, 45]
    T28 = [64]
    T29 = [68]
    T30 = [77]
    T31 = [32] + block_trans[:]
    T32 = [39]
    T33 = [44]
    T34 = [33, 49]
    T35 = [56] + block_trans[:]
    T36 = [90]
    T37 = [91]
    T38 = [23]
    T39 = [94]
    T40 = [95]
    T41 = [12, 13, 18]
    T42 = [46]
    T43 = [34]
    T44 = [50, 71, 72, 73, 74]
    T45 = [58]
    T46 = [92]
    T47 = [93]
    T48 = [97, 81, 71, 72, 73, 74]
    T49 = [98, 18]
    T50 = [14, 19]
    T51 = [47, 42, 43, 45]
    T52 = [35]
    T53 = [52]
    T54 = [96, 81, 71, 72, 73, 74]
    T55 = [100]
    T56 = [82]
    T57 = [101]
    T58 = [19]
    T59 = [48]
    T60 = [53]
    T61 = [99]
    T62 = [103]
    T63 = [83, 71, 72, 73, 74]
    T64 = [104, 81, 71, 72, 73, 74]
    T65 = [102]
    T66 = [106] + block_trans_with_SMTM[:]
    T67 = [84]
    T68 = [107]
    T69 = [105] + block_trans_with_SMTM[:]
    T70 = [109] + block_trans_with_SMTM[:]
    T71 = [110, 18]
    T72 = [108]
    T73 = [116]
    T74 = [111]
    T75 = [117, 119, 120, 121]
    T76 = [112]
    T77 = [118]
    T78 = [122]
    T79 = [113] + block_trans_with_SMTM[:]
    T80 = [123] + block_trans_with_SMTM[:]
    T81 = [114]
    T82 = [124]
    T83 = [115]
    T84 = [51]
    T_LIST = [T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22,
              T23, T24, T25, T26, T27, T28, T29, T30, T31, T32, T33, T34, T35, T36, T37, T38, T39, T40, T41, T42, T43,
              T44, T45, T46, T47, T48, T49, T50, T51, T52, T53, T54, T55, T56, T57, T58, T59, T60, T61, T62, T63, T64,
              T65, T66, T67, T68, T69, T70, T71, T72, T73, T74, T75, T76, T77, T78, T79, T80, T81, T82, T83, T84]
    NFA_NUMBERS = list(range(0, 125))  # 0 ~ 124
    nfa_list_of_us = [y for x in T_LIST for y in x]
    for n in NFA_NUMBERS:
        if n not in nfa_list_of_us:
            print(f"{n}이 우리가 만든 DFA에 없어보입니다.")

    # NFA를 옮겨놓은것임
    # (nfa_state_index, shift_index)
    change_rules = [
        ["S",
         (["CODE"], [(0, 0), (1,1)]),
         ],
        ["CODE",
         (["VDECL", "CODE"], [(2, 0), (6, 1), (8, 2)]),
         (["FDECL", "CODE"], [(4, 0), (7, 1), (9, 2)]),
         ([], [(3, 0), (5, 1)])
         ],
        ["VDECL",
         (["vtype", "id", "semi"], [(10, 0), (12, 1), (14, 2), (16, 3)]),
         (["vtype", "ASSIGN", "semi"], [(11, 0), (13, 1), (15, 2), (17, 3)])
         ],
        ["ASSIGN",
         (["id", "assign", "RHS"], [(18, 0), (19, 1),(20, 2),(24, 3)])
         ],
        ["FDECL",
         (["vtype", "id", "lparen", "ARG", "rparen", "lbrace", "BLOCK", "RETURN", "rbrace"], [(26, 0), (27, 1), (28, 2), (29, 3), (30, 4), (31, 5), (32, 6), (33, 7), (34, 8), (35, 9)])
         ],
        ["ARG",
         (["vtype", "id", "MOREARGS"], [(36, 0),(37, 1),(38, 2),(39, 3)]),
         ([], [(40, 0), (41, 1)])
         ],
        ["MOREARGS",
         (["comma", "vtype", "id", "MOREARGS"], [(42, 0), (44, 1), (46, 2), (47, 3), (48, 4), ]),
         ([], [(43, 0),(45, 1)])
         ],
        ["BLOCK",
         (["STMT", "BLOCK"], [(54, 0),(56, 1),(58, 2)]),
         ([], [(55, 0),(57, 1)])
         ],
        ["STMT",
         (["VDECL"], [(85, 0),(90, 1),]),
         (["ASSIGN", "semi"], [(86, 0),(91, 1),(92, 2)]),
         (["if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace", "ELSE"], [(87, 0),(93, 1),(96, 2),(99, 3),(102, 4),(105, 5),(108, 6),(117, 7),(118, 8),]),
         (["while", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace"], [(88, 0),(94, 1),(97, 2),(100, 3),(103, 4),(106, 5),(109, 6),(116, 7)]),
         (["for", "lparen", "ASSIGN", "semi", "COND", "semi", "ASSIGN", "rparen", "lbrace", "BLOCK", "rbrace"], [(89, 0),(95, 1),(98, 2),(101, 3),(104, 4),(107, 5),(110, 6),(111, 7),(112, 8),(113, 9),(114, 10),(115, 11), ])
         ],
        ["ELSE",
         (["else", "lbrace", "BLOCK", "rbrace"], [(119,0),(122,1),(123,2),(124,3),(51, 4)]),
         ([], [(120, 0),(121, 1)])
         ],
        ["RHS",
         (["EXPR"], [(21,0), (25, 1)]),
         (["literal"], [(22,0), (23, 1)])
         ],
        ["EXPR",
         (["TERM", "addsub", "EXPR"], [(60, 0),(62, 1),(63, 2),(64, 3)]),
         (["TERM"], [(59, 0),(61, 1)])
         ],
        ["TERM",
         (["FACTOR", "multdiv", "TERM"], [(65, 0),(66, 1),(67, 2),(68, 3)]),
         (["FACTOR"], [(69, 0),(70, 1)])
         ],
        ["FACTOR",
         (["lparen", "EXPR", "rparen"], [(74, 0),(75, 1),(76, 2),(77, 3)]),
         (["id"], [(72, 0),(79, 1),]),
         (["num"], [(71, 0),(80, 1)]),
         (["float"], [(73, 0),(78, 1)])
         ],
        ["COND",
         (["FACTOR", "comp", "FACTOR"], [(81, 0),(82, 1),(83, 2),(84, 3)])
         ],
        ["RETURN",
         (["return", "FACTOR", "semi"], [(49, 0),(50, 1),(52, 2),(53, 3)])
         ],
    ]

    non_terminals = []
    change_rule_list = []
    terminals = set()

    # 검증용 데이터
    tran_list_count = 0
    visual_change_rule_dic = defaultdict(list)

    for l in change_rules:
        non_terminals.append(l[0])
        for rules, tran_list in l[1:]:
            tran_list_count += len(tran_list)
            new_tran_list = []
            # nfa의 state + index
            # dfa의 state + index로 치환한다.
            for nfa_state_index, shift_index in tran_list:
                for dfa_state, nfa_state_list in enumerate(T_LIST):
                    if nfa_state_index in nfa_state_list:
                        new_tran_list.append((dfa_state, shift_index))
                        visual_change_rule_dic[dfa_state].append((l[0], rules, shift_index))

            change_rule_list.append((l[0], rules, new_tran_list))

            for rule_symbol in rules:
                terminals.add(rule_symbol)

    terminals = list(filter(lambda symbol: symbol not in non_terminals, list(terminals)))

    print(f"{tran_list_count}개의 nfa 스테이트가 있었읍니다. 제대로 했다면.")
    pprint(visual_change_rule_dic)
    print("non_terminals", non_terminals)
    print("terminals", terminals)

    change_counter = 0
    for n, n, t_l in change_rule_list:
        change_counter += len(t_l)
    print(f"DFA에 있는 change 갯수는 {change_counter}개입니다. 확인해봐요!")

    for start, to, state_infos in change_rule_list:
        i = slr_table.add_change_rule(start, to)
        for state_index, shift_index in state_infos:
            # State Index에 change Index와 Shift Index의 Tuple을 넣어준다.
            slr_table.add_state_change_rule(state_index, (i, shift_index))

    # FOLLOW SET 입력
    slr_table.add_follow_set("S", ['$'])
    slr_table.add_follow_set("CODE", ['$'])
    slr_table.add_follow_set("VDECL", ['vtype', 'if', 'while', 'for', 'id', '$', 'rbrace', 'return'])
    slr_table.add_follow_set("ASSIGN", ['semi', 'rparen'])
    slr_table.add_follow_set("FDECL", ['vtype', '$'])
    slr_table.add_follow_set("ARG", ['rparen'])
    slr_table.add_follow_set("MOREARGS", ['rparen'])
    slr_table.add_follow_set("BLOCK", ['rbrace', 'return'])
    slr_table.add_follow_set("STMT", ['if', 'while', 'for', 'vtype', 'id', 'rbrace', 'return'])
    slr_table.add_follow_set("ELSE", ['if', 'while', 'for', 'vtype', 'id', 'rbrace', 'return'])
    slr_table.add_follow_set("RHS", ['semi', 'rparen'])
    slr_table.add_follow_set("EXPR", ['rparen', 'semi'])
    slr_table.add_follow_set("TERM", ['addsub', 'rparen', 'semi'])
    slr_table.add_follow_set("FACTOR", ['semi', 'comp', 'multdiv', 'rparen', 'addsub'])
    slr_table.add_follow_set("COND", ['rparen', 'semi'])
    slr_table.add_follow_set("RETURN", ['rbrace'])

    slr_table.add_terminals(terminals + ["$"])
    slr_table.add_non_terminals(non_terminals)

    # DFA 입력

    # block_move: T66 포탈을 모아둔거
    block_move = [(35, NT.STMT), (36, NT.VDECL), (37, NT.ASSIGN), (47, Token.IF), (39, Token.WHILE), (40, Token.FOR), ( 41, Token.V_TYPE), (58, Token.ID)]
    trans = [
        (0, [(4, Token.V_TYPE), (1, NT.CODE), (2,NT.VDECL), (3, NT.FDECL)]),
        (2, [(2, NT.VDECL), (3, NT.FDECL), (4, Token.V_TYPE), (5, NT.CODE)]),
        (3, [(2, NT.VDECL), (3, NT.FDECL), (4, Token.V_TYPE), (6, NT.CODE)]),
        (4, [(7, Token.ID), (8, NT.ASSIGN)]),
        (7, [(10, Token.ASSIGN), (9, Token.SEMI), (11, Token.L_PAREN)]),
        (8, [(12, Token.SEMI)]),
        (10, [(13, NT.RHS), (14, NT.EXPR), (15, NT.TERM), (16, NT.FACTOR), (17, Token.NUM), (18, Token.ID), (19, Token.FLOAT), (20, Token.L_PAREN), (38, Token.LITERAL) ]),
        (11, [(21, NT.ARG), (22, Token.V_TYPE)]),
        (15, [(23, Token.ADDSUB)]),
        (16, [(24, Token.MULTDIV)]),
        (20, [(20, Token.L_PAREN), (25, NT.EXPR), (19, Token.FLOAT), (15, NT.TERM), (18, Token.ID), (17, Token.NUM), (16, NT.FACTOR)]),
        (21, [(26, Token.R_PAREN)]),
        (22, [(27, Token.ID)]),
        (23, [(15, NT.TERM), (16, NT.FACTOR), (17, Token.NUM), (18, Token.ID), (19, Token.FLOAT), (17, Token.NUM), (28, NT.EXPR)]),
        (24, [(17, Token.NUM), (18, Token.ID), (19, Token.FLOAT), (20, Token.L_PAREN), (29, NT.TERM), (16, NT.FACTOR)]),
        (25, [(30, Token.R_PAREN)]),
        (26, [(31, Token.L_BRACE)]),
        (27, [(32, NT.MOREARGS), (33, Token.COMMA)]),
        (31, [(34, NT.BLOCK), (35, NT.STMT), (36, NT.VDECL), (37, NT.ASSIGN), (47, Token.IF), (39, Token.WHILE), (40, Token.FOR), (41, Token.V_TYPE), (58, Token.ID)]),
        (33, [(42, Token.V_TYPE)]),
        (34, [(44, Token.RETURN), (43, NT.RETURN)]),
        (35, [(45, NT.BLOCK), (35, NT.STMT), (36, NT.VDECL), (37, NT.ASSIGN), (47, Token.IF), (39, Token.WHILE), (40, Token.FOR), (41, Token.V_TYPE), (58, Token.ID)]),
        (37, [(46, Token.SEMI)]),
        (39, [(48, Token.L_PAREN)]),
        (40, [(49, Token.L_PAREN)]),
        (41, [(8, NT.ASSIGN), (50, Token.ID)]),
        (42, [(51, Token.ID)]),
        (43, [(52, Token.R_BRACE)]),
        (44, [(53, NT.FACTOR), (17, Token.NUM),(18, Token.ID),(19, Token.FLOAT),(20, Token.L_PAREN)]),
        (47, [(54, Token.L_PAREN)]),
        (48, [(55, NT.COND), (56, NT.FACTOR)]),
        (49, [(58, Token.ID), (57, NT.ASSIGN)]),
        (50, [(9, Token.SEMI), (10, Token.ASSIGN)]),
        (51, [(59, NT.MOREARGS)]),
        (53, [(60, Token.SEMI)]),
        (54, [(61, NT.COND), (56, NT.FACTOR), (17, Token.NUM), (18, Token.ID), (19, Token.FLOAT), (20, Token.L_PAREN)]),
        (55, [(62, Token.R_PAREN)]),
        (56, [(63, Token.COMP)]),
        (57, [(64, Token.SEMI)]),
        (58, [(10, Token.ASSIGN)]),
        (61, [(65, Token.R_PAREN)]),
        (62, [(66, Token.L_BRACE)]),
        (63, [(67, NT.FACTOR), (17, Token.NUM), (18, Token.ID), (19, Token.FLOAT), (20, Token.L_PAREN)]),
        (64, [(68, NT.COND), (17, Token.NUM), (18, Token.ID), (19, Token.FLOAT), (20, Token.L_PAREN), (56, NT.FACTOR)]),
        (65, [(69, Token.L_BRACE)]),
        (66, [(70, NT.BLOCK)] + block_move[:]),
        (68, [(71, Token.SEMI)]),
        (69, [(72, NT.BLOCK)] + block_move[:]),
        (70, [(73, Token.R_BRACE)] + block_move[:]),
        (71, [(74, NT.ASSIGN), (58, Token.ID)]),
        (72, [(75, Token.R_BRACE)] + block_move[:]),
        (73, [(76, Token.R_PAREN)]),
        (74, [(76, Token.R_PAREN)]),
        (75, [(77, NT.ELSE), (78, Token.ELSE)]),
        (76, [(79, Token.L_BRACE)]),
        (78, [(80, Token.L_BRACE)]),
        (79, [(81, NT.BLOCK)] + block_move[:]),
        (80, [(82, NT.BLOCK)] + block_move[:]),
        (81, [(83, Token.R_BRACE)] + block_move[:]),
        (82, [(84, Token.R_BRACE)] + block_move[:]),
    ]

    for s, t_list in trans:
        for to_state, symbol in t_list:
            slr_table.add_transition(s, to_state, symbol)

    print("테이블 준비끝")
    slr_table.build_goto_table()
    slr_table.build_action_table()

    print("Action Table")
    pprint(slr_table.action_table)
    print("GOTO TABLE")
    pprint(slr_table.goto_table)
    #
    sa = SyntaxAnalyzer(slr_table, tokens + ["$"])
    while True:
        ret = sa.parse_one()
        if ret == "END":
            print("성공적완수")
            print("미방문 STATE", list(filter(lambda x: x not in sa.passed_state, list(range(0,85)))))
            print("미사용 NFA", list(filter(lambda x: x not in sa.passed_change_rule, list(range(0,185)))))
            break

        if ret != True:
            _ret, error_symbol = ret
            print("에러발생, 바로여기서.", error_symbol)
            break


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("plaese pass file path")
        sys.exit()

    file_path = sys.argv[1]

    print("File path : " + file_path)

    main(file_path)
