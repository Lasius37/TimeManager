# -------------------- IMPORTS --------------------
from tkinter import *
from .constants import *


# -------------------- CLASSES --------------------
class AssetsManager:
    def __init__(self, view):
        if isinstance(view, SimultaneousChronoView):
            self.home_img = PhotoImage(file=HOME).subsample(2)
            self.run_img = PhotoImage(file=RUN).subsample(2)
            self.pause_img = PhotoImage(file=PAUSE).subsample(2)
            self.reset_img = PhotoImage(file=RESET).subsample(2)
    
        elif isinstance(view, MultiTimerView):
            self.home_img = PhotoImage(file=HOME).subsample(1)
            self.run_img = PhotoImage(file=RUN).subsample(1)
            self.pause_img = PhotoImage(file=PAUSE).subsample(1)
            self.reset_img = PhotoImage(file=RESET).subsample(1)
            self.up_img = PhotoImage(file=UP).subsample(3)
            self.down_img = PhotoImage(file=DOWN).subsample(3)
        
        elif isinstance(view, MultiChronoView):
            self.home_img = PhotoImage(file=HOME).subsample(2)
            self.run_img = PhotoImage(file=RUN).subsample(2)
            self.pause_img = PhotoImage(file=PAUSE).subsample(2)
            self.reset_img = PhotoImage(file=RESET).subsample(2)
        
        if isinstance(view, TimerView):
            self.home_img = PhotoImage(file=HOME).subsample(3)
            self.run_img = PhotoImage(file=RUN).subsample(3)
            self.pause_img = PhotoImage(file=PAUSE).subsample(3)
            self.reset_img = PhotoImage(file=RESET).subsample(3)
            self.up_img = PhotoImage(file=UP).subsample(7)
            self.down_img = PhotoImage(file=DOWN).subsample(7)
        
        if isinstance(view, ChronoView):
            self.home_img = PhotoImage(file=HOME).subsample(1)
            self.run_img = PhotoImage(file=RUN).subsample(1)
            self.pause_img = PhotoImage(file=PAUSE).subsample(1)
            self.reset_img = PhotoImage(file=RESET).subsample(1)


class SimultaneousChronoView(Frame):
    def __init__(self, controller, nb_chronos) -> None:
        """Creates the view of fiew chronos (2 -> 16), with 3 buttons (home/run/reset) and a label where time is
        displayed. Each chrono has an entry to set a name, and a pause button.
        The controller binds it to the same amount of models.

        Args:
            controller (SimultaneousChronoController): The controller of the view, in the controllers.py file
            nb_chronos (int): How many chronos you want (2 -> 16).
        """
        super().__init__()
        self.controller = controller
        self.asset_manager = AssetsManager(self)
        self.config(bg=BG_COLOR)
        if nb_chronos not in range(2, MAX_SIM_CHRONOS + 1):
            nb_chronos = 2
        self.nb_chronos = nb_chronos
        self.views = []

        self.grid(row=0, column=0)

        # 2 frames, one for the buttons, one for the chronos
        self.button_frm = Frame(
            self,
            bg=BG_COLOR,
        )
        self.button_frm.grid(row=0, column=0)

        self.chronos_frm = Frame(
            self,
            bg=BG_COLOR,
        )
        self.chronos_frm.grid(row=1, column=0)

        # Home button
        self.home_btn = Button(
            self.button_frm,
            bg=BG_COLOR,
            image=self.asset_manager.home_img,
            border=0,
            state=NORMAL,
            command=self.controller.destroy,
        )
        self.home_btn.grid(row=0, column=0, padx=BIG_PAD)

        # Run button
        self.run_btn = Button(
            self.button_frm,
            bg=BG_COLOR,
            image=self.asset_manager.run_img,
            border=0,
            state=NORMAL,
            command=self.controller.run_all,
        )
        self.run_btn.grid(row=0, column=1, padx=BIG_PAD)

        # Pause button
        self.pause_btn = Button(
            self.button_frm,
            bg=BG_COLOR,
            image=self.asset_manager.pause_img,
            border=0,
            state=DISABLED,
            command=self.controller.pause_all,
        )
        self.pause_btn.grid(row=0, column=2, padx=BIG_PAD)

        # Reset button
        self.reset_btn = Button(
            self.button_frm,
            bg=BG_COLOR,
            image=self.asset_manager.reset_img,
            border=0,
            command=self.controller.reset_all,
        )
        self.reset_btn.grid(row=0, column=3, padx=BIG_PAD)

        # Time Manager
        for i in range(self.nb_chronos):
            self.views.append(self._chrono_builder(i))

    def _chrono_builder(self, row) -> tuple:
        """Builds a chrono on a line, with an empty entry (allowing to attach the chrono to a person, for example), a
        button, and a label displaying the amount of time.
        The chrono is recorded in a list.

        Args:
            row (int): The line in which the chrono is built, corresponding to the chrono number.
        """
        # Variable to display
        display_var = StringVar(value="00:00.0")

        # Entry
        entry = Entry(
            self.chronos_frm,
            font=SMALL_FONT,
            width=12
        )
        entry.grid(row=row, column=0, padx=SMALL_PAD)

        # Run button
        run_btn = Button(
            self.chronos_frm,
            image=self.asset_manager.run_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.run_one(row),
        )
        run_btn.grid(row=row, column=1, padx=SMALL_PAD)

        # Pause button
        pause_btn = Button(
            self.chronos_frm,
            image=self.asset_manager.pause_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.pause_one(row),
            state=DISABLED,
        )
        pause_btn.grid(row=row, column=2, padx=SMALL_PAD)

        # Pause button
        stop_btn = Button(
            self.chronos_frm,
            image=self.asset_manager.reset_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.reset_one(row),
        )
        stop_btn.grid(row=row, column=3, padx=SMALL_PAD)

        # Display label
        display_lbl = Label(
            self.chronos_frm,
            font=BIG_FONT,
            bg=BG_COLOR,
            fg=TXT_COLOR,
        )
        display_lbl.grid(row=row, column=4, padx=SMALL_PAD)

        # Associates each chrono label with a StringVar variable
        display_lbl.config(textvariable=display_var)

        return display_var, display_lbl, entry, run_btn, pause_btn, stop_btn

    def update_display(self, chrono, value) -> None:
        """Displays the time value in the label of the chrono

        Args:
            chrono (int): The chrono to display.
            value (str): The time value to display.
        """
        self.views[chrono][0].set(value)

    def update_every_60ms(self) -> None:
        """Refreshes time display every 60 ms.
        """
        self.after(60, self.controller.update_every_60ms)

    def run_all(self) -> None:
        """Runs all chronos.
        """
        self.run_btn.config(state=DISABLED)
        self.pause_btn.config(state=NORMAL)
        for number in range(len(self.views)):
            self.run_one(number)

    def pause_all(self) -> None:
        """Pauses all chronos.
        """
        self.pause_btn.config(state=DISABLED)
        self.run_btn.config(state=NORMAL)
        for number in range(len(self.views)):
            self.pause_one(number)

    def reset_all(self) -> None:
        """Resets all chronos.
        """
        self.run_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
        for number in range(len(self.views)):
            self.reset_one(number)

    def run_one(self, value) -> None:
        """Enables all PAUSE buttons, disables the RUN button.

        value (int): the index of the chrono to run.
        """
        self.pause_btn.config(state=NORMAL)
        for index, chrono in enumerate(self.views):
            if index == value:
                chrono[3].config(state=DISABLED)
                chrono[4].config(state=NORMAL)
                chrono[5].config(state=NORMAL)

    def pause_one(self, value: int) -> None:
        """Disables the PAUSE button of the selected chrono.

        Args:
           value (int): the index of the chrono to pause.
        """
        self.run_btn.config(state=NORMAL)
        for index, chrono in enumerate(self.views):
            if index == value:
                chrono[3].config(state=NORMAL)
                chrono[4].config(state=DISABLED)
                chrono[5].config(state=NORMAL)

    def reset_one(self, value) -> None:
        """Enables all the buttons, and clears all the entries.

        Args:
           value (int): the index of the chrono to reset.
        """
        self.run_btn.config(state=NORMAL)
        for index, chrono in enumerate(self.views):
            if index == value:
                chrono[3].config(state=NORMAL)
                chrono[4].config(state=DISABLED)
                chrono[5].config(state=NORMAL)
                chrono[2].delete(0, END)

    def delete(self) -> None:
        """Deletes the instance.
        """
        self.destroy()


class MultiTimerView(Frame):
    def __init__(self, controller, number):
        """Creates the view of 2 timers, with 4 buttons (home/run/pause/reset). Each timer has a label displaying
        the amount of remaining time, and a circle representing the amount of remaining time.

        Args:
            controller (MultiTimerController): The controller of the view, in the controllers.py file.
        """
        super().__init__()
        self.controller = controller
        self.asset_manager = AssetsManager(self)
        self.config(bg=BG_COLOR)
        self.number = number
        self.font = BIG_FONT
        self.diameter = BIG_DIAMETER
        self.chrono_color = CHRONO_COLOR
        self.circle_color = TXT_COLOR
        self.views = []
        self.margin = MARGIN

        self.grid(row=0, column=0, columnspan=self.number)

        # Frames
        self.buttons_frm = Frame(self, bg=BG_COLOR)
        self.buttons_frm.grid(row=0, column=0)
        self.chronos_frm = Frame(self, bg=BG_COLOR)
        self.chronos_frm.grid(row=1, column=0)

        # Home button
        self.home = Button(
            self.buttons_frm,
            image=self.asset_manager.home_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.destroy,
        )
        self.home.grid(row=0, column=0, rowspan=2)

        # Add 10 min button
        self.add_10 = Button(
            self.buttons_frm,
            image=self.asset_manager.up_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.change_time(10),
        )
        self.add_10.grid(row=0, column=1)

        # Add 1 min button
        self.add_1 = Button(
            self.buttons_frm,
            image=self.asset_manager.up_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.change_time(1),
        )
        self.add_1.grid(row=0, column=2)

        # Substract 10 min button
        self.sub_10 = Button(
            self.buttons_frm,
            image=self.asset_manager.down_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.change_time(-10),
        )
        self.sub_10.grid(row=1, column=1)

        # Substract 1 min button
        self.sub_1 = Button(
            self.buttons_frm,
            image=self.asset_manager.down_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.change_time(-1),
        )
        self.sub_1.grid(row=1, column=2)

        # Run button
        self.run_btn = Button(
            self.buttons_frm,
            image=self.asset_manager.run_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.run,
        )
        self.run_btn.grid(row=0, column=3, rowspan=2)

        # Pause button
        self.pause_btn = Button(
            self.buttons_frm,
            image=self.asset_manager.pause_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.pause,
            state=DISABLED,
        )
        self.pause_btn.grid(row=0, column=4, rowspan=2)

        # Reset button
        self.reset_btn = Button(
            self.buttons_frm,
            image=self.asset_manager.reset_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.reset,
            state=DISABLED,
        )
        self.reset_btn.grid(row=0, column=5, rowspan=2)

        # Timers
        for i in range(self.number):
            self.views.append(TimerView(self, vertical=True, column=i, diameter=BIG_DIAMETER))
            self.views[i].run_btn.destroy()
            self.views[i].pause_btn.destroy()
            self.views[i].reset_btn.destroy()
            self.views[i].home.destroy()
            self.views[i].add_1.destroy()
            self.views[i].add_10.destroy()
            self.views[i].sub_1.destroy()
            self.views[i].sub_10.destroy()

    @property
    def interior_diameter(self) -> int:
        """Returns the value of the diameter of the internal circle.

        Returns:
            int: the value of the internal diameter.
        """
        return self.diameter - self.margin

    def update_every_60ms(self) -> None:
        """Refreshes time display every 60 ms.
        """
        self.after(60, self.controller.update_every_60ms)

        # The clock angles
        for timer in self.views:
            timer.clock.itemconfig(timer.arc, extent=timer.angle)
            timer.clock.update()

    def update_display(self, values_and_percents: list) -> None:
        """Displays the time value in the label and updates the arc angle.

        Args:
            values_and_percents (list): few tuples (str, float), one for each timer. The time value is the str,
            the percent is the float.
        """
        for index, value_and_percent in enumerate(values_and_percents):
            if value_and_percent[1] == 0 or values_and_percents[1] == 1:
                self.views[index].angle = 359.99
            else:
                self.views[index].angle = value_and_percent[1] * 360

            # The clock angles
            self.views[index].update_display(value_and_percent[0], value_and_percent[1])

    def run(self) -> None:
        """Disables all buttons except PAUSE and RESET buttons.
        """
        self.run_btn.config(state=DISABLED)
        self.pause_btn.config(state=NORMAL)
        self.reset_btn.config(state=NORMAL)
        self.add_1.config(state=DISABLED)
        self.add_10.config(state=DISABLED)
        self.sub_1.config(state=DISABLED)
        self.sub_10.config(state=DISABLED)

    def pause(self) -> None:
        """Enables RUN and RESET buttons, disables PAUSE button.
        """
        self.run_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
        self.reset_btn.config(state=NORMAL)

    def reset(self) -> None:
        """Enables every button except PAUSE and RESET buttons.
        """
        self.run_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
        self.reset_btn.config(state=DISABLED)
        self.add_1.config(state=NORMAL)
        self.add_10.config(state=NORMAL)
        self.sub_1.config(state=NORMAL)
        self.sub_10.config(state=NORMAL)

    def delete(self) -> None:
        """Deletes the instance.
        """
        for timer in self.views:
            timer.destroy()
        self.destroy()


class MultiChronoView(Frame):
    def __init__(self, controller, nb_chronos) -> None:
        """Creates the view of fiew chronos (2 -> 10), with 3 buttons (home/pause/reset) and a label where time is
        displayed. Each chrono has an entry to set a name, and a run button whiche pauses all the others.
        The controller binds it to the same amount of models.

        Args:
            controller (MultiChronoController): The controller of the view, in the controllers.py file.
            nb_chronos (int): How many chronos you want (2 -> 10).
        """
        super().__init__()
        self.controller = controller
        self.asset_manager = AssetsManager(self)
        if nb_chronos not in range(2, MAX_MLT_CHRONOS + 1):
            nb_chronos = 2
        self.nb_chronos = nb_chronos
        self.views = []

        self.config(bg=BG_COLOR)

        self.grid(row=0, column=0)

        # 2 frames, one for the buttons, one for the chronos
        self.button_frm = Frame(self, bg=BG_COLOR)
        self.button_frm.grid(row=0, column=0)

        self.chronos_frm = Frame(self, bg=BG_COLOR)
        self.chronos_frm.grid(row=1, column=0)

        # Home button
        self.home_btn = Button(
            self.button_frm,
            image=self.asset_manager.home_img,
            bg=BG_COLOR,
            border=0,
            state=NORMAL,
            command=self.controller.destroy,
        )
        self.home_btn.grid(row=0, column=0, padx=BIG_PAD)

        # Pause button
        self.pause_btn = Button(
            self.button_frm,
            image=self.asset_manager.pause_img,
            bg=BG_COLOR,
            border=0,
            state=DISABLED,
            command=self.controller.pause,
        )
        self.pause_btn.grid(row=0, column=1, padx=BIG_PAD)

        # Reset button
        self.reset_btn = Button(
            self.button_frm,
            image=self.asset_manager.reset_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.reset,
        )
        self.reset_btn.grid(row=0, column=2, padx=BIG_PAD)

        # Time Manager
        for i in range(self.nb_chronos):
            self.views.append(self._chrono_builder(i))

    def _chrono_builder(self, row):
        """Builds a chrono on a line, with an empty entry (allowing to attach the chrono to a person, for example), a
        button, and a label displaying the amount of time.
        The chrono is recorded in a list.

        Args:
            row (int): The line in which the chrono is built, corresponding to the chrono number.
        """
        # Variable to display
        display_var = StringVar(value="00:00.0")

        # Entry
        entry = Entry(self.chronos_frm, font=SMALL_FONT, width=12)
        entry.grid(row=row, column=0, padx=SMALL_PAD)

        # Run button
        run_btn = Button(
            self.chronos_frm,
            image=self.asset_manager.run_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.run(row),
        )
        run_btn.grid(row=row, column=1, padx=SMALL_PAD)

        # Display label
        display_lbl = Label(self.chronos_frm, font=BIG_FONT, bg=BG_COLOR, fg=TXT_COLOR)
        display_lbl.grid(row=row, column=2, padx=SMALL_PAD)

        # Associates each chrono label with a StringVar variable
        display_lbl.config(textvariable=display_var)

        return display_var, display_lbl, entry, run_btn

    def update_display(self, chrono: int, value: str) -> None:
        """Displays the time value in the label of the chrono

        Args:
            chrono (int): The index of the chrono to display
            value (str): The time value to display.
        """
        self.views[chrono][0].set(value)

    def update_every_60ms(self) -> None:
        """Refreshes time display every 60 ms.
        """
        self.after(60, self.controller.update_every_60ms)

    def run(self, value: int) -> None:
        """Enables all buttons except the RUN button of the chrono at the index in the self.views list

        Args:
            value (int): The index of the chrono to run.
        """
        self.pause_btn.config(state=NORMAL)
        for index, chrono in enumerate(self.views):
            if index == value:
                chrono[3].config(state=DISABLED)
            else:
                chrono[3].config(state=NORMAL)

    def pause(self) -> None:
        """Enables all RUN buttons, and disables the PAUSE button.
        """
        self.pause_btn.config(state=DISABLED)
        self.reset_btn.config(state=NORMAL)
        for chrono in self.views:
            chrono[3].config(state=NORMAL)

    def reset(self) -> None:
        """Enables all the buttons, and clears all the entries.
        """
        self.pause_btn.config(state=NORMAL)
        for chrono in self.views:
            chrono[3].config(state=NORMAL)
            chrono[2].delete(0, END)

    def delete(self) -> None:
        """Deletes the instance.
        """
        self.destroy()


class TimerView(Frame):
    def __init__(self, controller, vertical: bool = False, column: int = 0, diameter: int = SMALL_DIAMETER) -> None:
        """Creates the view of a timer, with 3 buttons (home/run/pause/reset), a label where time is displayed, and
        a circle representing the amount of remaining time.
        The controller binds it to a model.

        Args:
            controller (TimerController): the controller of the view, in the controllers.py file.
            vertical (bool): the disposition of the clock and the label.
            column (int): the index of the column to display the view.
        """
        super().__init__()
        self.controller = controller
        self.asset_manager = AssetsManager(self)

        # Dimensions, disposition, colors, font
        if vertical:
            clock_coords = (2, 0, 1)
        else:
            clock_coords = (0, 2, 2)
        self.font = BIG_FONT
        self.diameter = diameter
        self.margin = MARGIN
        self.chrono_color = CHRONO_COLOR
        self.circle_color = TXT_COLOR
        self.column = column
        self.config(bg=BG_COLOR)

        # Variable displayed in the label and arc's angle
        self.display_var = StringVar(value="00:00.0")
        self.angle = 359.99

        self.grid(row=1, column=self.column)

        # Frames
        self.buttons_frm = Frame(self, bg=BG_COLOR)
        self.buttons_frm.grid(row=0, column=0)

        # Home button
        self.home = Button(
            self.buttons_frm,
            image=self.asset_manager.home_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.destroy,
        )
        self.home.grid(row=0, column=0, rowspan=2)

        # Add 10 min button
        self.add_10 = Button(
            self.buttons_frm,
            image=self.asset_manager.up_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.change_time(10),
        )
        self.add_10.grid(row=0, column=1)

        # Add 1 min button
        self.add_1 = Button(
            self.buttons_frm,
            image=self.asset_manager.up_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.change_time(1),
        )
        self.add_1.grid(row=0, column=2)

        # Substract 10 min button
        self.sub_10 = Button(
            self.buttons_frm,
            bg=BG_COLOR,
            border=0,
            image=self.asset_manager.down_img,
            command=lambda: self.controller.change_time(-10),
        )
        self.sub_10.grid(row=1, column=1)

        # Substract 1 min button
        self.sub_1 = Button(
            self.buttons_frm,
            image=self.asset_manager.down_img,
            bg=BG_COLOR,
            border=0,
            command=lambda: self.controller.change_time(-1),
        )
        self.sub_1.grid(row=1, column=2)

        # Run button
        self.run_btn = Button(
            self.buttons_frm,
            image=self.asset_manager.run_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.run,
        )
        self.run_btn.grid(row=0, column=3, rowspan=2)

        # Pause button
        self.pause_btn = Button(
            self.buttons_frm,
            image=self.asset_manager.pause_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.pause,
            state=DISABLED,
        )
        self.pause_btn.grid(row=0, column=4, rowspan=2)

        # Reset button
        self.reset_btn = Button(
            self.buttons_frm,
            image=self.asset_manager.reset_img,
            bg=BG_COLOR,
            border=0,
            command=self.controller.reset,
            state=DISABLED,
        )
        self.reset_btn.grid(row=0, column=5, rowspan=2)

        # Label
        self.display_lbl = Label(self, font=self.font, fg=TXT_COLOR, bg=BG_COLOR, textvariable=self.display_var)
        self.display_lbl.grid(row=1, column=0)

        # Clock
        self.clock = Canvas(self, height=self.diameter, width=self.diameter, bg=BG_COLOR)
        self.clock.grid(row=clock_coords[0], column=clock_coords[1], rowspan=clock_coords[2])
        self.clock.create_oval(self.margin, self.margin, self.diameter, self.diameter,
                               fill=self.circle_color, outline=self.circle_color)
        self.arc = self.clock.create_arc(2 * self.margin, 2 * self.margin,
                                         self.interior_diameter, self.interior_diameter,
                                         start=90, extent=self.angle, outline=self.chrono_color,
                                         fill=self.chrono_color)

    @property
    def interior_diameter(self) -> int:
        """Returns the value of the diameter of the internal circle.

        Returns:
            int: the internal diameter of the chrono.
        """
        return self.diameter - self.margin

    def update_every_60ms(self) -> None:
        """Refreshes time display every 60 ms.
        """
        self.after(60, self.controller.update_every_60ms)

        # The clock angle
        self.clock.itemconfig(self.arc, extent=self.angle)
        self.clock.update()

    def update_display(self, value: str, percent: float) -> None:
        """Displays the time value in the label and updates the arc angle

        Args:
            value (str): the time value to display.
            percent (float): the percent of this time value.
        """
        if percent == 0 or percent == 1:
            self.angle = 359.99
        else:
            self.angle = percent * 360

        # The clock angle
        self.clock.itemconfig(self.arc, extent=self.angle)
        self.clock.update()

        #  The label
        self.display_var.set(value)

    def run(self):
        """Disables all buttons except PAUSE and RESET.
        """
        self.run_btn.config(state=DISABLED)
        self.pause_btn.config(state=NORMAL)
        self.reset_btn.config(state=NORMAL)
        self.add_1.config(state=DISABLED)
        self.add_10.config(state=DISABLED)
        self.sub_1.config(state=DISABLED)
        self.sub_10.config(state=DISABLED)

    def pause(self) -> None:
        """Enables the RUN and RESET buttons and disables the PAUSE button.
        """
        self.run_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
        self.reset_btn.config(state=NORMAL)

    def reset(self) -> None:
        """Enables all buttons except RESET button.
        """
        self.pause_btn.config(state=DISABLED)
        self.run_btn.config(state=NORMAL)
        self.reset_btn.config(state=DISABLED)
        self.add_1.config(state=NORMAL)
        self.add_10.config(state=NORMAL)
        self.sub_1.config(state=NORMAL)
        self.sub_10.config(state=NORMAL)

    def delete(self) -> None:
        """Deletes the instance.
        """
        self.destroy()


class ChronoView(Frame):
    def __init__(self, controller) -> None:
        """Creates the view of a chrono, with 4 buttons (home/run/pause/reset) and a label where time is displayed.
        The controller binds it to a model.

        Args:
            controller (ChronoController): the controller of the view, in the controllers.py file.
        """
        super().__init__()
        self.config(bg=BG_COLOR)
        self.controller = controller
        self.asset_manager = AssetsManager(self)
        self.font = SMALL_FONT

        # Variable displayed in the label
        self.display_var = StringVar(value="00:00.0")


        self.grid(row=0, column=0)

        # Display label
        self.display_lbl = Label(self, bg=BG_COLOR, textvariable=self.display_var, font=VERY_BIG_FONT)
        self.display_lbl.grid(row=0, column=0, columnspan=4, padx=MARGIN)

        # Home button
        self.home_btn = Button(
            self,
            bg=BG_COLOR,
            image=self.asset_manager.home_img,
            border=0,
            command=self.controller.destroy,
        )
        self.home_btn.grid(row=1, column=0, padx=MARGIN)

        # Run button
        self.run_btn = Button(
            self,
            bg=BG_COLOR,
            image=self.asset_manager.run_img,
            border=0,
            command=self.controller.run,
        )
        self.run_btn.grid(row=1, column=1, padx=MARGIN)

        # Pause button
        self.pause_btn = Button(
            self,
            bg=BG_COLOR,
            image=self.asset_manager.pause_img,
            border=0,
            state=DISABLED,
            command=self.controller.pause,
        )
        self.pause_btn.grid(row=1, column=2, padx=MARGIN)

        # Reset button
        self.reset_btn = Button(
            self,
            bg=BG_COLOR,
            state=DISABLED,
            image=self.asset_manager.reset_img,
            border=0,
            command=self.controller.reset,
        )
        self.reset_btn.grid(row=1, column=3, padx=MARGIN)

    def update_display(self, value: str) -> None:
        """Displays the time value in the label

        Args:
            value (str): The time value to display.
        """
        self.display_var.set(value)

    def update_every_60ms(self) -> None:
        """Refreshes time display every 60 ms.
        """
        self.after(60, self.controller.update_every_60ms)

    def run(self) -> None:
        """Enables PAUSE and RESET buttons, and disables RUN button.
        """
        self.run_btn.config(state=DISABLED)
        self.pause_btn.config(state=NORMAL)
        self.reset_btn.config(state=NORMAL)

    def pause(self) -> None:
        """Enables RUN and RESET buttons, and disables PAUSE button.
        """
        self.run_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
        self.reset_btn.config(state=NORMAL)

    def reset(self) -> None:
        """Enables RUN buttons, and disables PAUSE and RESET button.
        """
        self.run_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
        self.reset_btn.config(state=DISABLED)

    def delete(self) -> None:
        """Deletes the instance.
        """
        self.destroy()


class ApplicationView(Tk):
    def __init__(self, controller):
        """Creates the view of the app menu, allowing user to select an option.
        The controller binds it to a model.

        Args:
            controller (ApplicationController): the controller of the view, in the controllers.py file.
        """
        super().__init__()
        self.controller = controller
        self.config(bg=BG_COLOR)
        self.iconbitmap(ICONE)

        self.menu_frm = Frame(self, bg=BG_COLOR)
        self.menu_frm.grid(row=0, column=0)
        self.show_menu()

        self.one_chrono_btn = Button(
            self.menu_frm,
            fg=TXT_COLOR,
            width=BUTTON_WIDTH,
            text=CHRONO,
            font=SMALL_FONT,
            command=lambda: self.build_app(1),
        )
        self.one_chrono_btn.grid(row=0, column=0, columnspan=2, padx=SMALL_PAD, pady=SMALL_PAD)

        self.spinbox_mlt = Spinbox(
            self.menu_frm,
            fg=TXT_COLOR,
            width=SPINBOX_WIDTH,
            from_=2,
            to=MAX_MLT_CHRONOS,
            wrap=True,
            justify="right",
            font=SMALL_FONT,

        )
        self.spinbox_mlt.grid(row=1, column=0, padx=SMALL_PAD, pady=SMALL_PAD)

        self.mlt_chrono_btn = Button(
            self.menu_frm,
            fg=TXT_COLOR,
            width=BUTTON_WIDTH - SPINBOX_WIDTH - 3,
            text=MULTICHRONO,
            font=SMALL_FONT,
            command=lambda: self.build_app(2),
        )
        self.mlt_chrono_btn.grid(row=1, column=1, padx=SMALL_PAD, pady=SMALL_PAD)

        self.spinbox_sim = Spinbox(
            self.menu_frm,
            fg=TXT_COLOR,
            width=SPINBOX_WIDTH,
            from_=2,
            to=MAX_SIM_CHRONOS,
            wrap=True,
            justify="right",
            font=SMALL_FONT,
        )
        self.spinbox_sim.grid(row=2, column=0, padx=SMALL_PAD, pady=SMALL_PAD)

        self.mlt_chrono_btn = Button(
            self.menu_frm,
            text=SIMCHRONOS,
            fg=TXT_COLOR,
            width=BUTTON_WIDTH - SPINBOX_WIDTH - 3,
            font=SMALL_FONT,
            command=lambda: self.build_app(3),
        )
        self.mlt_chrono_btn.grid(row=2, column=1, padx=SMALL_PAD, pady=SMALL_PAD)

        self.one_timer_btn = Button(
            self.menu_frm,
            text=TIMER,
            fg=TXT_COLOR,
            width=BUTTON_WIDTH,
            font=SMALL_FONT,
            command=lambda: self.build_app(4),
        )
        self.one_timer_btn.grid(row=3, column=0, columnspan=2, padx=SMALL_PAD, pady=SMALL_PAD)

        self.mlt_timer_btn = Button(
            self.menu_frm,
            text=MULTITIMER,
            fg=TXT_COLOR,
            width=BUTTON_WIDTH,
            font=SMALL_FONT,
            command=lambda: self.build_app(5),
        )
        self.mlt_timer_btn.grid(row=4, column=0, columnspan=2, padx=SMALL_PAD, pady=SMALL_PAD)

    @property
    def nb_mlt_chronos(self):
        try:
            a = int(self.spinbox_mlt.get())
            return a
        except ValueError:
            return 1

    @property
    def nb_sim_chronos(self):
        try:
            a = int(self.spinbox_sim.get())
            return a
        except ValueError:
            return 1

    def hide_menu(self) -> None:
        """When user selects an option, hides the main menu.
        """
        self.menu_frm.grid_forget()

    def show_menu(self) -> None:
        """When user gets back to main menu, displays main menu and deletes the name of the app.
        """
        self.title(MAIN_TITLE)
        self.menu_frm.grid(row=1, column=0)

    def build_app(self, index: int) -> None:
        """Builds the selected app : Chrono, Multichrono, Timer, Multitimer.

        Args:
            index (int): the index of the selected app.
        """
        match index:
            case 1:
                self.title(CHRONO)
                self.controller.build_one_chrono()
            case 2:
                self.title(MULTICHRONO)
                self.controller.build_mlt_chrono()
            case 3:
                self.title(SIMCHRONOS)
                self.controller.build_sim_chronos()
            case 4:
                self.title(TIMER)
                self.controller.build_one_timer()
            case 5:
                self.title(MULTITIMER)
                self.controller.build_mlt_timer()

    def launch_app(self) -> None:
        """Runs the GUI.
        """
        self.mainloop()
