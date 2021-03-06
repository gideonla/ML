# -*- coding: utf-8 -*-
import curses,time
from random import randint
import math

class SnakeGame:
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
        self.vertical = False
        #self.last_key # if no move is made the last key sets how the snake continues
        self.key_num_map={0:curses.KEY_LEFT,1:curses.KEY_RIGHT,2:curses.KEY_UP,3:curses.KEY_DOWN}
        self.state = [0] * 5

    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: self.render_init()
        return self.generate_observations()

    def snake_init(self):
        x = randint(5, self.board["width"] - 5)
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        self.vertical = randint(0,1) == 0
        for i in range(3):
            point = [x + i, y] if self.vertical else [x, y + i]
            self.snake.insert(0, point)
        if self.vertical:
            self.last_key = curses.KEY_DOWN
        else:
            self.last_key = curses.KEY_RIGHT

    def generate_food(self):
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: food = []
        self.food = food

    def render_init(self):
        screen = curses.initscr()
        self.win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        self.win.nodelay(1)
        self.win.timeout(1000)
        self.win.keypad(1)

        self.win2 = curses.newwin(200, 200, self.board["height"] + 2, 0)

        self.win2.nodelay(1)
        self.win2.timeout(100)
        self.win2.clear()
        # self.win2.border()

        curses.curs_set(0)

        self.render()

    def display_NN_data(self, pos: int, data: str):
        self.win2.addstr(pos, 0, data)

    def render(self):
        self.win.clear()
        self.win.border(0)
        self.win.addstr(0,1, 'state : ' + str(self.state) + ' ')
        self.win.addch(self.food[0], self.food[1], 'A')
        for i, point in enumerate(self.snake):
            if i == 0:
                self.win.addch(point[0], point[1], 'H')
            else:
                self.win.addch(point[0], point[1], 'X')
       # self.win.getch()

    def step(self, key):
        # 0 - UP
        # 1 - RIGHT
        # 2 - DOWN
        # 3 - LEFT
        if self.done == True: self.end_game()
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        else:
            self.remove_last_point()
        self.check_collisions()
        if self.gui: self.render()
        #print (self.return_state())
        self.update_state()
        return self.generate_observations()

    def create_new_point(self, key):
        new_point = [self.snake[0][0], self.snake[0][1]]
        if self.vertical and ((key == curses.KEY_DOWN) or (key == curses.KEY_UP)):
            key = self.last_key
        if not self.vertical and ((key == curses.KEY_LEFT) or (key == curses.KEY_RIGHT)):
            key = self.last_key
        if key == -1:
            key = self.last_key
        if key == curses.KEY_LEFT:
            new_point[1] += -1
            self.last_key = curses.KEY_LEFT
            self.vertical = False
        elif key == curses.KEY_RIGHT:
            new_point[1] += 1
            self.last_key = curses.KEY_RIGHT
            self.vertical = False
        elif key == curses.KEY_UP:
            new_point[0] += -1
            self.last_key = curses.KEY_UP
            self.vertical = True
        elif key == curses.KEY_DOWN:
            new_point[0] += +1
            self.last_key = curses.KEY_DOWN
            self.vertical = True
        self.snake.insert(0, new_point)

    def remove_last_point(self):
        self.snake.pop()

    def food_eaten(self):
        return self.snake[0] == self.food

    def check_collisions(self):
        if (self.snake[0][0] == 0 or
            self.snake[0][0] == self.board["width"] + 1 or
            self.snake[0][1] == 0 or
            self.snake[0][1] == self.board["height"] + 1 or
            self.snake[0] in self.snake[1:-1]):
            self.done = True

    def generate_observations(self):
        return self.state, self.score, self.done, 1

    def update_state(self): # this is for the NN, this function will return an array of 5 numbers: distance from all 4 walls (left, right,top, bottom) and distance to apple
        top = self.snake[0][0]
        bottom = self.board["height"]-top
        left = self.snake[0][1]
        right = self.board["width"]-left
        distance_to_apple = int(math.sqrt((self.snake[0][0]-self.food[0])**2+(self.snake[0][1]-self.food[1])**2))
        self.state = [top,bottom,left,right,distance_to_apple]

    def return_state(self): # this is for the NN, this function will return an array of 5 numbers: distance from all 4 walls (left, right,top, bottom) and distance to apple
        top = self.snake[0][0]
        bottom = self.board["height"]-top
        left = self.snake[0][1]
        right = self.board["width"]-left
        distance_to_apple = int(math.sqrt((self.snake[0][0]-self.food[0])**2+(self.snake[0][1]-self.food[1])**2))
        return [top,bottom,left,right,distance_to_apple]

    def render_destroy(self):
        curses.endwin()

    def end_game(self):
        if self.gui: self.render_destroy()
        raise Exception("Game over")

if __name__ == "__main__":
    game = SnakeGame(gui = True)
    game.start()
    while True:
        #game.step(game.key_num_map.get((randint(0,3))))
        game.step(game.win.getch())
