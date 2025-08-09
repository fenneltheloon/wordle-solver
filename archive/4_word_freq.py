import csv

with (
    open("../dict_5_words.csv", "r") as input,
):
    reader = csv.reader(input)
    total = 0
    for row in reader:
        total += int(row[1])

with (
    open("../dict_5_words.csv", "r") as input,
    open("../dict_5_words_norm.csv", "w") as output,
):
    reader = csv.reader(input)
    writer = csv.writer(output)
    for row in reader:
        writer.writerow([row[0], str(int(row[1]) / total)])
