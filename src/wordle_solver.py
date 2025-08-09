from game import Game

weights = {
  "black": 4.950368945938928,
  "green": 2.1625415028158764,
  "yellow": 1.420023668400915,
  "word": -2.745717732166203,
}
game = Game(weights)
game.print_intro()
(correct_word, guesses) = game.play()
if correct_word:
  print(f"Wordle solved in {guesses}: {correct_word}")
else:
  print("Can't find a word :<")
