import csv

input = open("../unigram_freq.csv", "r")
reader = csv.reader(input)

with open("../trim_5_words.csv", "w", newline="") as output:
    writer = csv.writer(output)

    for row in reader:
        if len(row[0]) == 5:
            writer.writerow(row)

input.close()
