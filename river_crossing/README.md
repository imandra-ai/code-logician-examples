[Wolf, goat and cabbage problem](https://en.wikipedia.org/wiki/Wolf,_goat_and_cabbage_problem)

In `gen_w_query.iml`, with the existence of `List.for_all`, `List.exists`, and `List.find`, unrolling takes larger computational resources and Imandra cannot find the solution within the time limit (30 seconds).

In `gen_w_query_fixed.iml`, by replacing `List.for_all`, `List.exists`, and `List.find` with concrete expressions, Imandra can find the solution.