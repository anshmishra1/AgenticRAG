from agentic_rag.graph.edges import route_after_grading, route_after_hallucination_check


def test_route_after_grading_relevant_goes_to_generate():
    assert route_after_grading({"relevance_grade": "relevant", "retry_count": 0}) == "generate"


def test_route_after_grading_irrelevant_triggers_rewrite():
    assert route_after_grading({"relevance_grade": "irrelevant", "retry_count": 0}) == "rewrite_query"


def test_route_after_grading_gives_up_after_max_retries():
    assert route_after_grading({"relevance_grade": "irrelevant", "retry_count": 2}) == "generate"


def test_route_after_hallucination_check_grounded_ends():
    assert route_after_hallucination_check({"hallucination_grade": "grounded", "retry_count": 0}) == "end"


def test_route_after_hallucination_check_regenerates_on_failure():
    assert route_after_hallucination_check({"hallucination_grade": "hallucinated", "retry_count": 0}) == "generate"
