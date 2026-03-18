import pytest
from logic_utils import check_guess


@pytest.mark.parametrize(
    "guess,target,expected_outcome,required_word,forbidden_word",
    [
        (25, 50, "Too Low", "HIGHER", "LOWER"),
        (75, 50, "Too High", "LOWER", "HIGHER"),
    ],
)
def test_app_hint_direction_matches_guess_relation(
    guess, target, expected_outcome, required_word, forbidden_word
):
    outcome, message = check_guess(guess, target)

    assert outcome == expected_outcome
    assert required_word in message
    assert forbidden_word not in message


def test_app_correct_guess_has_no_directional_hint():
    outcome, message = check_guess(50, 50)

    assert outcome == "Win"
    assert "HIGHER" not in message
    assert "LOWER" not in message
