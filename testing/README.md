# Testing
This directory contains all testing results. Directories are titled by the used solver. `opt` is added if a search for an optimal solution was performed.
All encodings correctly returned UNSAT on `straight_map.pkl`, `3x4x1-infLoop.pkl` and `4xx3x1-no_exit.pkl` instances and ran out of memory (32GB) during grounding on `20x20x1-snake.pkl`.