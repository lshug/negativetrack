from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from relapse_db import RelapseDB
from stat_screen import StatsScreen
import time
import datetime


class MainScreen(BoxLayout):
    def __init__(self, manager, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.manager = manager
        self.orientation = "vertical"
        self.db = RelapseDB()

        self.last_relapse_label = Label(text="Last relapse: calculating...")
        self.add_widget(self.last_relapse_label)

        self.relapse_button = Button(text="Relapse", on_press=self.record_relapse)
        self.add_widget(self.relapse_button)

        self.stats_button = Button(text="Stats", on_press=self.show_stats)
        self.add_widget(self.stats_button)

        Clock.schedule_interval(self.update_time_since_last_relapse, 1)

    def record_relapse(self, instance):
        self.db.add_relapse()
        self.update_time_since_last_relapse()

    def update_time_since_last_relapse(self, *args):
        last_relapse = self.db.get_last_relapse()
        if last_relapse:
            last_timestamp = last_relapse[0]
            elapsed = time.time() - last_timestamp
            elapsed_time = str(datetime.timedelta(seconds=int(elapsed)))
            self.last_relapse_label.text = f"Time since last relapse: {elapsed_time}"
        else:
            self.last_relapse_label.text = "No relapses recorded yet."

    def show_stats(self, instance):
        self.manager.current = "stats"


class RelapseApp(App):
    def build(self):
        sm = ScreenManager()
        main_screen = Screen(name="main")
        main_screen.add_widget(MainScreen(sm))
        sm.add_widget(main_screen)
        stats_screen = Screen(name="stats")
        stats_screen.add_widget(StatsScreen())
        sm.add_widget(stats_screen)
        return sm


if __name__ == "__main__":
    RelapseApp().run()
