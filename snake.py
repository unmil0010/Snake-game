"""A classic Snake game built with Python's standard-library turtle module."""

from __future__ import annotations

import random
import turtle
from dataclasses import dataclass, field

SCREEN_SIZE = 600
STEP = 20
INITIAL_DELAY_MS = 100
MIN_DELAY_MS = 55
SPEEDUP_MS = 2
BOUNDARY = SCREEN_SIZE // 2 - STEP


@dataclass
class GameState:
    """Game state kept separate from the turtle UI for easy testing."""

    score: int = 0
    high_score: int = 0
    direction: str = "stop"
    segments: list[tuple[int, int]] = field(default_factory=list)
    food: tuple[int, int] = (0, 100)
    game_over: bool = False

    def set_direction(self, new_direction: str) -> None:
        """Change direction without allowing an immediate 180-degree turn."""
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if new_direction not in opposites:
            raise ValueError(f"Unknown direction: {new_direction}")
        if opposites[new_direction] != self.direction:
            self.direction = new_direction

    def move_head(self, position: tuple[int, int]) -> tuple[int, int]:
        x, y = position
        dx, dy = {"up": (0, STEP), "down": (0, -STEP),
                  "left": (-STEP, 0), "right": (STEP, 0),
                  "stop": (0, 0)}[self.direction]
        return x + dx, y + dy

    def reset_round(self) -> None:
        self.score = 0
        self.direction = "stop"
        self.segments.clear()
        self.game_over = False


def random_food_position(rng: random.Random, occupied: set[tuple[int, int]]) -> tuple[int, int]:
    """Choose an unoccupied grid cell inside the play area."""
    cells = [(x, y)
             for x in range(-BOUNDARY, BOUNDARY + 1, STEP)
             for y in range(-BOUNDARY, BOUNDARY + 1, STEP)
             if (x, y) not in occupied]
    if not cells:
        return (0, 0)
    return rng.choice(cells)


class SnakeGame:
    def __init__(self) -> None:
        self.state = GameState()
        self.delay_ms = INITIAL_DELAY_MS
        self.screen = turtle.Screen()
        self.screen.title("Snake Game — Unmil Mukhopadhyay")
        self.screen.bgcolor("white")
        self.screen.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
        self.screen.tracer(0)

        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("triangle")
        self.head.color("red")
        self.head.penup()
        self.head.goto(0, 0)

        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("square")
        self.food.color("blue")
        self.food.penup()
        self.food.goto(*self.state.food)

        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.goto(0, 260)

        self.segment_turtles: list[turtle.Turtle] = []
        self._bind_keys()
        self._draw_score()

    def _bind_keys(self) -> None:
        self.screen.listen()
        for key, direction in (("w", "up"), ("s", "down"),
                               ("a", "left"), ("d", "right"),
                               ("Up", "up"), ("Down", "down"),
                               ("Left", "left"), ("Right", "right")):
            self.screen.onkeypress(lambda d=direction: self.state.set_direction(d), key)
        self.screen.onkeypress(self.restart, "r")

    def _draw_score(self) -> None:
        self.pen.clear()
        self.pen.write(
            f"Score: {self.state.score}  High Score: {self.state.high_score}",
            align="center", font=("Courier", 18, "normal")
        )

    def _add_segment(self) -> None:
        segment = turtle.Turtle()
        segment.speed(0)
        segment.shape("square")
        segment.color("green")
        segment.penup()
        self.segment_turtles.append(segment)

    def _reset_round(self, message: str = "Game over! Press R to restart") -> None:
        self.state.high_score = max(self.state.high_score, self.state.score)
        self.state.reset_round()
        self.delay_ms = INITIAL_DELAY_MS
        self.head.goto(0, 0)
        for segment in self.segment_turtles:
            segment.hideturtle()
        self.segment_turtles.clear()
        self.head.setheading(0)
        self._draw_score()
        self.pen.goto(0, 230)
        self.pen.write(message, align="center", font=("Courier", 12, "normal"))
        self.pen.goto(0, 260)

    def restart(self) -> None:
        self.pen.clear()
        self.state.reset_round()
        self.delay_ms = INITIAL_DELAY_MS
        self.head.goto(0, 0)
        self.head.setheading(0)
        for segment in self.segment_turtles:
            segment.hideturtle()
        self.segment_turtles.clear()
        self._draw_score()

    def _tick(self) -> None:
        self.screen.update()
        if self.state.direction != "stop":
            old_positions = [(segment.xcor(), segment.ycor())
                             for segment in self.segment_turtles]
            for index in range(len(self.segment_turtles) - 1, 0, -1):
                self.segment_turtles[index].goto(*old_positions[index - 1])
            if self.segment_turtles:
                self.segment_turtles[0].goto(self.head.xcor(), self.head.ycor())

            next_position = self.state.move_head((self.head.xcor(), self.head.ycor()))
            self.head.goto(*next_position)

            x, y = next_position
            if abs(x) > BOUNDARY or abs(y) > BOUNDARY:
                self._reset_round()
            elif self.head.distance(self.food) < STEP:
                self.state.score += 10
                self.state.high_score = max(self.state.high_score, self.state.score)
                self._add_segment()
                occupied = set(self.state.segments)
                occupied.update((int(s.xcor()), int(s.ycor())) for s in self.segment_turtles)
                self.state.food = random_food_position(random, occupied)
                self.food.goto(*self.state.food)
                self.delay_ms = max(MIN_DELAY_MS, self.delay_ms - SPEEDUP_MS)
                self._draw_score()
            elif any(self.head.distance(segment) < STEP for segment in self.segment_turtles):
                self._reset_round()

        self.screen.ontimer(self._tick, self.delay_ms)

    def run(self) -> None:
        self._tick()
        self.screen.mainloop()


def main() -> None:
    SnakeGame().run()


if __name__ == "__main__":
    main()
