from __future__ import annotations
from threading import Timer
from time import perf_counter
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from loguru import Logger
    from kans import TaskBase


class HeartBeatTask:

    def __init__(self, logger: Logger, task: TaskBase) -> None:
        self._logger = logger
        self._task = task
        self._timer: Timer = Timer(self.task.first_delay, self.get_task())

    def start(self) -> None:
        self._timer.start()

    def cancel(self) -> None:
        self._timer.cancel()

    def get_task(self) -> Callable[..., None]:
        def run() -> None:
            t1 = perf_counter()
            self._task.run()
            self._logger.debug(f"Task {self.task.name} took {perf_counter() - t1:.2f} seconds")
            self._reschedule()
        return run

    def _reschedule(self) -> None:
        self._timer = Timer(self.task.interval, self.get_task())
        self._timer.start()

    @property
    def task(self) -> TaskBase:
        return self._task
