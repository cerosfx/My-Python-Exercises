# Pygame dev 1
# Basic game setup
# Set up display

import pygame

SCREEN_TITLE = 'Crossy-RPG'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
BLACK_COLOR = (0, 0, 0)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)


class Game:
    TICK_RATE = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player2.png', 375, 700, 50, 50)
        enemy_0 = EnemyCharacter('enemy.png',20, 600, 50, 50)
        enemy_1 = EnemyCharacter('enemy.png',20, 400, 50, 50)
        enemy_2 = EnemyCharacter('enemy.png',20, 200, 50, 50)

        
        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:  # Detect if key is pressed down
                    if event.key == pygame.K_UP:  # move up if up key pressed
                        direction = 1
                    elif event.key == pygame.K_DOWN:  # Move down if down key pressed
                        direction = -1
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

                print(event)
            # Redraw the screen to be a blank white window
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))
             
            treasure.draw(self.game_screen)
            
            # Update player position
            player_character.move(direction, self.height)
            # Draw player at the position
            player_character.draw(self.game_screen)

            enemies = [enemy_0, enemy_1, enemy_2]

            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            enemy_1.move(self.width)
            enemy_1.draw(self.game_screen)

            enemy_2.move(self.width)
            enemy_2.draw(self.game_screen)

            

            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render('You lose =(', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break
                
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('You Win =)', True, BLACK_COLOR)
                self.game_screen.blit(text, (300, 350))
                pygame.display.update()
                clock.tick(1)
                break

            pygame.display.update()
            clock.tick(self.TICK_RATE)

        if did_win:
            self.run_game_loop()
        else:
            return
        


class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))

        self.x_pos = x
        self.y_pos = y

        self.width = width #these are collision detection
        self.height = height

    # Draw the object by blitting it onto background (game screen)
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


# Class to represent the playable character
class PlayerCharacter(GameObject):
    # How many tiles the player moves per second.
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move character up if direction > 0 and down if < 0
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        if self.y_pos >= max_height - self.height:    
           self.y_pos = max_height - self.height


    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        
        return True
            
           

class EnemyCharacter(GameObject):
    # How many tiles the player moves per second.
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self,max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - (20 + self.width):
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
        
       

pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop()

pygame.quit()
quit()
