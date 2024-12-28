# import the modules
import pygame
import sys
import random
from enum import Enum
import os

# initialise the game
pygame.init()

# dividing the screen into a grid and adding some offset
cell_size = 30
number_of_cells = 25
offset = 75
screen = pygame.display.set_mode((cell_size * number_of_cells + 2 * offset, cell_size * number_of_cells + 2 * offset))
pygame.display.set_caption("Snake")

# clock and frame rate
frame_rate = 60
clock = pygame.time.Clock()

# load everything dynamically to make .exe file 
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# fonts used
title_font = pygame.font.Font(os.path.join(base_path, "space_invaders.ttf"), 40)
scores_font = pygame.font.Font(os.path.join(base_path, "space_invaders.ttf"), 20)
huge_font = pygame.font.Font(os.path.join(base_path, "space_invaders.ttf"), 130)
med_font = pygame.font.Font(os.path.join(base_path, "space_invaders.ttf"), 70)

# colors for the game
def get_bg_color():
    num = random.randint(1,5)
    if num == 1:
        COLOR = (152, 193, 139)
    elif num == 2:
        COLOR = (242, 234, 213)
    elif num == 3:
        COLOR = (173, 193, 202)
    elif num == 4:
        COLOR = (192, 222, 228)
    elif num == 5:
        COLOR = (182, 197, 182)
    return COLOR
PINE = (0, 121, 107)
bg_color = get_bg_color()

# visual improvements
# for glowing border
def draw_glowing_border():
    for i in range(10):  # Draw multiple rectangles with decreasing opacity
        color = (0, 121, 107, 255 - i * 25)
        rect = pygame.Rect(
            offset - i, 
            offset - i, 
            cell_size * number_of_cells + i * 2, 
            cell_size * number_of_cells + i * 2
        )
        pygame.draw.rect(screen, color, rect, width=1)

# grid like pattern
def draw_checkerboard():
    for row in range(number_of_cells):
        for col in range(number_of_cells):
            if (row + col) % 2 == 0:  # Alternate between two colors
                color = (200, 230, 200)  # Light green
            else:
                color = (240, 275, 220)  # Slightly lighter green
            rect = pygame.Rect(
                offset + col * cell_size,
                offset + row * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, color, rect)

def draw_grid():
    for x in range(offset, screen.get_width() - offset, cell_size):
        pygame.draw.line(screen, (200, 200, 200), (x, offset), (x, screen.get_height() - offset), 1)
    for y in range(offset, screen.get_height() - offset, cell_size):
        pygame.draw.line(screen, (200, 200, 200), (offset, y), (screen.get_width() - offset, y), 1)


# food that the snake will eat
class Food:
    # initialises the object of food class
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    # gets a random cell of the grid
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return pygame.math.Vector2(x, y)

    # genrates a random position not intersecting the snake body
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()            
        return position
    
    # draw function
    def draw(self):
        # pygame.Rect(top left corner x, top left corner y, width, height)
        # adjust for the grid
        food_rect = pygame.Rect(offset + self.position.x * cell_size,offset+ self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)
food_surface = pygame.image.load(os.path.join(base_path, "food.png"))


# snake class for the game
class Snake:
    def __init__(self):
        # store the body as a list of vectors
        self.body = [pygame.math.Vector2(6,9), pygame.math.Vector2(5,9), pygame.math.Vector2(4,9)]
        self.direction = pygame.math.Vector2(1, 0)
        self.add_segment = False

    # draw function
    def draw(self):
        # colors each cell in the grid containing the vector position of snake body 
        for segment in self.body:
            segment_rect = (offset + segment.x * cell_size,offset + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, PINE, segment_rect, 0, 7)
    
    def update(self):
        # always add the head of snake at the top of list based on the direction
        self.body.insert(0, self.body[0] + self.direction)
        # if food is eaten then doesnt remove the last element from the list
        if self.add_segment == True:
            self.add_segment = False
        else:
            # remove the last element from the list
            self.body = self.body[:-1]

    # reset to default position
    def reset(self):
        self.body = [pygame.math.Vector2(6,9), pygame.math.Vector2(5,9), pygame.math.Vector2(4,9)]
        self.direction = pygame.math.Vector2(1, 0)
# slow snake speed
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

# enum class for gamestates
class GameState(Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3
    PAUSE = 4

# class to handle the game
class Game:
    # initialises game elements
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.current_state = GameState.MENU
        self.score = 0
    
    
    # draws the screen based on gamestate
    def draw(self):
        if self.current_state == GameState.GAME:
            self.food.draw()
            self.snake.draw()
        elif self.current_state == GameState.MENU:
            self.draw_menu()
        elif self.current_state == GameState.PAUSE:
            self.draw_pause()
        elif self.current_state == GameState.GAME_OVER:
            self.draw_game_over()

    # update the game screen based on any events
    def update(self):
        if self.current_state == GameState.GAME:
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    # if head of snake reaches the location of food
    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            if self.score % 5 == 0:  # Increase speed every 5 points
                pygame.time.set_timer(SNAKE_UPDATE, max(50, 200 - self.score * 10))

    # if the snake collides with edge
    def check_collision_with_edges(self):
        if (self.snake.body[0].x == number_of_cells) or (self.snake.body[0].x == -1) or (self.snake.body[0].y == number_of_cells) or (self.snake.body[0].y == -1):
            self.game_over()
    
    # game over condition
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.current_state = GameState.GAME_OVER
        self.score = 0

    # if the head touches any part of the body
    def check_collision_with_tail(self):
        body_wo_head = self.snake.body[1:]
        if self.snake.body[0] in body_wo_head:
            self.game_over()
    
    # draw menu items
    def draw_menu(self):
        menu_surface = huge_font.render("SNAKE", True, PINE)
        start_surface = title_font.render("Press ENTER to Start", True, PINE)
        screen.blit(menu_surface, (screen.get_width() // 2 - menu_surface.get_width() // 2, 150))
        screen.blit(start_surface, (screen.get_width() // 2 - start_surface.get_width() // 2, 650))

    # draw pause screen
    def draw_pause(self):
        pause_surface = med_font.render("PAUSED", True, PINE)
        resume_surface = title_font.render("Press ESC to Resume", True, PINE)
        screen.blit(pause_surface, (screen.get_width() // 2 - pause_surface.get_width() // 2, 150))
        screen.blit(resume_surface, (screen.get_width() // 2 - resume_surface.get_width() // 2, 650))

    # draw game over screen
    def draw_game_over(self):
        game_over_surface = med_font.render("GAME OVER", True, PINE)
        retry_surface = title_font.render("Press ENTER to Retry", True, PINE)
        screen.blit(game_over_surface, (screen.get_width() // 2 - game_over_surface.get_width() // 2, 150))
        screen.blit(score_surface, (screen.get_width() // 2 - score_surface.get_width() // 2, 300))
        screen.blit(retry_surface, (screen.get_width() // 2 - retry_surface.get_width() // 2, 650))

# initialise a game object
game = Game()

# game music
sound_path = os.path.join(base_path, "sound_track.mp3")
game.music = pygame.mixer.Sound(sound_path)
game.music.play(-1)
game.music.set_volume(0.03)

# game loop
running = True
while (running):

    # get all the events
    for event in pygame.event.get():

        # handle exit of game
        if event.type == pygame.QUIT:
            running = False

        # balance the speed of snake
        if event.type == SNAKE_UPDATE:
            game.update()

        # handling of key presses  
        if event.type == pygame.KEYDOWN:
            
            # if enter is pressed while in MENU state
            if game.current_state == GameState.MENU:
                if event.key == pygame.K_RETURN:  
                    game.current_state = GameState.GAME

            # handle snake movement while in GAME state
            elif game.current_state == GameState.GAME:
                if event.key == pygame.K_UP and game.snake.direction != pygame.math.Vector2(0, 1):
                    game.snake.direction = pygame.math.Vector2(0, -1)
                elif event.key == pygame.K_DOWN and game.snake.direction != pygame.math.Vector2(0, -1):
                    game.snake.direction = pygame.math.Vector2(0, 1)
                elif event.key == pygame.K_RIGHT and game.snake.direction != pygame.math.Vector2(-1, 0):
                    game.snake.direction = pygame.math.Vector2(1, 0)   
                elif event.key == pygame.K_LEFT and game.snake.direction != pygame.math.Vector2(1, 0):
                    game.snake.direction = pygame.math.Vector2(-1, 0)
                # Pause the game if esc is pressed
                elif event.key == pygame.K_ESCAPE:  
                    game.current_state = GameState.PAUSE
            
            # press esc key when PAUSE state to resume
            elif game.current_state == GameState.PAUSE:
                # Resume game from pause
                if event.key == pygame.K_ESCAPE:  
                    game.current_state = GameState.GAME
            
            # for GAME OVER state
            elif game.current_state == GameState.GAME_OVER:
                # Restart game from game over
                if event.key == pygame.K_RETURN: 
                    game.current_state = GameState.GAME
                    game.snake.reset()
                    game.food.position = game.food.generate_random_pos(game.snake.body)
                    game.score = 0
                    bg_color = get_bg_color()
                    pygame.time.set_timer(SNAKE_UPDATE, 200)
            
            # update the game
            if event.type == SNAKE_UPDATE and game.current_state == GameState.GAME:
                game.update()


    # display all the objects
    screen.fill(bg_color)

    if game.current_state == GameState.GAME:
        pygame.draw.rect(screen, PINE, (offset - 5, offset - 5, cell_size * number_of_cells + 10, cell_size * number_of_cells + 10), 5)
        title_surface = title_font.render("SNAKE", True, PINE)
        screen.blit(title_surface, (offset - 5, 20))
        score_surface = scores_font.render(f"Score: {game.score}", True, PINE)
        screen.blit(score_surface, (cell_size * number_of_cells - 10, 35))
        draw_grid()
    
    # update screen
    draw_glowing_border()
    game.draw()

    pygame.display.update()
    clock.tick(frame_rate)


# ending the game
pygame.quit()
sys.exit()
