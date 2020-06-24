###############################################################
          ##  TETRIS GAME USING PYGAME  ##
###############################################################
'''
10 X 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0-6
'''

import pygame
import random
from pygame import mixer


pygame.init()  # Initialize pycharm functions
pygame.font.init()  # Initializes fonts and makes them available for use

# Set icon for our window
icon = pygame.image.load('tetris.png')
pygame.display.set_icon(icon)

# background img
background = pygame.image.load('bg.png')

# Image on the black window
puzzel_Img = pygame.image.load('puzzel.png')
imgX = 190
imgY = 150

# Game over image
over_Img = pygame.image.load('gameover.png')

# Background music
mixer.music.load('music.wav')
mixer.music.play(-1)

# todo SHAPE ORIENTATION

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.0000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00.',
      '.0...',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0.',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# todo GLOBAL VARIABLES

# A list of all 7 shapes of pieces
shapes = [S, Z, I, O, J, L, T]

# A list depicting the colour (in RGB value) for corresponding shapes of pieces.
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Size of each block on the playing grid
block_size = 30

# variable for maintaining the scores
score = 0

# Set the width and height of the game window
w_height = 800
w_width = 700

# playing area
play_width = 300
play_height = 600

top_left_x = (w_width - play_width) // 2
top_left_y = (w_height - play_height)


# todo CLASS DEFINITION
class Piece:
    x = 10  # Number of columns, set default to 10
    y = 20  # Number of rows, set default to 20
    shape = 0  # Shape of piece, set default to 0
    color = ()  # Color of shape (Transparent by default)
    rotation = 0  # Current orientation/rotation, default set to 0

    # This is a constructor
    def __init__(self, column, row, shape):
        # The values in parameters are assigned to the new object of type 'Piece
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


# todo FUNCTION DEFINITION
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)  # Assign the font

    label = font.render(text, 1, color)  # Render the Text using font

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y +
                         play_height / 2 - label.get_height() / 2))  # Print the Text using label


def create_grid(locked_positions):
    #  Create a 10*20 matrix initialized with (0,0,0)
    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]
    # Color the grid where the blocks are occupied already
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def get_shape():
    # Make a new object of type Piece with a randomly chosen shape
    newPiece = Piece(5, 0, random.choice(shapes))
    # return this object
    return newPiece


def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    # Loop over the formatted grid
    i = 0
    for line in format:
        row = list(line)
        j = 0
        for column in row:
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
            j += 1
        i += 1
    k = 0
    for pos in positions:  # optional
        positions[k] = (pos[0] - 2, pos[1] - 4)
        k += 1
    return positions


def valid_space(piece, grid):
    # Matrix of all position which are not currently occupied
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # Narrow down the matrix for easier handling
    accepted_positions = [j for sub in accepted_positions for j in sub]
    # convert_shape format returns a list of strings of the current shape in its correct orientation
    formatted = convert_shape_format(piece)

    # check if the block lies in a position that is not accepted(not valid)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    # Traverse through the locked positions
    for pos in positions:
        x, y = pos
        # If block crosses the above boundary of grid
        if y < 1:
            return True
    return False


def update_scores(nscore):  # storing the scores in a file
    score = max_score()

    with open('scores.txt', 'w') as f:  # opening fie in write mode
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:  # opening file in read mode
        lines = f.readlines()
        score = lines[0].strip()

    return score


def update_score(surface):
    text = "Score : " + str(score)
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render(text, 1, (255, 255, 255))

    sx = top_left_x + play_width + 40
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 10, sy + 150))


def draw_next_shape(piece, surface):
    # Decide the font and render it
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    # Where to display the next piece? These are the coordinates
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    # List of strings depicting the orientation of piece
    format = piece.shape[piece.rotation % len(piece.shape)]
    i = 0
    for line in format:
        row = list(line)
        j = 0
        # Traverse through each string
        for column in row:
            if column == '0':
                # Draw the next_piece
                pygame.draw.rect(surface, piece.color, (sx + j * 30, sy + i * 30, 30, 30), 0)
            j += 1
        i += 1
    surface.blit(label, (sx + 10, sy - 30))
    update_score(surface)


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        # Draw Horizontal Lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30), (sx + play_width, sy + i * 30))
        for j in range(col):
            # Draw Vertical Lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))


def draw_window(surface, last_score=0):
    # Fill the window with Black Color
    surface.fill((0, 0, 0))
    # We did this in the draw_text_middle() function
    # Decide the font, render the text with font, and print it on surface
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    # Draw the current_piece in grid
    # Traverse through the entire grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # draw the block
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, block_size, block_size), 0)
        # last score
        font = pygame.font.SysFont('comicsans', 35)
        label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

        sx = top_left_x - 200
        sy = top_left_y + 200

        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j],
                                 (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

        draw_grid(surface, 20, 10)
        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def clear_rows(grid, locked):
    # We store the number of rows to shift down in inc
    inc = 0
    global score
    # Traverse the grid in reverse direction
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # Check if there is any empty position(block) in this row
        if (0, 0, 0) not in row:
            inc += 1
            # Clear this row, save the index into ind
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        # Sort the locked position, store into temp
        temp = sorted(list(locked), key=lambda x: x[1])
        # Traverse temp in reverse direction
        for key in temp[::-1]:
            x, y = key
            # If the y coordinate of this position is less than ind
            if y < ind:
                # Update the y coordinate
                newKey = (x, y + inc)
                # Remove the previous locked position from the list
                locked[newKey] = locked.pop(key)
        score += 10
        update_scores(score)  # for updating high scores


def play():  # playing area
    # A global variable grid
    global grid
    # The positions already occupied by the block
    locked_positions = {}
    # create_grid returns the created grid
    grid = create_grid(locked_positions)
    # change_piece turns True when the next piece is to be released
    change_piece = False
    # run remains True unless the user decides to quit
    run = True
    # current_piece holds the current piece falling in the grid
    current_piece = get_shape()
    # next_piece holds the piece that would fall once the current one sets down
    next_piece = get_shape()
    # clock is used to keep a track of time for the falling piece
    clock = pygame.time.Clock()
    # This keeps a track of the time to automatically move current_piece one position down in vertical direction
    fall_time = 0

    while run:
        # Decide the falling speed
        fall_speed = 0.27
        # An updated grid is created each time
        grid = create_grid(locked_positions)
        # update the fall_time
        fall_time += clock.get_rawtime()
        # Move the clock ahead by 1 second
        clock.tick()

        # This block decides when to move the piece down vertically by one position
        if fall_time / 1000 >= fall_speed:  # convert the fall_time into ms
            # Update the clock time and piece position
            fall_time = 0
            current_piece.y += 1  # one position down
        # Check if the piece touches the ground or existing stack
        if not (valid_space(current_piece, grid)) and current_piece.y > 0:
            current_piece.y -= 1  # reverse the change
            change_piece = True  # next piece will fall

        for event in pygame.event.get():
            # Check if user clicks on CROSS button to QUIT
            if event.type == pygame.QUIT:
                run = False
                # Simply quit the game window
                pygame.display.quit()
                # Exit the game now
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Left key
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:  # Right key
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:  # Down key
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:  # Up key
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        # Convert the current_position into coordinates on the grid
        shape_pos = convert_shape_format(current_piece)
        # Traverse through the grid and color it!
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
            # If change_piece is true, update the locked_positions by the current_piece
            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                # Then, assign next_piece to current_piece, assign random shape to next_piece
                current_piece = next_piece
                next_piece = get_shape()
                # Revert change_piece to False for the next falling piece
                change_piece = False
            clear_rows(grid, locked_positions)

        draw_window(window)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
            score = 0
            draw_window(window, score)

    window.fill((0, 0, 0))
    window.blit(over_Img, (imgX, imgY))
    draw_text_middle("Oops, You Lost", 80, (255, 255, 255), window)
    # Update the screen
    pygame.display.update()
    pygame.time.delay(2000)


def game():
    run = True

    while run:  # Our game runs until 'run' is made 'False'
        window.fill((0, 0, 0))
        window.blit(background, (0, 5))
        window.blit(puzzel_Img, (imgX, imgY))  # Image appears on black window
        draw_text_middle("Press any key to begin!", 60, (255, 255, 255), window)  # Display this text in the middle
        # of the window
        pygame.display.update()  # Update the screen

        # Track every event while the game is running
        for event in pygame.event.get():
            # If the user presses any key, start playing the game!
            if event.type == pygame.KEYDOWN:
                play()
            # If user clicks on the 'cross' to quit, make run = False
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


# todo DRIVER CODE
# Make the game window
window = pygame.display.set_mode((w_width, w_height))

pygame.display.set_caption("TETRIS")

game()
