"""Decision logic for the RAG pipeline: thresholds, heuristics, and the
classification/routing rules built on top of them.

Split by concern, not by graph node:
  - retrieval.py   - is retrieval evidence strong enough to skip grading?
  - generation.py  - context/history budgets, refusal-answer detection.

Values (thresholds, limits) live in config.py as the single source of tunable
numbers. Modules in this package hold the LOGIC that interprets those values -
pure functions, no LLM calls, no I/O - so they're unit-testable in isolation
and there's one place to look when tuning behavior, instead of hunting through
nodes.py / edges.py / query_utils.py / vectorstore.py for scattered constants.
"""