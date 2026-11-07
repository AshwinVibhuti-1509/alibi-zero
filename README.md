# ALIBI ZERO — Everyone Has a Story. One Doesn't Add Up.

#### Video Demo: https://youtu.be/v_LyXsfG9vw

## Description

ALIBI ZERO is a terminal-based detective game developed in Python as my final project for Harvard's CS50 Introduction to Programming with Python.

The game takes place in a fictional museum where a valuable diamond has disappeared. Four suspects provide statements describing their movements between different rooms. However, one of them claims to have completed a journey in less time than the museum's minimum required travel time.

The player's objective is to examine these statements, compare the timings with the museum map, and identify the inconsistent alibi.

Unlike a fixed puzzle with a predetermined answer, ALIBI ZERO generates randomized investigations. Each new game can feature different routes, departure times, arrival times, and an inconsistent suspect.

The game focuses on logical deduction and time calculations rather than establishing whether a fictional suspect actually committed the theft.

## Features

- **Randomized investigations:** Each round generates new suspect statements and travel times.
- **Four suspects:** Director, Guide, Security, and Visitor.
- **Museum map:** Displays the minimum travel time between connected rooms.
- **Evidence examination:** Players can inspect statements and revisit the map before making an accusation.
- **Alibi analysis:** The program identifies journeys that cannot be completed within the claimed duration.
- **One inconsistent alibi:** Every generated investigation is designed to contain exactly one impossible journey.
- **Answer explanation:** After an accusation, the game reveals the inconsistent suspect and explains the timing discrepancy.
- **Scoring:** Correct accusations earn 100 points; incorrect accusations earn zero.
- **Replay:** Players can start another investigation or return to the main menu.
- **Input validation:** Invalid menu selections and unrecognized suspect names are rejected.

## How to Play

Run the game and select **Start Investigation** from the main menu.

During an investigation, four options are available:

1. **Examine Suspects:** Read the statements containing starting locations, destinations, departure times, and arrival times.
2. **View Museum Map:** Check the minimum time required to travel between museum rooms.
3. **Make Accusation:** Select the suspect whose claimed journey is impossible.
4. **Exit Investigation:** Leave the current investigation without making an accusation.

To solve the mystery, calculate the time elapsed between each suspect's departure and arrival. Compare that duration with the minimum required travel time shown on the map.

If a suspect claims to have travelled in less than the minimum time, their alibi is inconsistent.

Only one accusation is permitted per investigation. After submitting an accusation, the program announces whether it was correct, reveals the actual inconsistent suspect, and explains the evidence.

The player can then start a new investigation or return to the main menu. Scores accumulate during the current game session.

## Project Structure

```text
project/
├── project.py
├── test_project.py
├── README.md
├── requirements.txt
└── data/
    └── cases.json
```

**`project.py`** contains the main game, including menu navigation, suspect statements, random case generation, scoring, and evidence validation.

**`test_project.py`** contains automated tests written with pytest to check important functions and expected behavior.

**`data/cases.json`** stores the museum's travel-time map, suspect information, and the original case description. The program uses this information to generate new investigations.

**`requirements.txt`** lists the Python packages needed for testing.

**`README.md`** explains the game's purpose, design, implementation, and usage.

## How the Investigation Engine Works

The investigation engine compares two values:

**Claimed travel time:** The difference between a suspect's departure and arrival timestamps.

**Required travel time:** The minimum duration stored in the museum's travel-time map.

For example, if a suspect claims to travel from Archive to Reception in 5 minutes, but the museum map specifies a minimum of 8 minutes, the statement is inconsistent by 3 minutes.

The function `calc_elapsed_time()` converts timestamps into minutes and calculates the elapsed duration. `get_travel_time()` retrieves the minimum duration for the route, supporting travel in either direction.

`check_alibi()` determines whether the claimed duration is sufficient, while `analyse_case()` examines every suspect and verifies that exactly one alibi is inconsistent.

This separation allows the same validation functions to work with both the original case data and newly generated investigations.

## Random Case Generation

The `generate_case()` function creates a new investigation by randomly selecting one suspect to receive an inconsistent statement.

For every suspect, the program randomly selects a route and generates departure and arrival times.

The selected inconsistent suspect receives a journey duration shorter than the minimum required time. The remaining suspects receive durations that meet or exceed their routes' minimum requirements.

New suspect dictionaries are collected into a list and placed inside a generated case dictionary. The original museum data is preserved.

Before returning the generated case, the program calls `analyse_case()` to verify that it contains exactly one inconsistent alibi.

This approach makes investigations replayable while maintaining a single logical solution.

## Installation and Usage

The game requires Python 3 and runs in a terminal.

From the project directory, install the testing dependency:

```bash
python -m pip install -r requirements.txt
```

Start the game:

```bash
python project.py
```

Run the automated tests:

```bash
python -m pytest test_project.py -v
```

The game itself uses Python's standard-library modules. Optional terminal characters and text-to-speech features were excluded from the final implementation.

## Testing

ALIBI ZERO uses pytest to verify individual functions independently.

The tests cover valid and invalid timestamps, elapsed-time calculations, impossible journeys, bidirectional route lookups, missing routes, accusation comparisons, and scoring.

The initial automated test suite successfully completed **21 tests**.

Additional tests are designed to check whether the investigation engine rejects cases with zero or multiple inconsistent suspects and whether randomized case generation preserves the museum data while producing valid investigations.

The expanded test suite should be run and its final result confirmed before submission.

Manual gameplay checks have also covered evidence examination, incorrect accusations, answer explanations, repeated investigations, returning to the main menu, and the How to Play instructions.

## Design Decisions

I chose a terminal-based interface to focus primarily on Python programming and problem-solving rather than graphical design.

JSON was selected because it provides a straightforward way to separate the museum data from the game's Python logic.

The game uses dictionaries to represent suspects and routes, lists to organize records, and separate functions for generating, displaying, and validating evidence.

I deliberately designed each investigation to contain exactly one inconsistent alibi so that players can reach a definite answer using logical reasoning.

The scoring and replay systems encourage players to complete multiple investigations without requiring them to restart the program.

## Limitations and Future Improvements

The current implementation assumes journeys occur within the same day and uses the 24-hour `HH:MM` format.

The museum map contains a predefined set of routes, and generated cases use these existing connections. The game does not calculate arbitrary shortest paths through a larger museum network.

Scores are maintained only during the current session and are not permanently saved.

Future improvements could include additional museum rooms, more complicated movement patterns, multiple difficulty levels, and persistent scores.

For this version, I prioritized a reliable, understandable, and replayable command-line experience.

## Final Note

ALIBI ZERO is a fictional logic game. An inconsistent statement represents a contradiction under the game's travel-time rules; it does not, by itself, establish guilt.

The project demonstrates Python concepts including functions, loops, conditionals, dictionaries, lists, file handling, randomization, exception handling, and automated testing.
