from syntax import *
import sys
import json


def main(file_path):
    with open(file_path, "r") as f:
        tokens = json.load(f)["body"]
        # f.writelines(map(lambda t: f"{t}\n", token_list))
    print(tokens)

    slr_table = SLRTable()

    change_rule_list = [
        # Start, [to들(심볼다하나씩잘라서)], [(state_index, shift_index)]
        ("S'", ["E"], [(1,0), (2,1)]),
        ("E", ["T", "*", "E"], [(1,0), (3,1), (3,0), (6,0), (6,2), (8,3)]),
        ("E", ["T"], [(1,0), (3,1), (4,0), (6,0)]),
        ("T", ["(", "E", ")"], [(1,0), (4,0), (4,1), (6,0), (7,2), (9,3)]),
        ("T", ["ID"], [(1,0), (4,0), (5,1), (6,0)]),
    ]

    change_counter = 0
    for n, n, t_l in change_rule_list:
        change_counter += len(t_l)
    print(f"DFA에 있는 change 갯수는 {change_counter}개입니다. 확인해봐요!")

    for start, to, state_infos in change_rule_list:
        i = slr_table.add_change_rule(start, to)
        for state_index, shift_index in state_infos:
            # State Index에 change Index와 Shift Index의 Tuple을 넣어준다.
            slr_table.add_state_change_rule(state_index, (i, shift_index))

    slr_table.add_follow_set("S'", ['$'])
    slr_table.add_follow_set("E", [')', '$'])
    slr_table.add_follow_set("T", ['*', ')', '$'])

    slr_table.add_terminals(["ID", "*", "(", ")", "$"])
    slr_table.add_non_terminals(["E", "T"])

    slr_table.add_transition(1,2,"E")
    slr_table.add_transition(1,3,"T")
    slr_table.add_transition(1,4,"(")
    slr_table.add_transition(1,5,"ID")
    #2는 없음
    slr_table.add_transition(3,6,"*")

    slr_table.add_transition(4,3,"T")
    slr_table.add_transition(4,4,"(")
    slr_table.add_transition(4,5,"ID")
    slr_table.add_transition(4,7,"E")
    #5는없음
    slr_table.add_transition(6,3,"T")
    slr_table.add_transition(6,4,"(")
    slr_table.add_transition(6,8,"E")
    slr_table.add_transition(6,5,"ID")

    slr_table.add_transition(7,9,")")
    #8은 없음
    #9는 없음

    slr_table.build_goto_table()
    slr_table.build_action_table()

    from pprint import pprint
    print("Action Table")
    pprint(slr_table.action_table)
    print("GOTO TABLE")
    pprint(slr_table.goto_table)

    sa = SyntaxAnalyzer(slr_table, ["ID", "*", "ID", "$"])
    while True:
        if sa.parse_one() != True:
            break

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("plaese pass file path")
        sys.exit()

    file_path = sys.argv[1]

    print("File path : " + file_path)

    main(file_path)


