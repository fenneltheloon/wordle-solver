import csv
import nltk
import utils

root = utils.get_project_root()
with open(root / "unigram_freq.csv", "r") as input:
  reader = csv.reader(input)
  trim_5_words = []

  for row in reader:
    if len(row[0]) == 5:
      trim_5_words.append(row)

with open(root / "english.txt", "r") as input:
  english_5 = []
  for line in input:
    line = line.strip()
    if len(line) == 5 and line.isalpha():
      english_5.append(line.lower())

dict_5_words = []
total = 0
for line in trim_5_words:
  line[1] = int(line[1])
  if line[0] in english_5 and line[0]:
    total += line[1]
    dict_5_words.append(line)
for line in dict_5_words:
  line[1] /= total

word_list = [
  [line[0], len(set(line[0])) / 5, line[1], 0, 0, 0] for line in dict_5_words
]

with open("../word_scores.csv", "w") as output:
  writer = csv.writer(output)
  writer.writerows(word_list)
