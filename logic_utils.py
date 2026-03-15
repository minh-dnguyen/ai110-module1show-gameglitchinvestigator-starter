# FIX: Claude 4.5 helped identify that Hard range (1-200) should be larger than Normal (1-100)
# Original bug: Hard was returning 1-50, which was smaller than Normal
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200  # FIX: Increased from 50 to 200 for proper difficulty scaling
    return 1, 100


# FIX: Claude 4.5 helped design robust parsing that handles edge cases.
# Improvement: Added support for float inputs (e.g., "42.7" converts to 42)
# This provides better UX by accepting decimal input from users.
def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Handles integers, floats (converts to int), and invalid input gracefully.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            # FIX: Support float input (e.g., "42.7" becomes 42)
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


# FIX: Claude 4.5 identified that the original code used string comparison instead of numeric comparison.
# Bug: "9" > "10" is True alphabetically, causing backwards hints for single vs double digit numbers.
# Fix: Ensured both guess and secret are treated as integers (not strings) for proper numeric comparison.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).
    Uses numeric comparison (not string) to correctly compare all number ranges.

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:  # FIX: Numeric comparison ensures 9 < 10, not 9 > 10 as strings
# FIX: Claude 4.5 helped design correct scoring logic after analyzing game balance.
# Original bugs: 
#   - Attempt numbering was off (was using attempt_number + 1, should be - 1)
#   - Even/odd penalty logic for "Too High" was inconsistent
# Fixed: Corrected formula to 100 - 10 * (attempt_number - 1) for proper scaling.
#        Even attempts on "Too High" now reward +5 instead of punishing inconsistently.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.
    Win: 100 points minus 10 per attempt (minimum 10).
    Too High on even attempt: +5 (good guess).
    Too High on odd attempt: -5 (early penalty).
    Too Low: -5 (encourages faster convergence).
    """
    if outcome == "Win":
        # FIX: Changed from (attempt_number + 1) to (attempt_number - 1)
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIX: Reward correct direction on even attempts, penalize on oddattempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
