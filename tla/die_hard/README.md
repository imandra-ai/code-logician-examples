Die Hard Water Jug Puzzle Solver

This module implements the famous water jug puzzle from the movie "Die Hard 3",
where John McClane and Zeus Carver must disarm a bomb by placing exactly 4 gallons
of water on a scale. They have:
- A 5-gallon jug
- A 3-gallon jug
- A water fountain

They can perform the following actions:
- Fill up the 5-gallon jug from the water fountain
- Fill up the 3-gallon jug from the water fountain
- Empty the 5-gallon jug
- Empty the 3-gallon jug
- Pour water from the 5-gallon jug to the 3-gallon jug
- Pour water from the 3-gallon jug to the 5-gallon jug

We are interested in finding a sequence of actions that leads to the solution state.
Also, we want to prove that there is no solution with less than 3 steps.


reference: https://github.com/tlaplus/Examples/tree/master/specifications/DieHard