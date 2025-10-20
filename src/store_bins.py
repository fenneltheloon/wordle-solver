from game import Game

g = Game()
g.sort_bins()

with open("first_word_list.txt", "w") as f:
  f.write(str(g.word_scores))
