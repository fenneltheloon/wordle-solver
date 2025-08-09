from nltk.corpus import webtext
from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk import pos_tag
from nltk import FreqDist
from collections import defaultdict
import nltk

from utils import get_project_root


# Returns true if the values in the checklist all exist in the denylist
def only_denylist(checklist, denylist):
  for word in checklist:
    if word not in denylist:
      return False
  return True


def single_denylist(checklist, denylist):
  for word in checklist:
    if word in denylist:
      return False
  return True


with open("/usr/share/dict/american-english", "r") as dictionary:
  dictionary = dictionary.readlines()

dictionary = [i.strip().lower() for i in dictionary]

pos_lists = defaultdict(set)
verif_list = set()
final_list = []
bad_tags = ["NNS", "NNPS", "NNP", "VBD", "VBN"]
proper_noun_tags = ["NNPS", "NNP"]

for file in webtext.fileids():
  words = webtext.words(file)
  pos_tags = pos_tag(words)
  for word, tag in pos_tags:
    pos_lists[word.lower()].add(tag)
for word, tag in brown.tagged_words():
  pos_lists[word.lower()].add(tag)
for file in gutenberg.fileids():
  words = gutenberg.words(file)
  pos_tags = pos_tag(words)
  for word, tag in pos_tags:
    pos_lists[word.lower()].add(tag)
pos_tags = pos_tag(dictionary)
for word, tag in pos_tags:
  pos_lists[word.lower()].add(tag)
for word, tag in pos_tag(nltk.corpus.words.words()):
  pos_lists[word.lower()].add(tag)

for word, tags in pos_lists.items():
  if not word.isalpha():
    continue
  if len(word) != 5:
    continue
  if not word.isascii():
    continue
  if word not in dictionary:
    continue
  # Remove proper nouns
  if only_denylist(tags, proper_noun_tags):
    continue
  # Looking for words that end in "S", "ES", "ED"
  # Remove regular plurals and past tenses
  if (word[-1] == "s" or word[-2:] == "ed") and single_denylist(tags, bad_tags):
    continue
  verif_list.add(word)

webtext_freq_dist = FreqDist(webtext.words())
gutenberg_freq_dist = FreqDist(gutenberg.words())
brown_freq_dist = FreqDist(brown.words())
for word in verif_list:
  final_list.append(
    word
    + "\t"
    + str(
      webtext_freq_dist[word] + gutenberg_freq_dist[word] + brown_freq_dist[word] + 1
    )
    + "\n"
  )

with open(get_project_root() / "corpus.txt", "w") as output:
  output.writelines(final_list)
