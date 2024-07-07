import matplotlib.pyplot as plt
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from relapse_db import RelapseDB
import numpy as np
import time


class StatsScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.orientation = "vertical"

        # Time period selector
        self.period_spinner = Spinner(
            text="Last 1 hour",
            values=(
                "Last 1 hour",
                "Last 8 hours",
                "Last day",
                "Last week",
                "Last 30 days",
                "Last 180 days",
                "Last year",
                "All",
            ),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.period_spinner.bind(text=self.update_stats)
        self.add_widget(self.period_spinner)

        # Plot area
        self.plot_area = BoxLayout(size_hint=(1, 0.6))
        self.add_widget(self.plot_area)

        # Statistical labels
        self.stats_label = Label(text="Stats: Calculating...")
        self.add_widget(self.stats_label)

        self.db = RelapseDB()
        self.update_stats(self.period_spinner, self.period_spinner.text)

    def update_stats(self, spinner, text):
        period_map = {
            "Last 1 hour": 3600,
            "Last 8 hours": 3600 * 8,
            "Last day": 3600 * 24,
            "Last week": 3600 * 24 * 7,
            "Last 30 days": 3600 * 24 * 30,
            "Last 180 days": 3600 * 24 * 180,
            "Last year": 3600 * 24 * 365,
            "All": None,
        }

        period = period_map[text]
        current_time = time.time()
        start_time = current_time - period if period else 0
        relapses = (
            self.db.get_relapses_in_period(start_time, current_time)
            if period
            else self.db.get_all_relapses()
        )

        times = [relapse[0] for relapse in relapses]

        if len(times) > 1:
            intervals = np.diff(times)
            mean_interval = np.mean(intervals)
            stddev_interval = np.std(intervals)
        else:
            mean_interval = stddev_interval = 0

        total_relapses = len(times)
        self.stats_label.text = f"Total relapses: {total_relapses}\nMean interval: {mean_interval:.2f} seconds\nStddev interval: {stddev_interval:.2f} seconds"

        self.plot_relapses(times, period)

    def plot_relapses(self, times, period):
        self.plot_area.clear_widgets()
        if not times:
            return

        times = np.array(times)
        bins = np.arange(times.min(), times.max(), period // 24) if period else 24

        fig, ax = plt.subplots()
        ax.hist(times, bins=bins, edgecolor="black")
        ax.set_title("Relapses over time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Number of relapses")

        self.plot_area.add_widget(FigureCanvasKivyAgg(fig))
