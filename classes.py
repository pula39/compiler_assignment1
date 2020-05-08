from collections import defaultdict

class Dfa():
    def __init__(self, type):
        self.states = []
        self.finite_states = []
        self.rules = defaultdict(dict)
        self.type = type

    # DFA의 Final states를 작성한다.
    def set_final_states(self, finite_state_list):
        self.finite_states = finite_state_list

    # DFA의 Transition rule을 작성한다.
    def add_rule(self, from_state, to_state, transit_literal_list):
        self.rules[from_state][transit_literal_list] = to_state

    # start_pos 부터 code를 봐서, Parse 될 수 있는 token이 있는지 시도해본다.
    # Parse 된 token의 type, value, 파싱한 범위를 반환한다.
    def try_accept(self, code, start_pos):
        accepted = self.accept_this(0, code[start_pos:], 0)

        if accepted is None:
            return None
        else:
            end_pos = start_pos + accepted
            return (self.type, code[start_pos:end_pos], end_pos)

    # 제시된 literal에 대해, accept 하는지 재귀로 확인한다.
    def accept_this(self, current_state, code, current_pos):
        # 현재 판단되는 literal을 가져온다.
        current_literal = code[current_pos:current_pos+1]

        literal_left = current_literal is not ''

        has_rule = False

        # 글자가 남아있으면 돌려본다.
        if literal_left:
            for rule_literal_list, rule_state in self.rules[current_state].items():
                if current_literal not in rule_literal_list:
                    continue

                has_rule = True
                accept_end_pos = self.accept_this(rule_state, code, current_pos + 1)

                if accept_end_pos is None:
                    continue

                return accept_end_pos

        # 남아있는 글자로 갈 규칙이 있었는데, 위에서 return 되지 않았음 -> Accept 된 규칙이 없음. 실패.
        if has_rule:
            return None

        # 글자가 남아있는게 없거나 그 글자에 해당되는 Rule이 없을 때
        if current_state in self.finite_states:
            return current_pos
        else:
            return None


class TokenScanner():
    def __init__(self, source_code):
        self.code = source_code
        self.start_pos = 0
        self.parsed_token = []
        self.dfa_list = []

    def add_dfa(self, dfa):
        self.dfa_list.append(dfa)

    # parsing이 성공적으로 끝난 상태인지 조회한다.
    def parse_end(self):
        return self.start_pos == len(self.code)

    def parse_token(self):
        parsed_tokens = []
        # 모든 dfa 중에 parse 성공하는 dfa를 보고, 있으면 return 한다.
        for dfa in self.dfa_list:
            ret = dfa.try_accept(self.code, self.start_pos)

            if ret is None:
                continue

            print(f"{ret} accepted to {self.start_pos} -> {ret[2]}, add to parsed_tokens.")
            parsed_tokens.append(ret)
            # 한 Token Parse 에 성공했으므로, start_pos를 end_pos로 해준다.

        if len(parsed_tokens) > 0:
            #같은 endpos면 앞에 것이 나옴
            print(parsed_tokens)
            longest_match = max(parsed_tokens, key=lambda p: p[2])

            ret_type, ret_value, end_pos = longest_match

            self.start_pos = end_pos

            return (ret_type, ret_value)

        print(f"parse failed. for {self.code[self.start_pos:]}")
        return None
