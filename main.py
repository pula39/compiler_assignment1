import sys
from classes import *
import pprint
import os

# system keword 에 대한 dfa를 자동생성한다.
def make_system_dfa(name, keyword):
    digit = "1234567890"
    char = "qwertyuiopasdfghjklzxcvbnm"

    length = len(keyword)
    dfa = Dfa(name)
    dfa.set_final_states([length])

    for i in range(0, length):
        dfa.add_rule(i,i+1, keyword[i])

    return dfa

# 한 글자를 판단하기 위한 dfa를 작성한다.
def make_single_dfa(name, char):
    dfa = Dfa(name)
    dfa.set_final_states([1])
    dfa.add_rule(0, 1, char)
    return dfa

# dfa 작성 코드가 너무 길어서 별도의 함수로 분리.
def set_dfa(token_scanner):
    digit = "1234567890"
    char = "qwertyuiopasdfghjklzxcvbnm"

    # system keword
    token_scanner.add_dfa(make_system_dfa("integer", "int"))
    token_scanner.add_dfa(make_system_dfa("float", "float"))
    token_scanner.add_dfa(make_system_dfa("if", "if"))
    token_scanner.add_dfa(make_system_dfa("else", "else"))

    # arthimatic
    arth_dfa = Dfa("arthimatic")
    arth_dfa.set_final_states([1, 2, 11])
    arth_dfa.add_rule(0, 1, "<>")
    arth_dfa.add_rule(1, 2, "=")
    arth_dfa.add_rule(2, 3, "=<>")

    arth_dfa.add_rule(0, 10, "!")
    arth_dfa.add_rule(0, 11, "=")
    arth_dfa.add_rule(10, 11, "=")
    arth_dfa.add_rule(11, 12, "!")

    token_scanner.add_dfa(arth_dfa)

    # arithmatic with one token
    token_scanner.add_dfa(make_single_dfa("plus", "+"))
    token_scanner.add_dfa(make_single_dfa("minus", "-"))
    token_scanner.add_dfa(make_single_dfa("devide", "/"))
    token_scanner.add_dfa(make_single_dfa("mod", "%"))

    # 괄호들
    token_scanner.add_dfa(make_single_dfa("LPAREN", "("))
    token_scanner.add_dfa(make_single_dfa("RPAREN", ")"))
    token_scanner.add_dfa(make_single_dfa("LCURBRACKET", "{"))
    token_scanner.add_dfa(make_single_dfa("RCURBRACKET", "}"))
    token_scanner.add_dfa(make_single_dfa("EQUAL", "="))
    token_scanner.add_dfa(make_single_dfa("SEMICOLON", ";"))

    iden_dfa = Dfa("identifier")
    iden_dfa.set_final_states([1])
    iden_dfa.add_rule(0, 1, char)
    iden_dfa.add_rule(1, 1, digit)
    iden_dfa.add_rule(1, 1, char)
    token_scanner.add_dfa(iden_dfa)

    iden_dfa = Dfa("digits")
    iden_dfa.set_final_states([1])
    iden_dfa.add_rule(0, 1, digit)
    iden_dfa.add_rule(1, 1, digit)
    iden_dfa.add_rule(0, 2, "-")
    iden_dfa.add_rule(2, 1, digit)
    iden_dfa.add_rule(1, 3, ".")
    token_scanner.add_dfa(iden_dfa)

    iden_dfa = Dfa("float")
    iden_dfa.set_final_states([4])
    iden_dfa.add_rule(0, 1, "-")
    iden_dfa.add_rule(1, 2, digit)
    iden_dfa.add_rule(0, 2, digit)
    iden_dfa.add_rule(2, 3, ".")
    iden_dfa.add_rule(3, 4, digit)
    token_scanner.add_dfa(iden_dfa)

    blank = "\n\r "
    blank_dfa = Dfa("blank")
    blank_dfa.set_final_states([1])
    blank_dfa.add_rule(0, 1, blank)
    blank_dfa.add_rule(1, 1, blank)
    token_scanner.add_dfa(blank_dfa)

    quote = '"'
    blank_dfa = Dfa("quote")
    blank_dfa.set_final_states([2])
    blank_dfa.add_rule(0, 1, quote)
    blank_dfa.add_rule(1, 1, digit + char)
    blank_dfa.add_rule(1, 2, quote)
    token_scanner.add_dfa(blank_dfa)

def main(file_path):
    with open(file_path, mode="r") as f:
        literal_list = f.read()

    print(literal_list)

    # 읽어온 Source Code를 Parsing 하기 위해 Token Scanner에 전달합니다.
    token_scanner = TokenScanner(literal_list)

    # Token을 인식하기 위한 dfa를 생성해 token_scanner에 전달해준다.
    set_dfa(token_scanner)

    # Parse 된 Token을 저장하기 위한 list를 생성한다.
    token_list = []

    while True:
        # Token 한개를 Parsing 해본다.
        ret = token_scanner.parse_token()
        # ret이 None이다 -> 파싱 실패 또는 파싱 종료.
        if ret is None:
            if token_scanner.parse_end() is True:
                print("성공")
                # 성공했을 때의 출력
                pprint.pprint(token_list)
                with open(f"{file_path}.out", "w") as f:
                    f.writelines(map(lambda t: f"{t}\n", token_list))
            else:
                end_pos = token_scanner.start_pos
                all_lines = literal_list[0:end_pos + 1];
                line_number = len(all_lines.splitlines());

                literal_list_lines = literal_list.splitlines()
                print(literal_list_lines, literal_list_lines[0:line_number])
                length_line_before = len(''.join(literal_list_lines[0:line_number]))
                print(length_line_before)
                local_pos = end_pos - length_line_before

                str = ""
                str = str + f"error at line number {line_number}, column {local_pos}.\n"

                original_line = literal_list_lines[line_number - 1]
                str = str + f"{original_line}\n"
                print(str)
                with open(f"{file_path}.out", "w") as f:
                    f.write(str)

                pass

            break;

        token_list.append(ret)

        print(ret)

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("plaese pass file path")
        sys.exit()

    file_path = sys.argv[1]

    print("File path : " + file_path)

    main(file_path)

