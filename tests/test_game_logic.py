import random
import pytest

from snake import GameState, random_food_position


def test_direction_prevents_reverse_turn():
    state = GameState(direction="right")
    state.set_direction("left")
    assert state.direction == "right"
    state.set_direction("up")
    assert state.direction == "up"


def test_move_head_uses_twenty_pixel_grid():
    state = GameState(direction="up")
    assert state.move_head((0, 0)) == (0, 20)


def test_reset_round_preserves_high_score():
    state = GameState(score=30, high_score=50, direction="left",
                      segments=[(20, 0)], game_over=True)
    state.reset_round()
    assert state.score == 0
    assert state.high_score == 50
    assert state.direction == "stop"
    assert state.segments == []
    assert state.game_over is False


def test_invalid_direction_is_rejected():
    with pytest.raises(ValueError):
        GameState().set_direction("diagonal")


def test_food_is_not_placed_on_occupied_cell():
    rng = random.Random(7)
    occupied = {(x, y) for x in range(-280, 281, 20)
                for y in range(-280, 281, 20)}
    occupied.remove((20, 40))
    assert random_food_position(rng, occupied) == (20, 40)
