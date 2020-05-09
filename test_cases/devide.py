with open("a.txt", mode="r") as f:
    lines = f.readlines()
    count = 0
    for line in lines:
        count = count + 1
        line = line.replace("\n", "")
        with open(f"testcase_{count}", mode="w") as lf:
            lf.write(line)

