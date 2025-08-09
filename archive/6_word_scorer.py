# Need to create way to assign a score to each of the words
#
# Depends on:
# - Number of unique letters in word (N)
# - Popularity/frequency of word (F)
# - Frequency of each letter (R)
# - frequency of each letter in each position (P)
#
# Score = w1*N + w2*F + w3*R + w4*P
#
# P = sum(letter frequency at index) over the entire word

import csv
from collections import defaultdict


word_dict = {}
word_score_dict = {}
with open("../dict_5_words_norm.csv", "r") as word_freq:
    reader = csv.reader(word_freq)
    for row in reader:
        word_dict[row[0]] = float(row[1])

letter_dict = defaultdict(lambda: [0 for _ in range(5)])
with open("../letter_freq.csv", "r") as letter_freq:
    reader = csv.reader(letter_freq)
    for row in reader:
        letter_dict[row[0]][int(row[1]) - 1] = float(row[2])

# Calculate score for each word
for word in word_dict:
    nn = len(set(word))
    ff = float(word_dict[word])
    pp = 0
    for idx, letter in enumerate(word):
        pp += letter_dict[letter][idx]
    pp *= 5
    word_score = nn + ff + pp
    word_score_dict[word] = word_score

word_score_list = [(k, v) for k, v in word_score_dict.items()]
word_score_list.sort(key=lambda a: a[1])
word_score_list.reverse()

with open("../word_scores.csv", "w") as output:
    writer = csv.writer(output)
    writer.writerows(word_score_list)
