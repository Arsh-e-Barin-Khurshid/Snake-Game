import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25
UPDATE_INTERVAL = 100  # Interval in milliseconds for updating the game state

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()

# Initialize game variables
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0

def reset_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score
    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = Tile(random.randint(0, COLS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    canvas.delete("all")
    show_start_screen()

def change_direction(e):
    global velocityX, velocityY, game_over
    if game_over:
        return

    if e.keysym == "w" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "s" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "a" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "d" and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score
    if game_over:
        return
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"GAME OVER: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 40, font="Arial 15", text="Click to Restart", fill="white")
        canvas.bind("<Button-1>", restart_game)  # Bind click to restart game
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score {score}", fill="white")

    window.after(UPDATE_INTERVAL, draw)  # Consistent update interval

def show_start_screen():
    canvas.delete("all")
    canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text="Click to Start", fill="white")
    canvas.bind("<Button-1>", start_game)

def start_game(event=None):
    canvas.unbind("<Button-1>")
    window.bind("<KeyRelease>", change_direction)
    draw()

def restart_game(event=None):
    canvas.unbind("<Button-1>")
    reset_game()

# Start the game
show_start_screen()
window.mainloop()

