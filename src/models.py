# -------------------- IMPORTS --------------------
from datetime import datetime, timedelta
from dataclasses import dataclass


# -------------------- CLASSES --------------------
@dataclass
class TimerModel:
    start_time: datetime = datetime.now()
    memory_time: timedelta = timedelta()
    total_time: timedelta = timedelta()
    paused: bool = True

    @property
    def remaining_time(self) -> timedelta:
        """Returns the amount of time to display as a timedelta.

        Returns:
            timedelta: the amount of remaining time.
        """
        if self.paused:
            return self.memory_time
        else:
            return self.start_time + self.memory_time - datetime.now()

    def run(self) -> None:
        """Counts a duration by now.
        """
        self.start_time = datetime.now()
        self.paused = False

    def pause(self) -> None:
        """Stops counting duration, saving actual duration
        """
        self.memory_time = self.remaining_time
        self.paused = True

    def reset(self) -> None:
        """Resets the timer

        Returns:
            None
        """
        self.start_time = datetime.now()
        self.memory_time = timedelta()
        self.total_time = timedelta()
        self.paused = True

    def add_time(self, seconds: int|float) -> None:
        """Adjusts the timer duration

        Args:
            seconds: (int|float): the amount of time to increase / decrease.
        """
        if self.total_time + timedelta(seconds=seconds) > timedelta():
            self.total_time += timedelta(seconds=seconds)
        else:
            self.total_time = timedelta()
        self.memory_time = self.total_time


@dataclass
class ChronoModel:
    start_time: datetime = datetime.now()
    memory_time: timedelta = timedelta()
    paused: bool = True

    @property
    def elapsed_time(self) -> timedelta:
        """Returns the durtion between start and now, considering pauses.

        Returns:
            timedelta: the amount of elapsed time.
        """
        if self.paused:
            return self.memory_time
        else:
            return datetime.now() - self.start_time + self.memory_time

    def run(self) -> None:
        """Counts a duration by now.
        """
        self.start_time = datetime.now()
        self.paused = False

    def pause(self) -> None:
        """Stops counting duration, saving actual duration.
        """
        self.memory_time = self.elapsed_time
        self.paused = True

    def reset(self) -> None:
        """Resets the chrono.
        """
        self.start_time = datetime.now()
        self.memory_time = timedelta()
        self.paused = True
