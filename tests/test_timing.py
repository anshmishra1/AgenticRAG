import pytest

from agentic_rag.core.timing import PerformanceTracker


def test_performance_tracker_records_stage():
    tracker = PerformanceTracker()

    with tracker.measure("test_stage"):
        pass

    assert tracker.stage_calls("test_stage") == 1
    assert tracker.stage_total("test_stage") >= 0
    assert tracker.total_time >= 0


def test_performance_tracker_accumulates_calls():
    tracker = PerformanceTracker()

    with tracker.measure("test_stage"):
        pass

    with tracker.measure("test_stage"):
        pass

    assert tracker.stage_calls("test_stage") == 2
    assert tracker.stage_total("test_stage") >= 0
    assert tracker.total_time == pytest.approx(
        tracker.stage_total("test_stage")
    )
