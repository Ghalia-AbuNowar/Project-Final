'''
    Ghalia Abu Nowar
    CS5100 project
    This is the game logic file
'''
# import random libary
from cmath import exp
from email.mime import base
from math import log
import numpy as np
import random
from copy import deepcopy


class Grid:
    '''
    This class creats a Grid object that has the following properties
    1) self.size, this is the size of the matrix
    2) self.score, this is set to zero and represents the score of
       the game
    3) self.matrix, this is the array representing the game board
       it's a (self.size X self.size) matrix and is set as an all zero
       matrix
       

    '''
    def __init__(self, size = 4):
        '''
            Attributes:
            1) self.size, this is the size of the matrix
            2) self.score, this is set to zero and represents the score of
               the game
            3) self.matrix, this is the array representing the game board
               it's a (self.size X self.size) matrix and is set as an all zero
               matrix
               
        parameters:
            size(int): (optional parameter)This represents
            the AxA matrix            
        '''
        self.size = size
        self.score = 0
        # Initialize a size x size grid of zeros using NumPy
        self.matrix = np.zeros((size, size), dtype=int)
        self.max_tile = 0
        self.prev_Score = 0
        self.pattern = self.generate_snake_pattern()

    def get_size(self):
        '''
        This methode takes no parameters and returns the value of
        the self.size property of current instance of object

        Return(list/int): self.size attribute
        '''
        
        return self.size
    
    def get_matrix(self):
        '''
        This methode takes no parameters and returns the value of
        the self.matrix attribute
        '''
        
        return self.matrix

    def get_score(self):
        '''
        This methode takes no parameters and returns the value of
        the self.score attribute
        '''
        return self.score
    

    def get_score_diff(self):
        '''
        This methode takes no parameters and returns the value of
        the self.score attribute
        '''
        return self.score - self.prev_Score

        
    def add_value(self):
        # Choose a random empty position
        empty_positions = np.argwhere(self.matrix == 0)
        if empty_positions.size == 0:
            raise ValueError('No more empty tiles')
        x, y = empty_positions[random.randint(0, len(empty_positions) - 1)]
        
        # randomly generate a tile
        self.matrix[x, y] = np.random.choice([2, 4], p=[0.9, 0.1])
        self.max_tile = max(self.max_tile, self.matrix[x,y])

    def start_game(self):
        '''
        This method calls the add_value methode twice
        i.e. it assigns two random values to self.matrix property of
        the current Grid object
        '''
        
        self.add_value()
        self.add_value()



    def compress(self):
        '''
        This methode is responisble for 'compressing' all non zero
        values of the self.matrix property to the utmost left
        '''
        
        # creat a new Grid object
        new = Grid(self.size)
        
        for i in range(self.size):
            index = 0
            for j in range(self.size):
                # if the cell in the matrix is not zero append the value
                # to the new Grid object 
                if self.matrix[i][j] != 0:
                    new.matrix[i][index] = self.matrix[i][j]
                    index = index + 1
        
        self.matrix = new.matrix                

    def merge(self):
        '''
        This methode is responsible for combining two similar connsecetive
        (row wise)values in the self.matrix

        parameters: None
        Returns:
            change(Boolen): this indicates wheather any two values were merged
                            in the self.matrix property
                            - True: if two values were merged
                            -False: no merging happened
        '''
        self.prev_Score = self.score
        change = False
        for i in range(self.size):
            for j in range(1, self.size):
                # if two consective values are non zero combine the values
                if self.matrix[i][j] == self.matrix[i][j - 1]\
                   and self.matrix[i][j] != 0:
                    self.matrix[i][j - 1] = self.matrix[i][j - 1] * 2
                    self.matrix[i][j] = 0
                    # increase the self.score property 
                    self.score = self.score + self.matrix[i][j - 1]
                    self.max_tile = max(self.max_tile, self.matrix[i][j - 1])
                    change = True
        return change

    def flip(self):
        '''
        This methode rearranges the self.matrix values from left-right
        to right-left
        '''
        
        self.matrix = np.fliplr(self.matrix)

    def transpose(self):
        '''
        This methode flips the rows and coloums of the self.matrix
        '''
        self.matrix = self.matrix.T
        
    def shift_left(self):
        '''
        This methode is responsible for compressing and merging the
        cells to the left
        '''

        original = deepcopy(self)

        # first shift and merge
        self.compress()
        merge = self.merge()
        # if the return value for the merge is True then call compress methode again
        if merge is True:
            self.compress()
        
        # check if there is change
        if self.grid_change(original):
            self.add_value()


    def shift_right(self):
        '''
        This methode is responsible for compressing and merging the
        cells to the right
        '''
  
        self.flip()
        self.shift_left()
        self.flip()


    def shift_up(self):
        '''
        This methode is responsible for compressing and merging the
        cells up
        '''

        self.transpose()
        self.shift_left()
        self.transpose()
        


    def shift_down(self):
        '''
        This methode is responsible for compressing and merging the
        cells down
        '''
     
        self.transpose()
        self.flip()
        self.shift_left()
        self.flip()
        self.transpose()



    def grid_change(self, other):
        '''
        This method checks if there are any changes between the current grid
        and another grid.

        Parameters:
            other (Grid object): The grid to compare against.

        Returns:
            bool: True if there is a change, False otherwise.
        '''


        # Iterate through each cell to compare values
        for i in range(self.size):
            for j in range(self.size):
                # Found a cell that is different
                if self.matrix[i][j] != other.matrix[i][j]:
                    return True  

        # No differences found, return False
        return False
        # raise Exception('Not a valid move.') 
        
    def get_max_value(self):
        return self.max_tile

    def is_gameover(self):
        '''
        This method check if the game has been won, lost, or still ongoing.

        Return:
            Booleen:
            -'YOU WON'(str): if one of matrix cells == 2048

            - 'GAME OVER'(str): if shift_left, shift_right
            shift_up, shift_down does not change anything in matrix
                  
            -False(Boolen): if game there is zero value left in the self.matrix
            or if the methodes: shift_left, shift_right, shift_up shift_down
            do not change the matrix
        '''
  
        # Check for any empty spaces
        if np.any(self.matrix == 0):
            return False

        # Check for possible merges in rows and columns
        for i in range(self.size):
            for j in range(self.size - 1):  # Check horizontally, avoiding index out of bounds
                if self.matrix[i, j] == self.matrix[i, j + 1]:
                    return False

            for j in range(self.size - 1):  # Check vertically, avoiding index out of bounds
                if self.matrix[j, i] == self.matrix[j + 1, i]:
                    return False

        # No empty spaces and no possible merges, game is over
        return True
    

    def play_game(self):
        """ Handles user input for playing the game in the console """
        self.reset()

       

        while True:
            print(self.pattern)
            print(self)
            move = input("Enter move (w, a, s, d): ")
            if move == 'a':
                self.shift_left()
            elif move == 'd':
                self.shift_right()
            elif move == 'w':
                self.shift_up()
            elif move == 's':
                self.shift_down()
            else:
                continue
            if self.is_gameover():
                print("Game Over. Your score:", self.score)
                break

    def reset(self):
        """ Resets the game board and score for a new game """
        self.matrix = np.zeros((self.size, self.size), dtype=int)
        self.score = 0
        self.max_tile = 0
        self.prev_Score = 0
        self.pattern = self.generate_snake_pattern()
        self.start_game()



   

    def get_possible_moves(self):
        """ Return a list of possible moves based on the current state of the grid """
       
        possible_moves = []

        # Test shift left
        copy_grid = deepcopy(self)
        copy_grid.shift_left()
        if self.grid_change(copy_grid):
           possible_moves.append('left')

        # Test shift right
        copy_grid = deepcopy(self)
        copy_grid.shift_right()
        if self.grid_change(copy_grid):
            possible_moves.append('right')

        # Test shift up
        copy_grid = deepcopy(self)
        copy_grid.shift_up()
        if self.grid_change(copy_grid):
            possible_moves.append('up')

        # Test shift down
        copy_grid = deepcopy(self)
        copy_grid.shift_down()
        if self.grid_change(copy_grid):
            possible_moves.append('down')

        return possible_moves

 
    

    def generate_snake_pattern(self):
        pattern = np.zeros((self.size, self.size), dtype=int)
        index = 0
        for i in range(self.size):
            if i % 2 == 0:
                # Fill left to right on even rows
                pattern[i, :] = np.arange(index, index + self.size)
            else:
                # Fill right to left on odd rows
                pattern[i, :] = np.arange(index + self.size - 1, index - 1, -1)
            index += self.size
        # return np.max(pattern) - pattern
        data =  [[6,5,4,3], [5,4,3,2],[4,3,2,1], [3,2,1,0]]
        return np.array(data)

    def calculate_snake_score(self):
        snake_score = 0
        for i in range(self.size):
            for j in range(self.size):
                snake_score += self.matrix[i, j] * (self.pattern[i, j])
        return snake_score





    def __eq__(self, other):
        if self.matrix == other.matrix and self.score == other.score\
           and self.size == other.size:
            return True
        else:
            return False

    def __str__(self):
        # get matrix values as str
        matrix = '' 
        for i in range(self.size):
            matrix = matrix + '\n'
            for j in range(self.size):
                matrix = matrix + str(self.matrix[i][j]) + ' '          
                
        output = '\nSocre: '\
                 + str(self.score) + '\n' + 'Merging: '\
                 + str(self.get_score_diff()) +  '\n' + 'Max Tile: '\
                 + str(self.get_max_value()) + '\n' + matrix
        return output


def main():
    game = Grid(2)
    game.play_game()
    pattern = game.generate_snake_pattern
    print(pattern)



if __name__ == "__main__":
    main()