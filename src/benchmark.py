# Benchmark file
# Run an instance of the wordle solver on all possible wordle sols
from game import Game

from itertools import repeat
from multiprocessing import Pool
from utils import get_project_root
import numpy
import gc
from tqdm import tqdm
from collections import defaultdict
from math import inf
from scipy.optimize import OptimizeResult, minimize

GRANULARITY = 5


def run_game(args):
  weights, sol_word, wordlist, first_word = args
  game = Game(weights=weights, words=wordlist, first_word=first_word)
  sol_len = game.play_benchmark_best_weighted(sol_word)
  del game
  return [sol_word, sol_len, weights]


# Currently not in use
def result_call(result, scores, lock, progbar=None):
  with lock:
    scores[str(result[2])] += result[1]
    if progbar is not None:
      progbar.write(str(result))
      progbar.write(f"wordlist len: {len(wordlist)}")
      progbar.update(1)


def run_wordlist(weights, progbar=None):
  with open(get_project_root() / "corpus.txt") as verif_file:
    verif = [a.strip().split() for a in verif_file.readlines()]

  words = {}
  for w in verif:
    words[w[0]] = int(w[1])

  g = Game(weights)
  g.sort()
  g.eliminate_letters()
  first_word = g.eliminate_letters_scores[-1][0]
  del g
  wordlist_len = len(wordlist)
  input_iter = zip(
    repeat(weights, wordlist_len),
    wordlist,
    repeat(words, wordlist_len),
    repeat(first_word, wordlist_len),
  )
  total = 0
  with Pool() as p:
    progbar = tqdm(
      p.imap_unordered(
        run_game,
        input_iter,
      ),
      total=len(wordlist),
    )
    for result in progbar:
      progbar.write(str(result))
      total += result[1]
  avg_solve = total / len(wordlist)
  # for word in wordlist:
  #   pool.apply_async(
  #     run_game,
  #     args=[
  #       weights,
  #       word,
  #     ],
  #     kwds={"wordlist": words, "first_word": first_word},
  #     callback=lambda a: result_call(a, scores, lock, progbar),
  #   )
  # pool.close()
  # pool.join()
  # breakpoint()
  # avg_solve = scores[str(weights)] / len(wordlist)
  if progbar:
    progbar.write(str(weights))
    progbar.write(str(avg_solve))
  else:
    print(weights)
    print(avg_solve)
  return avg_solve, weights


# Not in use right now
def param_space_search():
  black_weight_values = numpy.linspace(0.5, 1.5, GRANULARITY, endpoint=True)
  green_weight_values = numpy.linspace(-1 / 3, 2 / 3, GRANULARITY, endpoint=True)
  yellow_weight_values = numpy.linspace(-1 / 3, 2 / 3, GRANULARITY, endpoint=True)
  word_weight_values = numpy.linspace(-1.5, 0, GRANULARITY, endpoint=True)
  progbar = tqdm(total=GRANULARITY**4 * len(wordlist))
  minimum = (inf, None)
  # lock = Lock()
  scores = defaultdict(int)

  for black_w in black_weight_values:
    for green_w in green_weight_values:
      for yellow_w in yellow_weight_values:
        for word_w in word_weight_values:
          weights = {
            "black": black_w,
            "green": green_w,
            "yellow": yellow_w,
            "word": word_w,
          }
          result = run_wordlist(lock, weights, progbar)
          if minimum[0] > result[0]:
            minimum = result

  print(minimum)


def grad_desc_callback(intermediate_result: OptimizeResult):
  print(intermediate_result.fun, intermediate_result.x)


def grad_desc():
  init_weights = [5.22639492, 2.12096432, 1.40157567, -2.82829539]
  # lock = Lock()
  ret: OptimizeResult = minimize(
    lambda x: run_wordlist(
      weights={"black": x[0], "green": x[1], "yellow": x[2], "word": x[3]},
    )[0],
    init_weights,
    callback=grad_desc_callback,
    method="nelder-mead",
    options={"disp": True, "adaptive": True, "fatol": 0},
  )
  print(ret.fun, ret.x)


if __name__ == "__main__":
  with open(get_project_root() / "all_wordle_answers_2025_08_15.txt") as input:
    input = input.readlines()
    wordlist = [i.strip().lower() for i in input]
  grad_desc()
  # lock = Lock()
  # weights = {
  #   "black": 4.950368945938928,
  #   "green": 2.1625415028158764,
  #   "yellow": 1.420023668400915,
  #   "word": -2.745717732166203,
  # }
  # print(run_wordlist(lock, weights))

  # with open(get_project_root() / "corpus.txt") as verif_file:
  #   verif = [a.strip().split() for a in verif_file.readlines()]

  # words = {}
  # for w in verif:
  #   words[w[0]] = int(w[1])
  # g = Game(weights)
  # g.sort()
  # g.eliminate_letters()
  # first_word = g.eliminate_letters_scores[-1][0]
  # del g
  # print(g.play_benchmark_best_weighted("tripe"))
