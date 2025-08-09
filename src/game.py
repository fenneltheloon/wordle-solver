from numpy import random
import sys
import re

from utils import get_project_root

MATCH_RE = r"[a-z]{5}\s+(?:b|y|g){5}\s*\S*"


class Game:
  def __init__(self, weights, first_word=None, words=None):
    if not words:
      with open(get_project_root() / "corpus.txt") as verif_file:
        verif = [a.strip().split() for a in verif_file.readlines()]

      self.words = {}
      for w in verif:
        self.words[w[0]] = int(w[1])
    else:
      self.words = words
    self.full_words = self.words.copy()
    self.guessed_letters = set()
    self.colors = {"black": 5, "yellow": 0, "green": 0}
    self.guessed_words = []
    self.green_letters = [""] * 5
    self.black_letters = set()
    self.generator = random.default_rng()
    self.weights = weights
    self.first_word = first_word

  def print_intro(self):
    self.sort()
    print(f"{len(self.words)} words loaded.")
    print(f'Top word is "{self.word_scores[-1][0]}"')
    print("Welcome to wordle solver. What would you like to do?")
    print("1. View top n words (enter n)")
    print("2. Randomly pick from top n words (enter n)")
    print("3. Produce a list of words that reveal as many unused letters as possible")
    print(
      "Enter 1 n | 2 n | 3 or just enter your first word and result like the following:"
    )
    print("WORDL YBBYG s")
    print("B = black/grey, Y = yellow, G = green")
    print(
      "Including a third term (s) indicates you want a random ordering of remaining words."
    )

  def sort(self):
    # Get freq values for each of the words
    self.letter_freqs = {chr(i + 97): 0 for i in range(26)}
    self.pos_letter_freqs = {chr(i + 97): [0 for _ in range(5)] for i in range(26)}
    word_freq_total = 0
    for word in self.words:
      word_freq_total += self.words[word]
      for lidx, letter in enumerate(word):
        self.letter_freqs[letter] += self.words[word]
        self.pos_letter_freqs[letter][lidx] += self.words[word]
    # Compensate for the 5x increase in frequencies
    for letter in self.letter_freqs:
      self.letter_freqs[letter] /= 5 * word_freq_total
    for letter, idxs in self.pos_letter_freqs.items():
      self.pos_letter_freqs[letter] = list(map(lambda a: a / word_freq_total, idxs))
    word_scores = {}
    for word in self.words:
      # 1 uniq, 2 word freq, 3 positional, 4 global
      uniq_score = len(set(word)) / 5
      word_freq_score = self.words[word] / word_freq_total
      letter_freq_score = sum([self.letter_freqs[letter] for letter in word])
      pos_letter_freq_score = sum(
        [self.pos_letter_freqs[letter][idx] for idx, letter in enumerate(word)]
      )
      word_scores[word] = (
        (
          (self.colors["black"] * self.weights["black"])
          * (uniq_score + letter_freq_score)
          / 2
        )
        + (self.colors["yellow"] * self.weights["yellow"]) * pos_letter_freq_score
        + (self.colors["green"] * self.weights["green"]) * word_freq_score
        + self.weights["word"] * word_freq_score / len(self.words)
      )
    self.word_scores = list(word_scores.items())
    self.word_scores.sort(key=lambda a: a[1])

  def eliminate_letters(self):
    possible_word_scores = {a[0]: a[1] for a in self.word_scores}
    word_scores = {}
    for word in self.full_words:
      if word in self.guessed_words:
        continue
      word_score = 0
      for letter in set(word):
        if letter not in self.guessed_letters:
          for possible_word, pw_score in possible_word_scores.items():
            if letter in possible_word:
              word_score += pw_score
      word_scores[word] = word_score
    self.eliminate_letters_scores = list(word_scores.items())
    self.eliminate_letters_scores.sort(key=lambda a: a[1])

  def eliminate_letters_unweighted(self):
    word_scores = {}
    for word in self.full_words:
      if word in self.guessed_words:
        continue
      word_score = 0
      for letter in set(word):
        if letter not in self.guessed_letters:
          for possible_word in self.word_scores:
            if letter in possible_word[0]:
              word_score += 1
      word_scores[word] = word_score
    self.eliminate_letters_scores = list(word_scores.items())
    self.eliminate_letters_scores.sort(key=lambda a: a[1])

  def get_guess(self):
    try:
      inpt = input("> ").strip().lower()
    except EOFError:
      print()
      print("Thanks for playing!")
      sys.exit()
    ipt = inpt.split()
    if ipt[0].isdigit():
      match int(ipt[0]):
        case 1:
          to_print = self.word_scores[-1 * int(ipt[1]) :]
          for item in to_print:
            print(item)
        case 2:
          slice = self.word_scores[-1 * int(ipt[1]) :]
          # Normalize scores in slice
          total = sum([i[1] for i in slice])
          for i in range(len(slice)):
            slice[i] = [slice[i][0], slice[i][1] / total]
          random_list_words = [a[0] for a in slice]
          random_list_weights = [i[1] for i in slice]
          choice = self.generator.choice(random_list_words, p=random_list_weights)
          print(choice)
        case 3:
          self.eliminate_letters()
          for word in self.eliminate_letters_scores:
            print(word)
        case _:
          sys.stderr.write("Option not supported.\n")
    # Handle a guessed word
    if not re.fullmatch(MATCH_RE, inpt):
      sys.stderr.write("Input does not match expected value.\n")
      return None
    return ipt

  def play(self):
    while True:
      ipt = self.get_guess()
      if ipt is None:
        continue
      if ipt[1] == "ggggg":
        return (ipt[0], len(self.guessed_words) + 1)
      # Valid input
      self.guessed_words.append(ipt[0])
      yellow_letters = []
      self.green_letters = [""] * 5

      self.colors = {"black": 0, "yellow": 0, "green": 0}
      for position, (letter, color) in enumerate(zip(ipt[0], ipt[1])):
        self.guessed_letters.add(letter)
        match color:
          case "b":
            self.black_letters.add(letter)
            self.colors["black"] += 1
          case "y":
            yellow_letters.append((letter, position))
            self.colors["yellow"] += 1
          case "g":
            self.green_letters[position] = letter
            self.colors["green"] += 1

      for word in self.words.copy():
        if word in self.guessed_words:
          del self.words[word]
          continue
        if not self.verif(yellow_letters, word):
          del self.words[word]
          continue
      if len(self.words) < 1:
        return (None, None)
      if len(self.words) == 1:
        correct = list(self.words)[0]
        return (correct, len(self.guessed_words) + 1)
      # Need to score and resort
      # Factors to consider:
      # - How many blacks, yellows, greens in the current word
      #   Just convert to percentages and weight them accordingly?
      #   Black is global letter + uniqs, yellow is positional, green is popularity
      # - How many words left in the word list

      self.sort()
      self.eliminate_letters()
      if len(ipt) > 2:
        just_words = [a[0] for a in self.word_scores]
        just_weights = [a[1] for a in self.word_scores]
        just_weights = [i / sum(just_weights) for i in just_weights]
        random_list = self.generator.choice(
          just_words, p=just_weights, size=len(just_words), replace=False
        )
        random_list = list(random_list)
        random_list.reverse()
        for possible in random_list:
          print(possible)
        print()
      else:
        filter_list = []
        for item in self.eliminate_letters_scores.copy():
          if item[0] in self.words:
            filter_list.append(item)
        delta = len(self.word_scores) - len(filter_list)
        if delta > 0:
          for i in range(delta):
            filter_list.insert(0, "")
        for possible, elim, filter in zip(
          self.word_scores,
          self.eliminate_letters_scores[-len(self.word_scores) :],
          filter_list,
        ):
          print(possible, elim, filter)
        print()

  # def guess_result(self, guess):
  #   assert self.given_word is not None
  #   result = ""
  #   actual = [i for i in self.given_word]
  #   for idx, letter in enumerate(guess):
  #     if letter == self.given_word[idx]:
  #       result += "g"
  #       actual[idx] = ""
  #       continue
  #     if letter in actual:
  #       inde = actual.index(letter)
  #       result += "y"
  #       actual[inde] = ""
  #       continue
  #     result += "b"
  #   return result

  def verif(self, yellow, word):
    word = [i for i in word]
    for idx, letter in enumerate(self.green_letters):
      if letter != "":
        if letter != word[idx]:
          return False
        word[idx] = ""
    for letter, lpos in yellow:
      if letter == word[lpos]:
        return False
      early_ret = True
      for lid, letr in enumerate(word):
        if letr == letter and (letr, lid) not in yellow:
          word[lid] = ""
          early_ret = False
          break
      if early_ret:
        return False
    for letter in self.black_letters:
      if letter in word:
        return False
    return True

  def play_benchmark_best_weighted(self, given_word):
    while True:
      self.sort()
      if self.word_scores[-1][0] == given_word:
        return len(self.guessed_words) + 1
      self.guessed_words.append(self.word_scores[-1][0])
      yellow_letters = []
      given_word_array = [i for i in given_word]
      for position, letter in enumerate(self.word_scores[-1][0]):
        # Figure out what color it's supposed to be
        # Green
        if letter == given_word_array[position]:
          self.green_letters[position] = letter
          self.colors["green"] += 1
          given_word_array[position] = " "
          continue
      for position, letter in enumerate(self.word_scores[-1][0]):
        # Yellow
        if letter in given_word_array:
          yellow_letters.append((letter, position))
          self.colors["yellow"] += 1
          given_word_array[given_word_array.index(letter)] = " "
        # Black
        else:
          self.black_letters.add(letter)
          self.colors["black"] += 1
      # Remove words from list
      for word in self.words.copy():
        if word in self.guessed_words:
          del self.words[word]
          continue
        if not self.verif(yellow_letters, word):
          del self.words[word]
          continue
      if len(self.words) < 1:
        print(given_word + " did not work: " + self.guessed_words)
        return None
      if len(self.words) == 1:
        return len(self.guessed_words) + 1

  def play_benchmark_elim_letters(self, given_word):
    NUM_TO_SOLVE = 6
    # breakpoint()
    while True:
      if len(self.guessed_words) == 0 and self.first_word is not None:
        guessed_word = self.first_word
      else:
        use_weight_list = len(self.words) == 1
        self.sort()
        if not use_weight_list:
          self.eliminate_letters()
        if self.word_scores[-1][0] == given_word and use_weight_list:
          return len(self.guessed_words) + 1
        if use_weight_list:
          guessed_word = self.word_scores[-1][0]
        else:
          guessed_word = self.eliminate_letters_scores[-1][0]
      self.guessed_words.append(guessed_word)
      yellow_letters = []
      given_word_array = [i for i in given_word]
      for position, letter in enumerate(guessed_word):
        # Figure out what color it's supposed to be
        # Green
        if letter == given_word_array[position]:
          self.green_letters[position] = letter
          self.colors["green"] += 1
          given_word_array[position] = " "
          continue
      for position, letter in enumerate(guessed_word):
        # Yellow
        if letter in given_word_array:
          yellow_letters.append((letter, position))
          self.colors["yellow"] += 1
          given_word_array[given_word_array.index(letter)] = " "
        # Black
        else:
          self.black_letters.add(letter)
          self.colors["black"] += 1
      # Remove words from list
      for word in self.words.copy():
        if word in self.guessed_words:
          del self.words[word]
          continue
        if not self.verif(yellow_letters, word):
          del self.words[word]
          continue
      if len(self.words) < 1:
        print(given_word + " did not work: " + self.guessed_words)
        return None
      if len(self.words) == 1:
        return len(self.guessed_words) + 1
