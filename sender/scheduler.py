# scheduler.py
#
# Dazzling2-mini_2
# Sender Scheduler
#
# This module does NOT:
# - connect to Wi-Fi
# - get NTP time
# - call APIs
# - send UART
#
# It only determines which scheduled events are due
# based on a time value supplied to it.
#
# Events that become due between scheduler checks
# are returned in chronological order.


import time


class Scheduler:

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self):

        self.weekly_schedule = {
            self.MONDAY: [],
            self.TUESDAY: [],
            self.WEDNESDAY: [],
            self.THURSDAY: [],
            self.FRIDAY: [],
            self.SATURDAY: [],
            self.SUNDAY: []
        }

        self.special_dates = {}

        self.executed_events = set()

        # Time of the previous scheduler check.
        self.last_checked_time = None

    def add_weekly_event(
        self,
        weekday,
        hour,
        minute,
        event,
        profile=None
    ):

        self.weekly_schedule[weekday].append(
            (
                hour,
                minute,
                event,
                profile
            )
        )

    def add_special_date_event(
        self,
        date_string,
        hour,
        minute,
        event,
        profile=None
    ):

        if date_string not in self.special_dates:

            self.special_dates[date_string] = []

        self.special_dates[date_string].append(
            (
                hour,
                minute,
                event,
                profile
            )
        )

    def _get_date_string(self, current_time):

        year = current_time[0]
        month = current_time[1]
        day = current_time[2]

        return "{:04d}-{:02d}-{:02d}".format(
            year,
            month,
            day
        )

    def _get_event_key(
        self,
        current_time,
        hour,
        minute,
        event,
        profile
    ):

        date_string = self._get_date_string(
            current_time
        )

        return (
            date_string,
            hour,
            minute,
            event,
            profile
        )

    def _get_today_schedule(self, current_time):

        date_string = self._get_date_string(
            current_time
        )

        if date_string in self.special_dates:

            return self.special_dates[date_string]

        weekday = current_time[6]

        return self.weekly_schedule[weekday]

    def _time_to_minutes(self, current_time):

        return int(
            time.mktime(
                (
                    current_time[0],
                    current_time[1],
                    current_time[2],
                    current_time[3],
                    current_time[4],
                    0,
                    current_time[6],
                    0
                )
            ) // 60
        )

    def _get_time_tuple(self, total_minutes):

        timestamp = total_minutes * 60

        return time.localtime(timestamp)

    def _get_events_for_minute(self, current_time):

        current_hour = current_time[3]
        current_minute = current_time[4]

        schedule = self._get_today_schedule(
            current_time
        )

        due_events = []

        for scheduled_event in schedule:

            hour = scheduled_event[0]
            minute = scheduled_event[1]
            event = scheduled_event[2]
            profile = scheduled_event[3]

            if current_hour != hour:
                continue

            if current_minute != minute:
                continue

            event_key = self._get_event_key(
                current_time,
                hour,
                minute,
                event,
                profile
            )

            if event_key in self.executed_events:
                continue

            self.executed_events.add(
                event_key
            )

            due_events.append(
                {
                    "event": event,
                    "profile": profile
                }
            )

        return due_events

    def check(self, current_time):

        current_minutes = self._time_to_minutes(
            current_time
        )

        due_events = []

        # First check after startup:
        # only check the current minute.
        if self.last_checked_time is None:

            due_events.extend(
                self._get_events_for_minute(
                    current_time
                )
            )

            self.last_checked_time = current_minutes

            return due_events

        last_minutes = self.last_checked_time

        # Nothing new to check.
        if current_minutes <= last_minutes:

            return due_events

        # Check every minute since the previous check.
        #
        # This allows the scheduler to catch events that
        # occurred while main.py was busy with another task.
        for minute_value in range(
            last_minutes + 1,
            current_minutes + 1
        ):

            check_time = self._get_time_tuple(
                minute_value
            )

            minute_events = self._get_events_for_minute(
                check_time
            )

            due_events.extend(
                minute_events
            )

        self.last_checked_time = current_minutes

        return due_events
