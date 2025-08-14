from game import Game

weights = {
  "black": 5.22639492,
  "green": 2.12096432,
  "yellow": 1.40157567,
  "word": -2.82829539,
}
game = Game(weights)
game.print_intro()
(correct_word, guesses) = game.play()
if correct_word:
  print(f"Wordle solved in {guesses}: {correct_word}")
else:
  print("Can't find a word :<")
