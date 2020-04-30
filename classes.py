from enum import Enum, auto
from collections import defaultdict

class TokenKind(Enum):
    pass


class dfa():
    def __init__(self):
        self.states = []
        self.finite_states = []
        self.rules =  defaultdict({})

    def set_states(self, state_list):
        self.states = state_list

    def set_finite_states(self, finite_state_list):
        self.finite_states = finite_state_list

    def add_rule(self, state_number, transit_literal_list, to_state):
        self.rules[state_number][transit_literal_list] = to_state

    def try_accept(self, code, start_pos):
        accepted = self.accept_this(self, 0, code[start_pos:], 0)

    def accept_this(self, current_state, code, current_pos):
        current_literal = code[current_pos]

        current_state.finite_states()

        for rule_literal_list, rule_state in self.rules[current_state]:
            if current_literal not in rule_literal_list:
                continue

            accept_end_pos = self.accept_this(self, rule_state, code, current_pos + 1)

            if accept_end_pos is None:
                continue

            return accept_end_pos

        # 받아주는 게 없으면 false

        return None



class token_scanner():
    def __init__(self, source_code):
        self.code = source_code
        self.start_pos = 0
        self.end_pos = 0
        self.parsed_token = []

    def parse_next(self):
        parsed = get_current_token()


    def reset_end_pos(self):
        self.start_pos = self.end_pos

    def parse_token(self):
        if
        if self.has_valid_token():
            self.
            return self.code[self.start_pos, self.end_pos]
        else:
            return None

    def has_valid_token(self):
        if()
