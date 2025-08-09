with open("../english.txt", "r") as input, open("../english_5.txt", "w") as output:
    for line in input:
        # Including the newline
        if len(line) == 6 and line.strip().isalpha():
            output.write(line.lower())
