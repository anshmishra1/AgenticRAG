"""Pipeline timing and performance instrumentation."""

from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class PerformanceTracker:
    """Collect execution time for every pipeline stage invocation."""

    stages: dict[str, list[float]] = field(default_factory=dict)

    @contextmanager
    def measure(self, name: str):
        """Measure one execution of a pipeline stage."""

        start = time.perf_counter()

        try:
            yield
        finally:
            elapsed = time.perf_counter() - start

            self.stages.setdefault(name, []).append(elapsed)

            print(
                f"[TIMING] {name:<30} "
                f"{elapsed:>8.2f} sec"
            )

    @property
    def total_time(self) -> float:
        """Total measured execution time across all stage invocations."""

        return sum(
            elapsed
            for timings in self.stages.values()
            for elapsed in timings
        )

    def stage_total(self, name: str) -> float:
        """Return total time spent in a specific stage."""

        return sum(self.stages.get(name, []))

    def stage_calls(self, name: str) -> int:
        """Return number of times a stage was executed."""

        return len(self.stages.get(name, []))

    def summary(self) -> None:
        """Print a complete performance summary."""

        print("\n" + "=" * 70)
        print("PERFORMANCE SUMMARY")
        print("=" * 70)

        for name, timings in self.stages.items():
            total = sum(timings)
            calls = len(timings)

            percentage = (
                total / self.total_time * 100
                if self.total_time
                else 0
            )

            print(
                f"{name:<30}"
                f"{total:>8.2f} sec "
                f"({percentage:>5.1f}%) "
                f"[{calls} call(s)]"
            )

            # Show individual executions when a stage runs more than once.
            if calls > 1:
                for index, elapsed in enumerate(timings, start=1):
                    print(
                        f"    └─ Run #{index:<22}"
                        f"{elapsed:>8.2f} sec"
                    )

        print("-" * 70)

        print(
            f"{'TOTAL':<30}"
            f"{self.total_time:>8.2f} sec"
        )

        if self.stages:
            bottleneck = max(
                self.stages,
                key=self.stage_total,
            )

            print(
                f"\nBOTTLENECK: {bottleneck}"
            )

            print(
                f"BOTTLENECK TIME: "
                f"{self.stage_total(bottleneck):.2f} sec"
            )

        print("=" * 70)


def main():
    tracker = PerformanceTracker()

    with tracker.measure("query_prep"):
        time.sleep(0.05)

    with tracker.measure("embedding_generation"):
        time.sleep(0.20)

    with tracker.measure("vector_db_search"):
        time.sleep(0.45)

    with tracker.measure("post_processing"):
        time.sleep(0.02)

    tracker.summary()


if __name__ == "__main__":
    main()