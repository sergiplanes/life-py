# Author: Sergi Planes Ortiz
# Date: 2023/03/22

# Description: This is a simple implementation of Conway's Game of Life using Pygame.

# Imports
import random
import pygame


# Classes

# Cell class
class Cell:

    # Constructor
    # x: x position
    # y: y position
    # width: width of the cell
    # height: height of the cell
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alive = False
        self.next_state = False

    # Update the cell
    # game: the game
    def update(self, game):
        # count the number of neighbors
        neighbors = 0

        # check the neighbors
        for x in range(-1, 2):
            for y in range(-1, 2):
                # skip the cell itself
                if x == 0 and y == 0:
                    continue
                column = int((self.x + x * self.width) / self.width)
                row = int((self.y + y * self.height) / self.height)
                if column < 0 or column >= len(game.cells) or row < 0 or row >= len(game.cells[0]):
                    continue
                if game.cells[column][row].alive:
                    neighbors += 1

        # determine the next state
        if self.alive:
            # if the cell is alive
            if neighbors < game.survival_min or neighbors > game.survival_max:
                self.next_state = False
            else:
                self.next_state = True
        else:
            # if the cell is dead
            if neighbors == game.birth_threshold:
                self.next_state = True
            else:
                self.next_state = False

    # Draw the cell
    # surface: the surface to draw on
    def draw(self, surface):
        # draw the cell
        if self.alive:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))

    # Commit the next state
    def commit(self):
        # commit the next state
        self.alive = self.next_state


# LifeGame class
class LifeGame:

    # Constructor
    # width: width of the game
    # height: height of the game
    # cell_width: width of the cells'
    # cell_height: height of the cells
    # birth_threshold: number of neighbors needed to create a new cell
    # survival_min: minimum number of neighbors needed to keep a cell alive
    # survival_max: maximum number of neighbors needed to keep a cell alive
    def __init__(self, width, height, cell_width, cell_height, birth_threshold, survival_min, survival_max):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.birth_threshold = birth_threshold
        self.survival_min = survival_min
        self.survival_max = survival_max

        # create the cells
        self.cells = []
        # create the columns
        for x in range(0, width, cell_width):
            column = []
            # create the rows
            for y in range(0, height, cell_height):
                column.append(Cell(x, y, cell_width, cell_height))
            self.cells.append(column)

        # randomly initialize the cells
        for column in self.cells:
            for cell in column:
                # randomly set the cell to alive or dead
                if random.randint(0, 1) == 1:
                    cell.alive = True

    # Update the game
    def update(self):
        # update the cells
        for column in self.cells:
            for cell in column:
                cell.update(self)

        # commit the cells
        for column in self.cells:
            for cell in column:
                cell.commit()

    # Draw the game
    # surface: the surface to draw on
    def draw(self, surface):
        # draw the cells
        for column in self.cells:
            for cell in column:
                cell.draw(surface)

    # Toggle the cell at the given position
    # x: x position
    # y: y position
    def toggle_cell(self, x, y):
        # toggle the cell at the given position
        column = int(x / self.cell_width)
        row = int(y / self.cell_height)
        self.cells[column][row].alive = not self.cells[column][row].alive


# Functions
def game_init():
    # create the "life" game
    pygame.init()
    # create a screen
    screen = pygame.display.set_mode((640, 480))
    # set the caption
    pygame.display.set_caption("Conway's Game of Life")
    # create a clock
    clock = pygame.time.Clock()

    # create a surface to draw on
    background = pygame.Surface(screen.get_size())
    # convert the surface to a format that is faster to draw on
    background = background.convert()
    # fill the background with white
    background.fill((250, 250, 250))

    # create the game
    game = LifeGame(800, 600, 10, 10, 3, 2, 3)

    # main game loop
    while True:
        # limit the frame rate
        clock.tick(60)

        # handle events
        for event in pygame.event.get():
            # quit the game
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.toggle_cell(event.pos[0], event.pos[1])

        # update the game
        game.update()

        # draw the game
        game.draw(background)

        # draw the background
        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    game_init()
