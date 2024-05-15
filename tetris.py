import pygame
import random

# Initialize Pygame
pygame.init()

# Window dimensions
window_width = 300
window_height = 600
cell_size = 30
cols = window_width // cell_size
rows = window_height // cell_size

# Define colors
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128)
]

# Define shapes
shapes = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],

    [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],

    [['.....',
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
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']],

    [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
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
      '.....']],

    [['.....',
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
]


# Class for Tetromino shapes
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.x = cols // 2 - len(shape[0]) // 2
        self.y = 0

    def image(self):
        """Get the current rotation of the shape."""
        return self.shape[self.rotation]

    def rotate(self, direction=1):
        """Rotate the shape."""
        self.rotation = (self.rotation + direction) % len(self.shape)


# Create grid
def create_grid(locked_positions={}):
    """
    Create the game grid.

    Parameters:
    locked_positions (dict): Dictionary of locked positions.

    Returns:
    list: 2D list representing the grid.
    """
    grid = [[(0, 0, 0) for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid


# Check if the space is valid for the shape
def valid_space(shape, grid):
    """
    Check if the current position of the shape is valid.

    Parameters:
    shape (Tetromino): The shape to check.
    grid (list): The current game grid.

    Returns:
    bool: True if valid, False otherwise.
    """
    accepted_positions = [[(x, y) for x in range(cols) if grid[y][x] == (0, 0, 0)] for y in range(rows)]
    accepted_positions = [x for item in accepted_positions for x in item]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


# Convert the shape format to grid positions
def convert_shape_format(shape):
    """
    Convert shape format to positions in the grid.

    Parameters:
    shape (Tetromino): The shape to convert.

    Returns:
    list: List of positions in the grid.
    """
    positions = []
    format = shape.image()
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for pos in positions:
        positions[positions.index(pos)] = (pos[0], pos[1])
    return positions


# Check if the game is lost
def check_lost(locked_positions):
    """
    Check if the game is lost.

    Parameters:
    locked_positions (dict): Dictionary of locked positions.

    Returns:
    bool: True if lost, False otherwise.
    """
    for pos in locked_positions:
        x, y = pos
        if y < 1:
            return True
    return False


# Clear filled rows
def clear_rows(grid, locked):
    """
    Clear filled rows in the grid.

    Parameters:
    grid (list): The current game grid.
    locked (dict): Dictionary of locked positions.

    Returns:
    int: Number of cleared rows.
    """
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


# Draw the game window
def draw_window(surface, grid, score=0):
    """
    Draw the game window.

    Parameters:
    surface (pygame.Surface): The surface to draw on.
    grid (list): The current game grid.
    score (int): The current score.
    """
    surface.fill((0, 0, 0))
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(surface, grid[i][j], (j * cell_size, i * cell_size, cell_size, cell_size), 0)
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    surface.blit(label, (window_width - label.get_width() - 10, 10))


# Draw text in the middle of the screen
def draw_text_middle(surface, text, size, color):
    """
    Draw text in the middle of the screen.

    Parameters:
    surface (pygame.Surface): The surface to draw on.
    text (str): The text to draw.
    size (int): The font size.
    color (tuple): The color of the text.
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (window_width / 2 - label.get_width() / 2, window_height / 2 - label.get_height() / 2))


# Main game loop
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = Tetromino(random.choice(shapes), random.randint(1, len(colors) - 1))
    next_piece = Tetromino(random.choice(shapes), random.randint(1, len(colors) - 1))
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    score = 0
    pressing_down = False
    last_color = current_piece.color

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if pressing_down:
            fall_speed = 0.05
        else:
            fall_speed = 0.27

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate(-1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = colors[current_piece.color]

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = colors[current_piece.color]

            current_piece = next_piece

            while current_piece.color == last_color:
                current_piece = Tetromino(random.choice(shapes), random.randint(1, len(colors) - 1))

            last_color = current_piece.color
            next_piece = Tetromino(random.choice(shapes), random.randint(1, len(colors) - 1))
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

            # Check if the new piece is in a valid position, if not, the game is over
            if not valid_space(current_piece, grid):
                run = False

        draw_window(win, grid, score)
        pygame.display.update()

    draw_text_middle(win, "GAME OVER", 40, (255, 255, 255))
    pygame.display.update()
    pygame.time.delay(2000)  # Pause before showing "Continue? Y/N"

    # Ask the player if they want to continue
    while True:
        draw_window(win, grid, score)  # Clear the previous text
        draw_text_middle(win, "Continue? Y/N", 40, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    main()
                elif event.key == pygame.K_n:
                    pygame.quit()
                    quit()


win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Tetris')
main()
