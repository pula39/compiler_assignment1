from collections import defaultdict

class Dfa():
    def __init__(self, type):
        self.states = []
        self.finite_states = []
        self.rules = defaultdict(dict)
        self.type = type

    def set_states(self, state_list):
        self.states = state_list

    def set_finite_states(self, finite_state_list):
        self.finite_states = finite_state_list

    def add_rule(self, from_state, to_state, transit_literal_list):
        self.rules[from_state][transit_literal_list] = to_state

    def try_accept(self, code, start_pos):
        accepted = self.accept_this(0, code[start_pos:], 0)

        if accepted is None:
            return None
        else:
            end_pos = start_pos + accepted
            print(f"accepted to {start_pos} -> {end_pos}")
            print(code[start_pos:end_pos])
            return (self.type, code[start_pos:end_pos], end_pos)

    def accept_this(self, current_state, code, current_pos):
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

    def parse_next(self):
        parsed = self.get_current_token()

        if parsed is None:
            print("Parse Failed")
            return False

        self.parsed_token.append(parsed)

    def add_dfa(self, dfa):
        self.dfa_list.append(dfa)

    def parse_end(self):
        return self.start_pos == len(self.code)

    def parse_token(self):
        for dfa in self.dfa_list:
            ret = dfa.try_accept(self.code, self.start_pos)

            if ret is None:
                continue

            ret_type, ret_value, end_pos = ret

            print(f"parse success. {ret}. start_pos adjusted to {end_pos}")
            self.start_pos = end_pos
            return (ret_type, ret_value)

        print(f"parse failed. for {self.code[self.start_pos:]}")

        return None
