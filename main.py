import sys
from classes import *
import pprint
import os

# system keword 에 대한 dfa를 자동생성한다.
def make_system_dfa(name, keyword):
    digit = "1234567890"
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

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
    nz = "123456789"
    digit = "1234567890"
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # system keword (Keyword stmt)
    stmt_dfa = Dfa("Keyword stmt")
    stmt_dfa.set_final_states([2, 6, 11, 14, 20])
    stmt_dfa.add_rule(0, 1, "i")
    stmt_dfa.add_rule(1, 2, "f")

    stmt_dfa.add_rule(0, 3, "e")
    stmt_dfa.add_rule(3, 4, "l")
    stmt_dfa.add_rule(4, 5, "s")
    stmt_dfa.add_rule(5, 6, "e")

    stmt_dfa.add_rule(0, 7, "w")
    stmt_dfa.add_rule(7, 8, "h")
    stmt_dfa.add_rule(8, 9, "i")
    stmt_dfa.add_rule(9, 10, "l")
    stmt_dfa.add_rule(10, 11, "e")

    stmt_dfa.add_rule(0, 12, "f")
    stmt_dfa.add_rule(12, 13, "o")
    stmt_dfa.add_rule(13, 14, "r")

    stmt_dfa.add_rule(0, 15, "r")
    stmt_dfa.add_rule(15, 16, "e")
    stmt_dfa.add_rule(16, 17, "t")
    stmt_dfa.add_rule(17, 18, "u")
    stmt_dfa.add_rule(18, 19, "r")
    stmt_dfa.add_rule(19, 20, "n")
    token_scanner.add_dfa(stmt_dfa)


    # system keword (Vtype)
    vtype_dfa = Dfa("Vtype")
    vtype_dfa.set_final_states([3, 7, 11, 14, 19])
    vtype_dfa.add_rule(0, 1, "i")
    vtype_dfa.add_rule(1, 2, "n")
    vtype_dfa.add_rule(2, 3, "t")

    vtype_dfa.add_rule(0, 4, "c")
    vtype_dfa.add_rule(4, 5, "h")
    vtype_dfa.add_rule(5, 6, "a")
    vtype_dfa.add_rule(6, 7, "r")

    vtype_dfa.add_rule(0, 8, "b")
    vtype_dfa.add_rule(9, 9, "o")
    vtype_dfa.add_rule(9, 10, "o")
    vtype_dfa.add_rule(10, 11, "l")
    vtype_dfa.add_rule(11, 12, "e")
    vtype_dfa.add_rule(12, 13, "a")
    vtype_dfa.add_rule(13, 14, "n")

    vtype_dfa.add_rule(0, 15, "f")
    vtype_dfa.add_rule(15, 16, "l")
    vtype_dfa.add_rule(16, 17, "o")
    vtype_dfa.add_rule(17, 18, "a")
    vtype_dfa.add_rule(18, 19, "t")
    token_scanner.add_dfa(vtype_dfa)


    # arthimatic operators
    arth_dfa = Dfa("Arthimatic operator")
    arth_dfa.set_final_states([1])
    arth_dfa.add_rule(0, 1, "-")
    arth_dfa.add_rule(0, 1, "+")
    arth_dfa.add_rule(0, 1, "*")
    arth_dfa.add_rule(0, 1, "/")
    token_scanner.add_dfa(arth_dfa)

    # bitwise operators
    bit_dfa = Dfa("Bitwise operator")
    bit_dfa.set_final_states([2, 4, 5, 6])
    bit_dfa.add_rule(0, 1, "<")
    bit_dfa.add_rule(1, 2, "<")
    bit_dfa.add_rule(0, 3, ">")
    bit_dfa.add_rule(3, 4, ">")
    bit_dfa.add_rule(0, 5, "&")
    bit_dfa.add_rule(0, 6, "|")
    token_scanner.add_dfa(bit_dfa)

    # comparison operators
    comp_dfa = Dfa("Comparison operator")
    comp_dfa.set_final_states([2, 4, 6, 8])
    comp_dfa.add_rule(0, 1, "<")
    comp_dfa.add_rule(1, 2, "=")
    comp_dfa.add_rule(0, 3, ">")
    comp_dfa.add_rule(3, 4, "=")
    comp_dfa.add_rule(0, 5, "=")
    comp_dfa.add_rule(5, 6, "=")
    comp_dfa.add_rule(0, 7, "!")
    comp_dfa.add_rule(7, 8, "=")
    token_scanner.add_dfa(comp_dfa)

    # whites space
    ws_dfa = Dfa("WHITE SPACE")
    ws_dfa.set_final_states([1])
    ws_dfa.add_rule(0, 1, "\t")
    ws_dfa.add_rule(0, 1, "\n")
    ws_dfa.add_rule(0, 1, " ")
    ws_dfa.add_rule(1, 1, "\t")
    ws_dfa.add_rule(1, 1, "\n")
    ws_dfa.add_rule(1, 1, " ")
    token_scanner.add_dfa(ws_dfa)

    #assign
    token_scanner.add_dfa(make_single_dfa("Assign", "="))

    #semicolon
    semi_dfa = Dfa("Semicolon")
    semi_dfa.set_final_states([1])
    semi_dfa.add_rule(0, 1, ";")
    token_scanner.add_dfa(semi_dfa)

    # brackets
    token_scanner.add_dfa(make_single_dfa("LPAREN", "("))
    token_scanner.add_dfa(make_single_dfa("RPAREN", ")"))
    token_scanner.add_dfa(make_single_dfa("LCURBRACKET", "{"))
    token_scanner.add_dfa(make_single_dfa("RCURBRACKET", "}"))

    # comma
    token_scanner.add_dfa(make_single_dfa("COMMA", ","))

    # integer
    integer_dfa = Dfa("Integer")
    integer_dfa.set_final_states([1, 3])
    integer_dfa.add_rule(0, 1, "0")
    integer_dfa.add_rule(0, 2, "-")
    integer_dfa.add_rule(0, 3, nz)
    integer_dfa.add_rule(2, 3, nz)
    integer_dfa.add_rule(3, 3, digit)
    token_scanner.add_dfa(integer_dfa)

    # literal
    literal_dfa = Dfa("Literal")
    literal_dfa.set_final_states([2])
    literal_dfa.add_rule(0, 1, "\"")
    literal_dfa.add_rule(1, 1, digit)
    literal_dfa.add_rule(1, 1, char)
    literal_dfa.add_rule(1, 1, " ")
    literal_dfa.add_rule(1, 2, "\"")
    token_scanner.add_dfa(literal_dfa)

    # boolean
    bool_dfa = Dfa("Boolean")
    bool_dfa.set_final_states([4, 9])
    literal_dfa.add_rule(0, 1, "t")
    literal_dfa.add_rule(1, 2, "r")
    literal_dfa.add_rule(2, 3, "u")
    literal_dfa.add_rule(3, 4, "e")

    literal_dfa.add_rule(0, 5, "f")
    literal_dfa.add_rule(5, 6, "a")
    literal_dfa.add_rule(6, 7, "l")
    literal_dfa.add_rule(7, 8, "s")
    literal_dfa.add_rule(8, 9, "e")
    token_scanner.add_dfa(literal_dfa)

    #float
    float_dfa = Dfa("Float")
    float_dfa.set_final_states([5])
    float_dfa.add_rule(0, 1, "-")
    float_dfa.add_rule(0, 2, nz)
    float_dfa.add_rule(0, 3, "0")
    float_dfa.add_rule(1, 2, nz)
    float_dfa.add_rule(1, 3, "0")
    float_dfa.add_rule(2, 2, digit)
    float_dfa.add_rule(2, 4, ".")
    float_dfa.add_rule(3, 4, ".")
    float_dfa.add_rule(4, 5, digit)
    float_dfa.add_rule(5, 5, nz)
    float_dfa.add_rule(5, 6, "0")
    float_dfa.add_rule(6, 5, nz)
    float_dfa.add_rule(6, 6, "0")
    token_scanner.add_dfa(float_dfa)

    #id
    id_dfa = Dfa("ID")
    id_dfa.set_final_states([1])
    id_dfa.add_rule(0, 1, char)
    id_dfa.add_rule(0, 1, "_")
    id_dfa.add_rule(1, 1, char)
    id_dfa.add_rule(1, 1, "_")
    id_dfa.add_rule(1, 1, digit)
    token_scanner.add_dfa(id_dfa)

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
                all_lines = literal_list[0:end_pos + 1]
                line_number = len(all_lines.splitlines())

                literal_list_lines = literal_list.splitlines(keepends=True)
                print(literal_list_lines, literal_list_lines[0:line_number])
                length_line_before = len(''.join(literal_list_lines[0:line_number - 1]))
                print(length_line_before)
                local_pos = end_pos - length_line_before + 1
                print(f"local_pos {local_pos} = end_pos {end_pos} - {length_line_before} + 1")

                str = ""
                str = str + f"error at line number {line_number}, column {local_pos}.\n\n"

                original_line = literal_list_lines[line_number - 1]
                str = str + f"{original_line}\n"

                print(str)
                with open(f"{file_path}.out", "w") as f:
                    f.write(str)

                pass

            break

        token_list.append(ret)

        if len(token_list) > 1 \
            and (token_list[-1][0] in ["Integer", "Float"] and "-" in token_list[-1][1]):
            print(1)
            # 그 이전에 Number 가 바로 나오면 쪼갠다
            # 그렇지 않으면 유지
            finding_token = None
            for i in range(len(token_list) - 1, 0, -1):
                i = i - 1 # range 반복 값 보정.
                # 블랭크는 제외하고 찾는다.
                if token_list[i][0] == "WHITE SPACE":
                    continue

                finding_token = token_list[i]
                break

            if finding_token[0] in ["Integer", "Float", "ID"]:
                print(f"split {token_list[-1]}")
                token_list[-1] = (token_list[-1][0], token_list[-1][1].replace("-", ""))
                token_list.insert(-1, ("Arthimatic operator", "-"))

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("plaese pass file path")
        sys.exit()

    file_path = sys.argv[1]

    print("File path : " + file_path)

    main(file_path)

