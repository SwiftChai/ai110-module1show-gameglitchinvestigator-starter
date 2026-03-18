import pytest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_get_range_for_difficulty_values_and_default():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 500)
    assert get_range_for_difficulty("Extreme") == (1, 100)


def test_parse_guess_expected_behaviors():
    assert parse_guess(None) == (False, None, "Enter a guess.")
    assert parse_guess("") == (False, None, "Enter a guess.")

    assert parse_guess("abc") == (False, None, "That is not a number.")
    assert parse_guess("!") == (False, None, "That is not a number.")

    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("3.7") == (True, 3, None)
    assert parse_guess("-5") == (True, -5, None)


def test_check_guess_outcomes_and_string_secret():
    outcome, _ = check_guess(25, 25)
    assert outcome == "Win"

    outcome, _ = check_guess(30, 25)
    assert outcome == "Too High"

    outcome, _ = check_guess(20, 25)
    assert outcome == "Too Low"

    outcome, _ = check_guess(25, "25")
    assert outcome == "Win"


def test_update_score_rules_for_win_hints_and_unknown_outcome():
    assert update_score(0, "Win", 1) == 90
    assert update_score(0, "Win", 9) == 10
    assert update_score(0, "Win", 15) == 10

    assert update_score(100, "Too High", 3) == 105
    assert update_score(100, "Too Low", 3) == 95

    assert update_score(42, "Something Else", 4) == 42


def test_logic_utils_direct_imports_do_not_raise_importerror():
    try:
        from logic_utils import (
            check_guess,
            get_range_for_difficulty,
            parse_guess,
            update_score,
        )
    except ImportError as exc:
        pytest.fail(f"ImportError while importing logic_utils functions: {exc}")

    assert callable(check_guess)
    assert callable(get_range_for_difficulty)
    assert callable(parse_guess)
    assert callable(update_score)
