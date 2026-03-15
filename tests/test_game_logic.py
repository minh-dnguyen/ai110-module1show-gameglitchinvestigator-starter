from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "🎉" in message

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# ===== TESTS FOR BUG FIX: Lexicographic comparison (high/low bug) =====
def test_check_guess_boundary_single_digits():
    """
    Bug fix test: String comparison would make "9" > "10" = True (alphabetically).
    With correct numeric comparison, 9 < 10 should return "Too Low".
    """
    outcome, message = check_guess(9, 10)
    assert outcome == "Too Low", "Single digit should be lower than double digit numerically"
    assert "HIGHER" in message


def test_check_guess_boundary_teens():
    """
    Bug fix test: String comparison would fail on two-digit comparisons.
    15 > 100 should be False, returning "Too Low".
    """
    outcome, message = check_guess(15, 100)
    assert outcome == "Too Low", "15 should be less than 100 numerically"
    assert "HIGHER" in message


def test_check_guess_edge_cases():
    """
    Bug fix test: Test minimum and maximum range values.
    """
    # Test at minimum range (Easy: 1-20)
    outcome, _ = check_guess(1, 1)
    assert outcome == "Win"
    
    outcome, _ = check_guess(2, 1)
    assert outcome == "Too High"
    
    # Test at maximum range (Hard: 1-200)
    outcome, _ = check_guess(200, 200)
    assert outcome == "Win"
    
    outcome, _ = check_guess(199, 200)
    assert outcome == "Too Low"
    
    outcome, _ = check_guess(201, 200)
    assert outcome == "Too High"


def test_check_guess_no_type_coercion():
    """
    Bug fix test: Verify that no type coercion is happening.
    The original bug converted secret to string on even attempts.
    This test ensures comparisons work consistently.
    """
    secret = 42
    
    # Test several guesses against same secret
    assert check_guess(41, secret)[0] == "Too Low"
    assert check_guess(42, secret)[0] == "Win"
    assert check_guess(43, secret)[0] == "Too High"
    
    # Repeat to ensure no state changes
    assert check_guess(41, secret)[0] == "Too Low"
    assert check_guess(43, secret)[0] == "Too High"


# ===== TESTS FOR parse_guess =====
def test_parse_guess_valid_integer():
    """Test parsing valid integer input."""
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_float_input():
    """Test parsing float input (should convert to int)."""
    ok, value, err = parse_guess("42.7")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_empty_string():
    """Test empty string input."""
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert "Enter a guess" in err


def test_parse_guess_none():
    """Test None input."""
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert "Enter a guess" in err


def test_parse_guess_invalid_input():
    """Test invalid non-numeric input."""
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert "not a number" in err


# ===== TESTS FOR update_score =====
def test_update_score_win_first_attempt():
    """
    Bug fix test: Score calculation was 100 - 10 * (attempt_number + 1).
    Should be 100 - 10 * (attempt_number - 1).
    First attempt win should give 100 points.
    """
    score = update_score(0, "Win", attempt_number=1)
    assert score == 100, "First attempt win should award 100 points, not 80"


def test_update_score_win_second_attempt():
    """Second attempt win should give 90 points."""
    score = update_score(0, "Win", attempt_number=2)
    assert score == 90


def test_update_score_win_many_attempts():
    """Multiple attempts should decrease points correctly."""
    score = update_score(0, "Win", attempt_number=8)
    assert score == 30


def test_update_score_win_minimum_points():
    """Score should not go below 10 points."""
    score = update_score(0, "Win", attempt_number=20)
    assert score >= 10, "Score should have minimum of 10 points"


def test_update_score_too_high_even_attempt():
    """"Too High" on even attempt should add 5 points."""
    score = update_score(100, "Too High", attempt_number=2)
    assert score == 105


def test_update_score_too_high_odd_attempt():
    """'Too High' on odd attempt should subtract 5 points."""
    score = update_score(100, "Too High", attempt_number=3)
    assert score == 95


def test_update_score_too_low():
    """'Too Low' should always subtract 5 points."""
    score = update_score(100, "Too Low", attempt_number=2)
    assert score == 95
    
    score = update_score(100, "Too Low", attempt_number=3)
    assert score == 95


# ===== TESTS FOR get_range_for_difficulty =====
def test_get_range_easy():
    """Easy difficulty should be 1-20."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_get_range_normal():
    """Normal difficulty should be 1-100."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_get_range_hard():
    """
    Bug fix test: Hard was 1-50 (easier than Normal!).
    Should be 1-200 for actual difficulty progression.
    """
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200, "Hard difficulty should be 1-200, not 1-50"
    assert high > 100, "Hard should have larger range than Normal"


def test_get_range_default():
    """Unknown difficulty should default to Normal (1-100)."""
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100
