'''
Ghalia Abu Nowar
CS5100
Project

This is the main driver
'''
# import screen display class
from Screen import *

def main():
    game_grid = Grid()
    app = GameUI(game_grid)
    app.start()

if __name__ == '__main__':
    main()
