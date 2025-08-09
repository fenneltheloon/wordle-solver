from pathlib import Path


def get_project_root() -> Path:
  return Path(__file__).parent.parent


def unknown_sort(list, used_letters):
  list = freq_scores(list)
  scored_list = []
  totals = [0 for _ in range(26)]
  for word in list:
    for letter in word[0]:
      totals[ord(letter) - 97] += 1
  letter_freqs = [a / sum(totals) for a in totals]
  for word in list:
    score = 0
    for letter in set(word[0]):
      if letter not in used_letters:
        score += letter_freqs[ord(letter) - 97]
    scored_list.append(word[:5])
    scored_list[-1].append(score)
  scored_list.sort(key=lambda a: a[5])
  return scored_list


def known_sort(word_list, nums):
  word_list = freq_scores(word_list)
  for val in word_list:
    val[5] = (
      (nums[0] * 0.67) * (val[1] + val[4]) / 2
      + (nums[1] * 1.5) * val[3]
      + (nums[2] * 2) * val[2]
      + 10 * val[2] / len(word_list)
    )
  word_list.sort(key=lambda a: a[5])
  return word_list


def freq_scores(word_list):
  freq_table = [0 for _ in range(26)]
  pos_freq_table = [[0 for _ in range(5)] for _ in range(26)]
  for word in word_list:
    for idx, letter in enumerate(word[0]):
      o = ord(letter) - 97
      freq_table[o] += word[2]
      pos_freq_table[o][idx] += word[2]
  for word in word_list:
    # Positional 3, global 4
    word[3] = 0
    word[4] = 0
    for idx, letter in enumerate(word[0]):
      o = ord(letter) - 97
      word[4] += freq_table[o]
      word[3] += pos_freq_table[o][idx]
  # Normalize
  global_total = sum([a[4] for a in word_list])
  positional_total = sum([a[3] for a in word_list])
  word_list = [
    [a[0], a[1], a[2], a[3] / positional_total, a[4] / global_total, a[5]]
    for a in word_list
  ]
  return word_list
