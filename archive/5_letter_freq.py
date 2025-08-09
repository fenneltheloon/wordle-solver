import csv

freqs = [[0 for _ in range(5)] for _ in range(26)]
norm_freqs = [[0 for _ in range(5)] for _ in range(26)]

with (
    open("../dict_5_words.csv", "r") as input,
    open("../letter_freq.csv", "w") as output,
):
    i = csv.reader(input)
    o = csv.writer(output)

    for line in i:
        line[1] = int(line[1])
        for idx, letter in enumerate(line[0]):
            v = ord(letter) - 97
            assert v >= 0 and v < 26
            freqs[v][idx] += line[1]

    # Normalize for each index
    for idx in range(5):
        total = 0
        for letter in freqs:
            total += letter[idx]
        for lidx, letter in enumerate(freqs):
            norm_freqs[lidx][idx] = letter[idx] / total

    for c in range(26):
        for idx in range(5):
            o.writerow([chr(c + 97), str(idx + 1), str(norm_freqs[c][idx])])
