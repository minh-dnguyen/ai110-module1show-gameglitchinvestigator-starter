# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

* Attempts starts at 7 when open the game
* Keep showing go higher even when at maximum value or go lower when at minimum value
* Score calculated incorrectly

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

* The hints were backwards

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

* Claude 4.5 (via GitHub Copilot)

**Example 1: Correct AI Suggestion ✓**

- **What Claude suggested:** The Hard difficulty range in `get_range_for_difficulty()` was returning (1, 50), which is smaller than Normal (1, 100). Claude identified that Hard should have a larger range to actually be harder. The fix was to change Hard from 1-50 to 1-200.
- **Was it correct?** Yes, completely correct. This follows proper game design: Easy (1-20) < Normal (1-100) < Hard (1-200) create increasing difficulty.
- **How I verified it:** I ran the game on each difficulty and confirmed the range display in the sidebar was logically ordered. I also added specific test cases (`test_check_guess_edge_cases()`) that verify boundary conditions at 1, 200, 199, 201 all work correctly.

**Example 2: Misleading/Incorrect AI Suggestion ✗**

- **What Claude suggested:** When diagnosing the "backwards hints" bug where the game would say "go higher" even at maximum values, Claude initially suggested modifying the attempt counter logic. However, Claude later caught that the **real bug was in `check_guess()`** using string comparison instead of numeric comparison. The fix was not in attempts—it was ensuring guess and secret were always compared as integers, not strings.
- **Was it incorrect?** Partially misleading at first. Claude was on the wrong track initially but self-corrected when analyzing the test failures.
- **How I verified it:** I created specific test cases like `test_check_guess_boundary_single_digits()` which shows that with string comparison "9" > "10" (False alphabetically), but numerically 9 < 10 (True). Running pytest showed that with numeric comparison, all 21 tests pass, including edge cases like comparing 9 vs 10, 15 vs 100, and 199 vs 200. The game now gives correct hints.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I used a combination of manual testing and automated pytest tests. For each bug, I verified the fix by:

1. **Manual testing in the game UI:** Running the Streamlit app, trying each difficulty, and checking that hints were correct and attempts counted properly.
2. **Automated testing with pytest:** Created comprehensive test cases that cover edge cases, boundary conditions, and specific bug scenarios.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

**Test: `test_check_guess_boundary_single_digits()`** This test checks that when guess=9 and secret=10, the outcome is "Too Low" (not "Too High"). With the string comparison bug, "9" > "10" alphabetically would be False, but the bug was causing backwards direction hints. This test confirmed the numeric comparison fix works: 9 < 10 numerically returns "Too Low" correctly. Running `pytest tests/test_game_logic.py` showed 21 tests passing, including edge cases with 1, 200, 199, 201, and repeated guesses against the same secret.

- Did AI help you design or understand any tests? How?

Yes. Claude 4.5 helped me design the test suite strategy: (1) Create boundary tests for the bug scenarios (single vs double digits), (2) Test consistency by guessing multiple times against the same secret, (3) Verify that no type coercion or state mutation happens. Claude also helped me understand why those test cases would catch the specific bugs (e.g., string comparison would fail on single-digit boundaries). This systematic testing approach revealed that all 21 tests pass, confirming the fixes are robust.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
