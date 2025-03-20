# -------------------- IMPORTS --------------------
import winsound

from .models import *
from .views import *
        
        
# -------------------- CLASSES --------------------
class ApplicationController:
    def __init__(self) -> None:
        """Builds the application.
        """
        self.view = ApplicationView(self)
        self.type_app = None
        self.view.launch_app()

    def build_one_chrono(self) -> None:
        """Builds a chrono.
        """
        self.view.hide_menu()
        self.type_app = ChronoController(self)

    def build_mlt_chrono(self) -> None:
        """Builds an aleternate multichrono.
        """
        self.view.hide_menu()
        self.type_app = MultiChronoController(self, nb_chronos=self.view.nb_mlt_chronos)

    def build_one_timer(self) -> None:
        """Builds a timer.
        """
        self.view.hide_menu()
        self.type_app = TimerController(self)

    def build_mlt_timer(self) -> None:
        """Builds 2 timers, the second one counts 4/3 the other.
        """
        self.view.hide_menu()
        self.type_app = MultiTimerController(self)

    def build_sim_chronos(self):
        """Builds a simultaneous multichrono.
        """
        self.view.hide_menu()
        self.type_app = SimultaneousChronoController(self, nb_chronos=self.view.nb_sim_chronos)

    def reset_application(self) -> None:
        """Resets the application, displaying the main menu.
        """
        self.view.show_menu()


class SimultaneousChronoController:
    def __init__(self, application: ApplicationController, nb_chronos: int) -> None:
        """Builds a multiple chrono controller, which controls views (in views.py) and models (in models.py).

        Args:
            application (ApplicationController): the application containing the instance.
            nb_chronos (int): the amount of chrono to bulid (from 2 to 16).
        """
        self.application = application
        self.nb_chronos = nb_chronos
        self.view = SimultaneousChronoView(self, self.nb_chronos)
        self.models = []
        for i in range(self.nb_chronos):
            self.models.append(ChronoModel())

    def pause_all(self) -> None:
        """Runs one chrono and pauses all the others.
        """
        self.view.pause_all()
        for chrono in self.models:
            chrono.pause()

    def reset_all(self) -> None:
        """Runs one chrono and pauses all the others.
        """
        self.view.reset_all()
        for chrono in self.models:
            chrono.reset()

    def run_all(self) -> None:
        """Pauses all the chronos.
        """
        self.view.run_all()
        for chrono in self.models:
            if chrono.paused:
                chrono.run()
        self.update_every_60ms()

    def pause_one(self, index: int) -> None:
        """Runs one chrono and pauses all the others.

        Args:
            index (int): which chrono to pause.
        """
        self.models[index].pause()
        self.view.pause_one(index)
        all_paused = True
        for model in self.models:
            if not model.paused:
                all_paused = False
        if all_paused:
            self.view.pause_all()

    def run_one(self, index: int) -> None:
        """Pauses all the chronos.
        """
        self.models[index].run()
        self.view.run_one(index)
        self.update_every_60ms()
        all_running = True
        for model in self.models:
            if model.paused:
                all_running = False
        if all_running:
            self.view.run_all()

    def reset_one(self, index: int) -> None:
        """Disables the PAUSE button of the selected chrono.

        Args:
           index (int): which chrono to reset.
        """
        self.models[index].reset()
        self.view.reset_one(index)
        self.update_every_60ms()

    def display_value(self, index) -> None:
        """Calls the method to display the time value in the view (binding model and view), as a str.
        """
        time_value = format_time_str(self.models[index].elapsed_time)
        self.view.update_display(index, time_value)

    def update_every_60ms(self) -> None:
        """Calls the method to update the time value in the view every 60 ms (binding model and view).
        """
        for index in range(len(self.models)):
            self.display_value(index)
        self.view.update_every_60ms()

    def destroy(self) -> None:
        """Destroys the app and goes to menu.
        """
        self.view.delete()
        del self.models
        self.application.reset_application()
        del self


class MultiTimerController:
    def __init__(self, application: ApplicationController) -> None:
        """Builds a timer controller, which controls a view (in views.py) and a model (in models.py). The second timer
        is 4/3 longer than the other.

        Args:
            application (ApplicationController): the application containing the instance.
        """
        self.application = application
        self.view = MultiTimerView(self, NUMBER)
        self.models = [TimerModel() for _ in range(NUMBER)]
        self.allow_rings = [False for _ in range(NUMBER)]
        self.change_time(0)

    def run(self) -> None:
        """On user command, runs all the timers, disables run button and enables other buttons.
        """
        for model in self.models:
            model.run()
        self.view.run()
        self.update_every_60ms()

    def pause(self) -> None:
        """On user command, pauses all the timers, disables pause button and enables other buttons.
        """
        for model in self.models:
            model.pause()
        self.view.pause()

    def reset(self) -> None:
        """On user command, resets all the timers, disables reset button and enables other buttons.
        """
        for index, model in enumerate(self.models):
            model.reset()
            self.allow_rings[index] = False
        self.view.reset()

    def change_time(self, minutes: int | float) -> None:
        """Adds an amount of time (positive or negative) to every timer. Be careful to the coefficient.

        Args:
            minutes (int|float): amount of time to add to the timer.
        """
        for index, timer in enumerate(self.models):
            if index % 2:
                timer.add_time(60 * minutes * COEFFICIENT)
            else:
                timer.add_time(60 * minutes)
            self.allow_rings[index] = True
        self.display_values()

    def display_values(self) -> None:
        """Calls the method to display the time value in all the timers of the view (binding models and views), as str.
        """
        values_and_percents = []
        for model in self.models:
            time_value = format_time_str(model.remaining_time)
            percent = format_time_percent(model.remaining_time, model.total_time)
            if percent < 0:
                percent = 0
                time_value = format_time_str(timedelta())
            values_and_percents.append((time_value, percent))
        self.view.update_display(values_and_percents)

    def update_every_60ms(self) -> None:
        """Calls the method to update the time values in the view every 60 ms (binding models and views).
        """
        self.display_values()
        if self.models:
            for index, model in enumerate(self.models):
                if model.remaining_time <= timedelta():
                    if self.allow_rings[index]:
                        play_alarm_WAV()
                        self.allow_rings[index] = False
            self.view.update_every_60ms()

    def destroy(self) -> None:
        """Destroys the app and goes to menu.
        """
        self.view.delete()
        del self.models
        self.application.reset_application()
        del self


class MultiChronoController:
    def __init__(self, application: ApplicationController, nb_chronos: int) -> None:
        """Builds a multiple chrono controller, which controls views (in views.py) and models (in models.py).

        Args:
            application (ApplicationController): the application containing the instance.
            nb_chronos (int): the amount of chrono to bulid (from 2 to 10).
        """
        self.application = application
        self.nb_chronos = nb_chronos
        self.view = MultiChronoView(self, self.nb_chronos)
        self.models = [ChronoModel() for number in range(self.nb_chronos)]

    def run(self, index) -> None:
        """Runs one chrono and pauses all the others.

        Args:
            index (int): which chrono to run.
        """
        self.pause()
        self.models[index].run()
        self.view.run(index)
        self.update_every_60ms()

    def pause(self) -> None:
        """Pauses all the chronos.
        """
        self.view.pause()
        for chrono in self.models:
            chrono.pause()

    def reset(self) -> None:
        """Resets all the chronos.
        """
        self.view.reset()
        for chrono in self.models:
            chrono.reset()

    def display_value(self, index: int) -> None:
        """Calls the method to display the time value in the view (binding model and view), as a str.

        Args:
            index (int): which chrono to display.
        """
        time_value = format_time_str(self.models[index].elapsed_time)
        self.view.update_display(index, time_value)

    def update_every_60ms(self) -> None:
        """Calls the method to update the time value in the view every 60 ms (binding model and view).
        """
        for index in range(len(self.models)):
            self.display_value(index)
        self.view.update_every_60ms()

    def destroy(self) -> None:
        """Destroys the app and goes to menu.
        """
        self.view.delete()
        del self.models
        self.application.reset_application()
        del self


class TimerController:
    def __init__(self, application: ApplicationController, coefficient: float = 1) -> None:
        """Builds a timer controller, which controls a view (in views.py) and a model (in models.py). The coefficient
        is used to calculate the increase of time.

        Args:
            application (ApplicationController): the application containing the instance.
            coefficient (float): the multiplier for time to add.
        """
        self.application = application
        self.coefficient = coefficient
        self.view = TimerView(self)
        self.model = TimerModel()
        self.change_time(0)
        self.allow_ring = False

    def run(self) -> None:
        """On user command, runs the timer, disables run button and enables other buttons.
        """
        self.view.run()
        self.model.run()
        self.update_every_60ms()

    def pause(self) -> None:
        """On user command, pauses the chrono, disables pause button and enables other buttons.
        """
        self.view.pause()
        self.model.pause()
        self.display_value()

    def reset(self) -> None:
        """On user command, resets the chrono, disables reset button and enables other buttons.
        """
        self.view.reset()
        self.model.reset()
        self.display_value()
        self.change_time(0)
        self.allow_ring = False

    def change_time(self, minutes: int | float) -> None:
        """Adds an amount of time (positive or negative) to the timer

        Args:
            minutes (int|float): time to add to the timer.
        """
        self.model.add_time(60 * minutes * self.coefficient)
        self.allow_ring = True
        self.display_value()

    def display_value(self) -> None:
        """Calls the method to display the time value in the view (binding model and view), as a str.
        """
        time_value = format_time_str(self.model.remaining_time)
        percent = format_time_percent(self.model.remaining_time, self.model.total_time)
        if percent < 0:
            percent = 0
            time_value = format_time_str(timedelta())
            self.view.update_display(time_value, percent)
            return
        self.view.update_display(time_value, percent)

    def update_every_60ms(self) -> None:
        """Calls the method to update the time value in the view every 60 ms (binding model and view).
        """
        self.display_value()
        if self.model.remaining_time <= timedelta():
            if self.allow_ring:
                play_alarm_WAV()
        else:
            self.view.update_every_60ms()

    def destroy(self) -> None:
        """Destroys the app and goes to menu.
        """
        self.view.delete()
        del self.model
        self.application.reset_application()
        del self


class ChronoController:
    def __init__(self, application: ApplicationController) -> None:
        """Builds a chrono controller, which controls a view (in views.py) and a model (in models.py).

        Args:
            application (ApplicationController): the application containing the instance.
        """
        self.application = application
        self.view = ChronoView(self)
        self.model = ChronoModel()

    def run(self) -> None:
        """On user command, runs the chrono, disables run button and enables other buttons.
        """
        self.view.run()
        self.model.run()
        self.update_every_60ms()

    def pause(self) -> None:
        """On user command, pauses the chrono, disables pause button and enables other buttons.
        """
        self.view.pause()
        self.model.pause()
        self.display_value()

    def reset(self) -> None:
        """On user command, resets the chrono, disables reset button and enables other buttons.
        """
        self.view.reset()
        self.model.reset()
        self.display_value()

    def display_value(self):
        """Calls the method to display the time value in the view (binding model and view), as a str.
        """
        time_value = format_time_str(self.model.elapsed_time)
        self.view.update_display(time_value)

    def update_every_60ms(self) -> None:
        """Calls the method to update the time value in the view every 60 ms (binding model and view).
        """
        self.display_value()
        self.view.update_every_60ms()

    def destroy(self) -> None:
        """Destroys the app and goes to menu.
        """
        self.view.delete()
        del self.model
        self.application.reset_application()
        del self


# -------------------- FUNCTIONS --------------------
def format_time_str(value: timedelta) -> str:
    """Formats a timedelta value as a str : {h}:{mm}:{ss}.{µ} or {mm}:{ss}.{µ}, depending on value (> or < 1 hour).

    Args:
        value (timedelta): the timedelta to convert to string.

    Returns:
        str: the timedelta, converted to a string.
    """
    if value >= timedelta(hours=1):
        return "{:01d}:{:02d}:{:02d}.{}".format(
            value.seconds // 3600,
            (value.seconds // 60) % 60,
            value.seconds % 60,
            value.microseconds // 100000,
        )
    else:
        return "{:02d}:{:02d}.{}".format(
            (value.seconds // 60) % 60,
            value.seconds % 60,
            value.microseconds // 100000,
        )


def format_time_percent(value: timedelta, total: timedelta) -> float:
    """Formats a timedelta percentage as a float.

    Args:
        value (timedelta): the counted time.
        total: (timedelta): the total time.

    Returns:
        float: the percentage of the timedelta.
    """
    if total == timedelta():
        return 0
    return value / total


def play_alarm_WAV() -> None:
    """Plays a .WAV file, but allows user to click thanks to SND_ASYNC.
    """
    winsound.PlaySound(str(ALARM), winsound.SND_FILENAME | winsound.SND_ASYNC)
