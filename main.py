import game

WIDTH = 1600
HEIGHT = 900
ONE_PIXEL = 10
FPS = 30

my_game = game.Game(int(WIDTH/ONE_PIXEL),int(HEIGHT/ONE_PIXEL), FPS, ONE_PIXEL)
my_game.start_game()
