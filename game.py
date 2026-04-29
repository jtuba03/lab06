#!/usr/bin/env python3
"""Classic Snake game for Lab06 using Pygame."""

import random
import sys

import pygame

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

FPS = 12

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (220, 20, 60)
YELLOW = (255, 220, 0)
GRAY = (40, 40, 40)

FOOD_COLORS = [RED, YELLOW]


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.foods = []
        self.spawn_food()
        self.spawn_food()
        self.spawn_food()

    def spawn_food(self):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) in self.snake or any(food[0] == x and food[1] == y for food in self.foods):
                continue
            color = random.choice(FOOD_COLORS)
            self.foods.append((x, y, color))
            return

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.direction != (0, 1):
            self.direction = (0, -1)
        elif keys[pygame.K_s] and self.direction != (0, -1):
            self.direction = (0, 1)
        elif keys[pygame.K_a] and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif keys[pygame.K_d] and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        food_eaten = False
        for index, food in enumerate(self.foods):
            if new_head[0] == food[0] and new_head[1] == food[1]:
                self.score += 10
                self.foods.pop(index)
                self.spawn_food()
                food_eaten = True
                break

        if not food_eaten:
            self.snake.pop()

    def draw_food(self, x, y, color):
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        highlight = pygame.Rect(rect.x + 4, rect.y + 4, GRID_SIZE - 8, GRID_SIZE - 8)
        pygame.draw.rect(self.screen, WHITE, highlight, 2)

    def draw(self):
        self.screen.fill(BLACK)
        for i in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (i, 0), (i, WINDOW_HEIGHT))
        for i in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, i), (WINDOW_WIDTH, i))

        for index, segment in enumerate(self.snake):
            color = BRIGHT_GREEN if index == 0 else GREEN
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, color, rect)

        for food in self.foods:
            self.draw_food(food[0], food[1], food[2])

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        food_text = self.font.render(f"Food: {len(self.foods)}", True, WHITE)
        self.screen.blit(food_text, (10, 40))

        if self.game_over:
            over_text = self.large_font.render("GAME OVER", True, RED)
            over_rect = over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(over_text, over_rect)
            retry_text = self.font.render("Press R to restart", True, WHITE)
            retry_rect = retry_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(retry_text, retry_rect)

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    SnakeGame().run()
