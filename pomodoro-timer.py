#!/usr/bin/python2.7

import rumps
import time
import threading
import datetime


class AwesomeStatusBarApp(rumps.App):

    def __init__(self):
        icon_path = "images/icon.png"
        super(AwesomeStatusBarApp, self).__init__("Pomodoro")
        self.menu_items = ["Start", "Reset Timer", "Reset Pomodoro"]
        self.menu = self.menu_items

        self.break_message = "Time for a break"
        self.return_message = "Time to get back to work"
        self.message = ""

        self.pomodoro_count = 0
        self.work = 25
        self.short_break = 3
        self.long_break = 15

        self.break_time = False
        self.show_alert = False
        self.icon = icon_path
        self.timer_item = None
        self.end_time = None

        self.count_down_timer = None
        self.label_updater = None

    @rumps.clicked("Reset Timer")
    def restart_current(self, _):
        self.count_down_timer.stop()
        self.remove_time_remaining()

        self.break_time = not self.break_time

        if (not self.break_time):
            self.pomodoro_count -= 1

    @rumps.clicked("Reset Pomodoro")
    def reset_pomodoro(self, _):
        self.count_down_timer.stop()
        self.remove_time_remaining()
        self.pomodoro_count = 0
        self.break_time = False

    @rumps.clicked("Start")
    def pomodoro(self, _):

        self.pomodoro_count = 0 if self.pomodoro_count > 4 else self.pomodoro_count

        timer_mins = self.work
        alert_message = ""

        if(self.break_time == True):
            timer_mins = self.short_break
            if(self.pomodoro_count == 4):
                timer_mins = self.long_break

            alert_message = self.return_message

        else:
            self.pomodoro_count += 1
            break_length = "long" if self.pomodoro_count == 4 else "short"
            alert_message = "Time for a %s break" % break_length

        self.message = alert_message
        self.break_time = not self.break_time
        self.countdown(timer_mins)

    def time_remaining_updater(self, sender):
        remaining_time = self.end_time - datetime.datetime.now()

        remaining_minutes = (remaining_time.seconds % 3600) // 60
        remaining_seconds = remaining_time.seconds % 60

        time_remaining = unicode("Time remaining: %s:%s" % (
                                 remaining_minutes, remaining_seconds))

        self.remove_timer_menu()

        self.timer_item = time_remaining
        self.menu.insert_after("Start", time_remaining)

    def remove_timer_menu(self):
        if (self.timer_item is not None):
            self.menu.__delitem__(self.timer_item)

    def countdown(self, mins):
        secs = mins * 60
        self.end_time = datetime.datetime.now() + datetime.timedelta(seconds=secs)
        self.show_alert = False
        self.count_down_timer = rumps.Timer(self.alert, secs)
        self.count_down_timer.start()
        self.label_updater = rumps.Timer(self.time_remaining_updater, 1)
        self.label_updater.start()

    def alert(self, timer):

        if(self.show_alert == True):
            rumps.notification("Pomdoro", self.message, "", icon=self.icon)
            timer.stop()
            self.remove_time_remaining()
        self.show_alert = not self.show_alert

    def remove_time_remaining(self):
        self.label_updater.stop()
        self.remove_timer_menu()
        self.timer_item = None


if __name__ == "__main__":
    AwesomeStatusBarApp().run()
