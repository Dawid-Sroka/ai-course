This repo contains my solutions to AI university course tasks.

The tasks in this course are toy problems, which purpose is to demonstrate classic problem-solving algorithms like BFS, Uniform Cost Search, heuristics, A*, inference
algorithms etc.

---

For each task sheet ("pracownia", directories p1, p2 etc.) there is a validator script `validator.py` or `validator2.py` etc. It requires `numpy`. 

The validator expects input/output files. You can create them by invoking script `create_io_files.sh`.

You can run tests for a solution by invoking for example: `python validator.py zad4 python zad4.py`. The `validator` program also has a `-h`/`--help` option.
