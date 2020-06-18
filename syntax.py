from _collections import defaultdict

def already_error(dic, key1, key2, val):
    print(f"You are trying to insert to not empty slot.")
    print(f"{key1} {key2} already {dic[key1][key2]}. you tried {val}")

class SLRTable():
    def __init__(self):
        self.follow_sets = {}
        self.transitions = defaultdict(dict)
        self.change_rules = []
        self.non_terminals = []
        self.terminals = []
        self.state_to_change_rules = defaultdict(list)
        self.action_table = defaultdict(dict)
        self.goto_table = defaultdict(dict)

    ## 테이블 생성을 위한 사전자료 추가
    def add_change_rule(self, from_non_terminal, to_things):
        change_rule = (from_non_terminal, to_things)
        self.change_rules.append(change_rule)
        # 변환규칙의 번호를 반환
        return len(self.change_rules) -  1

    def add_state_change_rule(self, state_id, change_rule_shift_index):
        # 변환규칙은 중복 가능. shift_index 까지 합치면 불가능하다.
        self.state_to_change_rules[state_id].append(change_rule_shift_index)

    def add_follow_set(self, non_terminal, terminals):
        if non_terminal in self.follow_sets:
            print(f"{non_terminal} already exists. {self.follow_sets[non_terminal]} Check Follow set add.")
        self.follow_sets[non_terminal] = terminals

    def add_terminals(self, terminals):
        self.terminals = terminals

    def add_non_terminals(self, non_terminals):
        self.non_terminals = non_terminals

    def add_transition(self, from_state, to_state, by_thing):
        self.transitions[from_state][by_thing] = to_state

    ## 테이블 생성 처리 함수
    def add_goto(self, from_state, by_non_terminal, to_state):
        if by_non_terminal not in self.goto_table[from_state]:
            self.goto_table[from_state][by_non_terminal] = to_state
        else:
            already_error(self.goto_table, from_state, by_non_terminal, to_state)

    def add_shift_action(self, from_state, by_terminal, to_state):
        if by_terminal not in self.action_table[from_state]:
            self.action_table[from_state][by_terminal] = ("SHIFT", to_state)
        else:
            already_error(self.action_table, from_state, by_terminal, to_state)

    def add_reduce_action(self, from_state, by_terminal, change_rule):
        if by_terminal not in self.action_table[from_state]:
            self.action_table[from_state][by_terminal] = ("REDUCE", change_rule)
        else:
            already_error(self.action_table, from_state, by_terminal, change_rule)

    # 테이블 생성 처리 진행
    def build_goto_table(self):
        for from_state, transition_dic in self.transitions.items():
            for by_thing, to_state in transition_dic.items():
                if by_thing in self.non_terminals:
                    self.add_goto(from_state, by_thing, to_state)

    def build_action_table(self):
        for from_state, change_rules in self.state_to_change_rules.items():
            for change_rule_index, shift_index in change_rules:
                # shift_index 뒤에 있는게 터미널이고, 그 터미널로 새로운 스테이트로 이동할 수 있어야 함.
                # 그렇다면 쉬프트하고 그 스테이트로 이동.
                start, to = self.change_rules[change_rule_index]
                while True:
                    # terminal a가 shifter 뒤에 있는지 검사
                    after_shifter = to[shift_index:shift_index + 1]
                    if len(after_shifter) == 0:
                        break

                    [after_shifter] = after_shifter
                    if after_shifter not in self.terminals:
                        break

                    # terminal a에 맞는 transition이 있는지 검사

                    if after_shifter not in self.transitions[from_state]:
                        break

                    self.add_shift_action(from_state, after_shifter, self.transitions[from_state][after_shifter])
                    break

                #shifter가 마지막에 있는 변환 룰에 있는 Follow들을 reduce로 한다.
                while True:
                    # shifter가 마지막에 있는지 검사.
                    # 변환룰 결과 3개 스트링이 나오면, shifter는 3이여야 한다. 가능한 shifter는 (0,1,2,3)
                    if len(to) != shift_index:
                        break

                    if start not in self.follow_sets:
                        print(f"start {start}의 Follow Sets은 없습니다. 스타트 심벌인가보네요!")
                        break
                    for terminal in self.follow_sets[start]:
                        self.add_reduce_action(from_state, terminal, change_rule_index)
                    break