import pygame
import random
import sys
import os
import math

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

COLORS = {
    "background": (0, 0, 0),
    "snake_head": (0, 100, 255),
    "snake_body": (0, 150, 255),
    "snake_tail": (100, 180, 255),
    "food": (255, 50, 50),
    "food_glow": (255, 100, 100),
    "text": (255, 255, 255),
    "highlight": (255, 215, 0),
    "button": (50, 50, 50),
    "button_hover": (80, 80, 80),
    "green": (50, 205, 50),
    "red": (255, 80, 80),
}

DIFFICULTIES = {
    0: {"name": "EASY", "initial_speed": 8, "speed_increment": 0.03, "max_speed": 18},
    1: {
        "name": "NORMAL",
        "initial_speed": 12,
        "speed_increment": 0.05,
        "max_speed": 25,
    },
    2: {"name": "HARD", "initial_speed": 16, "speed_increment": 0.08, "max_speed": 35},
}

DIRECTIONS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

HIGHSCORE_FILE = "highscore.txt"

DIGIT_PATTERNS = {
    "0": [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    "1": [[0, 1, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
    "2": [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    "3": [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    "4": [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
    "5": [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    "6": [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    "7": [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
    "8": [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    "9": [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    ":": [[0], [1], [0], [1], [0]],
    ".": [[0], [0], [0], [0], [1]],
    " ": [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
}

LETTER_PATTERNS = {
    "S": [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    "N": [[1, 0, 1], [1, 1, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]],
    "A": [[0, 1, 0], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]],
    "K": [[1, 0, 1], [1, 1, 0], [1, 0, 0], [1, 1, 0], [1, 0, 1]],
    "E": [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 1, 1]],
    "G": [[1, 1, 1], [1, 0, 0], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    "M": [[1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1]],
    "O": [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    "V": [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [0, 1, 0]],
    "R": [[1, 1, 0], [1, 0, 1], [1, 1, 0], [1, 0, 1], [1, 0, 1]],
    "P": [[1, 1, 0], [1, 0, 1], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
    "U": [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    "D": [[1, 1, 0], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 0]],
    "H": [[1, 0, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]],
    "I": [[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
    "L": [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 1]],
    "C": [[1, 1, 1], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 1]],
    "W": [[1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1]],
    "Y": [[1, 0, 1], [1, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
    "X": [[1, 0, 1], [1, 0, 1], [0, 1, 0], [1, 0, 1], [1, 0, 1]],
    "T": [[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
    "F": [[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]],
    "B": [[1, 1, 0], [1, 0, 1], [1, 1, 0], [1, 0, 1], [1, 1, 0]],
    "Q": [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1]],
    "Z": [[1, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1]],
    "J": [[0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]],
}


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.state = "START"
        self.difficulty = 1
        self.highscore = self.load_highscore()
        self.reset_game()
        self.food_pulse = 0
        self.selected_option = 0

    def draw_char(self, char, x, y, size, color):
        pattern = DIGIT_PATTERNS.get(char) or LETTER_PATTERNS.get(char.upper())
        if not pattern:
            return 0

        for row_idx, row in enumerate(pattern):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (x + col_idx * size, y + row_idx * size, size - 1, size - 1),
                    )

        return (len(pattern[0]) + 1) * size

    def draw_text(self, text, x, y, size, color, center=True):
        total_width = 0
        for char in text:
            pattern = DIGIT_PATTERNS.get(char) or LETTER_PATTERNS.get(char.upper())
            if pattern:
                total_width += (len(pattern[0]) + 1) * size
            else:
                total_width += 2 * size

        if center:
            start_x = x - total_width // 2
        else:
            start_x = x

        current_x = start_x
        for char in text:
            current_x += self.draw_char(char, current_x, y, size, color)

    def draw_button(self, text, x, y, width, height, is_selected=False):
        color = COLORS["highlight"] if is_selected else COLORS["button"]
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=10)
        pygame.draw.rect(
            self.screen, COLORS["text"], (x, y, width, height), 2, border_radius=10
        )
        self.draw_text(
            text, x + width // 2, y + height // 2 - 12, 7, COLORS["text"], center=True
        )

    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def save_highscore(self):
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(self.highscore))
        except:
            pass

    def reset_game(self):
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"

        config = DIFFICULTIES[self.difficulty]
        self.speed = config["initial_speed"]
        self.speed_increment = config["speed_increment"]
        self.max_speed = config["max_speed"]

        self.score = 0
        self.food = self.generate_food()
        self.game_over = False
        self.paused = False
        self.move_counter = 0
        self.new_highscore = False

    def generate_food(self):
        while True:
            food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if food not in self.snake:
                return food

    def draw_start_screen(self):
        self.screen.fill(COLORS["background"])

        snake_x = WINDOW_WIDTH // 2 - 100
        snake_y = 70
        for i in range(5):
            color = COLORS["snake_head"] if i == 0 else COLORS["snake_body"]
            pygame.draw.rect(
                self.screen,
                color,
                (snake_x + i * GRID_SIZE, snake_y, GRID_SIZE - 2, GRID_SIZE - 2),
                border_radius=4,
            )

        self.draw_text("HUNGRY SNAKE", WINDOW_WIDTH // 2, 160, 16, COLORS["highlight"])

        self.draw_text("HIGHEST SCORE", WINDOW_WIDTH // 2, 250, 5, (150, 150, 150))
        self.draw_text(
            str(self.highscore), WINDOW_WIDTH // 2, 290, 10, COLORS["highlight"]
        )

        self.draw_text("DIFFICULTY", WINDOW_WIDTH // 2, 350, 6, (150, 150, 150))

        for i, (diff_id, config) in enumerate(DIFFICULTIES.items()):
            button_width = 180
            button_height = 50
            button_spacing = 30
            total_width = 3 * button_width + 2 * button_spacing
            start_x = (WINDOW_WIDTH - total_width) // 2
            x = start_x + i * (button_width + button_spacing)
            y = 390

            is_selected = i == self.difficulty
            self.draw_button(
                config["name"], x, y, button_width, button_height, is_selected
            )

        self.draw_text(
            "PRESS SPACE OR ENTER TO START", WINDOW_WIDTH // 2, 480, 5, COLORS["text"]
        )
        self.draw_text(
            "USE ARROW KEYS TO MOVE", WINDOW_WIDTH // 2, 520, 5, (150, 150, 150)
        )
        self.draw_text(
            "PRESS ESC OR Q TO QUIT", WINDOW_WIDTH // 2, 555, 4, (100, 100, 100)
        )

    def draw_game(self):
        self.screen.fill(COLORS["background"])

        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (20, 20, 20), (0, y), (WINDOW_WIDTH, y))

        self.draw_snake()
        self.draw_food()

        self.draw_text(
            "SCORE:" + str(self.score), 80, 15, 6, COLORS["text"], center=False
        )

        speed_text = "SPEED:" + str(int(self.speed))
        self.draw_text(
            speed_text, WINDOW_WIDTH - 190, 15, 6, COLORS["text"], center=False
        )

        if self.paused:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            self.draw_text(
                "PAUSED",
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 - 40,
                18,
                COLORS["highlight"],
            )
            self.draw_text(
                "PRESS SPACE OR ESC TO CONTINUE",
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2 + 40,
                5,
                COLORS["text"],
            )

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake):
            rect_x = x * GRID_SIZE + 1
            rect_y = y * GRID_SIZE + 1
            size = GRID_SIZE - 2

            if i == 0:
                color = COLORS["snake_head"]
                pygame.draw.rect(
                    self.screen, color, (rect_x, rect_y, size, size), border_radius=6
                )
                eye_size = 4
                if self.direction == "RIGHT":
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + size - 6, rect_y + 6),
                        eye_size,
                    )
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + size - 6, rect_y + size - 6),
                        eye_size,
                    )
                elif self.direction == "LEFT":
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + 6, rect_y + 6),
                        eye_size,
                    )
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + 6, rect_y + size - 6),
                        eye_size,
                    )
                elif self.direction == "UP":
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + 6, rect_y + 6),
                        eye_size,
                    )
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + size - 6, rect_y + 6),
                        eye_size,
                    )
                else:
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + 6, rect_y + size - 6),
                        eye_size,
                    )
                    pygame.draw.circle(
                        self.screen,
                        COLORS["background"],
                        (rect_x + size - 6, rect_y + size - 6),
                        eye_size,
                    )
            else:
                ratio = i / len(self.snake)
                color = (
                    int(
                        COLORS["snake_body"][0]
                        + (COLORS["snake_tail"][0] - COLORS["snake_body"][0]) * ratio
                    ),
                    int(
                        COLORS["snake_body"][1]
                        + (COLORS["snake_tail"][1] - COLORS["snake_body"][1]) * ratio
                    ),
                    int(
                        COLORS["snake_body"][2]
                        + (COLORS["snake_tail"][2] - COLORS["snake_body"][2]) * ratio
                    ),
                )
                pygame.draw.rect(
                    self.screen, color, (rect_x, rect_y, size, size), border_radius=4
                )

    def draw_food(self):
        self.food_pulse = (self.food_pulse + 0.1) % (2 * math.pi)
        pulse_size = 2 + math.sin(self.food_pulse) * 2

        x = self.food[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.food[1] * GRID_SIZE + GRID_SIZE // 2

        glow_size = int(GRID_SIZE + pulse_size * 2)
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surface, (*COLORS["food_glow"], 50), (glow_size, glow_size), glow_size
        )
        self.screen.blit(glow_surface, (x - glow_size, y - glow_size))

        size = GRID_SIZE - 2
        pygame.draw.rect(
            self.screen,
            COLORS["food"],
            (self.food[0] * GRID_SIZE + 1, self.food[1] * GRID_SIZE + 1, size, size),
            border_radius=5,
        )

    def draw_game_over(self):
        self.draw_game()

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        self.draw_text("GAME OVER", WINDOW_WIDTH // 2, 140, 20, COLORS["red"])

        self.draw_text("FINAL SCORE", WINDOW_WIDTH // 2, 210, 6, (150, 150, 150))
        self.draw_text(str(self.score), WINDOW_WIDTH // 2, 250, 14, COLORS["text"])

        if self.new_highscore:
            self.draw_text("NEW RECORD", WINDOW_WIDTH // 2, 310, 8, COLORS["highlight"])

        options = ["RESTART", "MENU", "QUIT"]
        for i, option in enumerate(options):
            button_width = 180
            button_height = 45
            spacing = 60
            start_y = 360

            x = WINDOW_WIDTH // 2 - button_width // 2
            y = start_y + i * spacing

            is_selected = i == self.selected_option
            self.draw_button(option, x, y, button_width, button_height, is_selected)

        self.draw_text(
            "ARROWS OR W/S TO SELECT", WINDOW_WIDTH // 2, 555, 4, (100, 100, 100)
        )
        self.draw_text("ENTER TO CONFIRM", WINDOW_WIDTH // 2, 580, 4, (100, 100, 100))

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = DIRECTIONS[self.next_direction]
        new_x = head_x + dx
        new_y = head_y + dy

        if new_x < 0:
            new_x = GRID_WIDTH - 1
        elif new_x >= GRID_WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = GRID_HEIGHT - 1
        elif new_y >= GRID_HEIGHT:
            new_y = 0

        new_head = (new_x, new_y)

        self.direction = self.next_direction
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            self.update_speed()
        else:
            self.snake.pop()

    def update_speed(self):
        self.speed = min(self.speed * (1 + self.speed_increment), self.max_speed)

    def check_collision(self):
        head = self.snake[0]
        if head in self.snake[1:]:
            return True
        return False

    def handle_start_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.difficulty = (self.difficulty - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.difficulty = (self.difficulty + 1) % 3
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.reset_game()
                self.state = "PLAYING"
            elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                return False

        return True

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                self.paused = not self.paused
            elif not self.paused:
                if event.key == pygame.K_UP and self.direction != "DOWN":
                    self.next_direction = "UP"
                elif event.key == pygame.K_DOWN and self.direction != "UP":
                    self.next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                    self.next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                    self.next_direction = "RIGHT"

        return True

    def handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % 3
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % 3
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    self.reset_game()
                    self.state = "PLAYING"
                elif self.selected_option == 1:
                    self.state = "START"
                elif self.selected_option == 2:
                    return False
            elif event.key == pygame.K_ESCAPE:
                self.state = "START"

        return True

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if self.state == "START":
                        running = self.handle_start_events(event)
                    elif self.state == "PLAYING":
                        running = self.handle_game_events(event)
                    elif self.state == "GAME_OVER":
                        running = self.handle_game_over_events(event)

            if self.state == "START":
                self.draw_start_screen()

            elif self.state == "PLAYING":
                if not self.paused:
                    self.move_counter += 1
                    if self.move_counter >= 60 / self.speed:
                        self.move_snake()
                        self.move_counter = 0

                        if self.check_collision():
                            if self.score > self.highscore:
                                self.highscore = self.score
                                self.new_highscore = True
                                self.save_highscore()
                            else:
                                self.new_highscore = False
                            self.state = "GAME_OVER"

                self.draw_game()

            elif self.state == "GAME_OVER":
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
