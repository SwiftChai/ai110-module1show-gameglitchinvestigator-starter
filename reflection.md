## 1. What was broken when you started?

My first guess was 50 and the hints kept telling me to go lower. Even when I 
guessed 1, which should be the minimum allowed, it told me to go lower. The 
secret number was revealed to be 69, so the hint should have told me to go 
higher from the beginning. I expected that the hints would correctly guide me 
to the correct number.

For the second attempt, I clicked the "new game" button, but it would not 
restart. I had to close the game and start over. I expected that the game 
would take me to a new screen without crashing.

On the third attempt, my first guess was 75. I checked the "Developer Debug 
Info" and learned the secret number was 82. I intentionally chose a higher 
number of 90 and the game hinted that I should "go higher". The third attempt 
I chose 82. The game did tell me I won, but incorrectly recorded 4 attempts 
and despite winning, my score was -5. I expected to have a positive score.

---

## 2. How did you use AI as a teammate?

I used GitHub Copilot (Agent mode) and Claude as AI teammates on this project.

**Correct AI suggestion:**
Copilot suggested moving the pure logic functions — `get_range_for_difficulty`,
`parse_guess`, `check_guess`, and `update_score` — out of `app.py` and into a
separate `logic_utils.py` file, since none of them depend on Streamlit or 
session state. This was the right call. I verified it by running `pytest -v` 
after the refactor and confirming all four functions were importable and all 
tests passed. I also ran the game in the browser and confirmed the hints, 
scoring, and difficulty ranges all still worked correctly.

**Incorrect/misleading AI suggestion:**
When Copilot generated the `update_score` function in `logic_utils.py`, it 
used the formula `100 - 10 * (attempt_number + 1)` instead of 
`100 - 10 * attempt_number`. This introduced an off-by-one error. Because 
`st.session_state.attempts` is already incremented before `update_score` is 
called, the attempt number passed in is 1 on the first guess — adding `+1` 
again would make a first-guess win worth 80 points instead of 90. I caught 
this by comparing both versions side by side and tracing through the submit 
handler manually to confirm which formula matched how the function was 
actually being called.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when two things were true: the relevant pytest
test passed, and I could reproduce the original broken behavior in the game and
confirm it no longer happened.

**Test I ran:**
After fixing `update_score`, I ran a pytest unit test that called the function
directly with `attempt_number=1` and `outcome="Win"` and asserted the returned 
score was `0 + 90 = 90`. The test failed initially with the AI-generated `+1` 
formula (returning 80), which confirmed the bug. After correcting the formula, 
the test passed. I also manually played a game, won on the first guess, and 
verified the score displayed as 90 in the UI.

I also hit a `ModuleNotFoundError` when first running pytest because the tests
lived in a `tests/` subfolder and Python couldn't find `logic_utils.py` in the
root. Claude helped me understand that adding an empty `conftest.py` to the 
project root fixes this — pytest uses it as a signal to add that directory to 
Python's path. Once I added it, all tests collected and ran correctly.

**AI help with tests:**
Claude suggested the specific edge cases to test for each function — for 
example, testing that `parse_guess` handles `None`, empty string, a float 
like `"3.7"`, and a non-numeric string like `"abc"`. This helped me see that 
testing edge cases is just as important as testing the happy path.

---

## 4. What did you learn about Streamlit and state?

SStreamlit reruns the whole script every time you click a button or type 
something. That means any regular variable just resets to zero each time, 
which is why the score and attempts kept breaking.

Session state is how you fix that. Think of it like a sticky note Streamlit 
keeps on the side; anything you save to `st.session_state` survives the 
rerun. That is how the game remembers your score, your guess history, and 
the secret number between clicks.
---

## 5. Looking ahead: your developer habits

**Habit I want to reuse:**
Always trace through the call site before trusting a refactored function. The 
off-by-one bug in `update_score` only became visible when I looked at *where*
and *how* the function was being called in `app.py`, not just at the function 
itself. That habit — checking the context around a function, not just the 
function is something I will carry into every future project.

**What I would do differently:**
Next time I would ask the AI to explain *why* it made a change, not just 
*what* it changed. If I had asked Copilot to explain the `+1` in the formula, 
I likely would have caught the mistake before running any tests at all.

**How this changed my thinking:**
This project showed me that AI-generated code needs the same careful review 
as code written by anyone else — the bugs are just more subtle because the 
code *looks* clean and confident. AI should be a considered fast starting point, not a finished 
answer.