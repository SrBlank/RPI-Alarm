import ffmpeg


class Alarm(object):
    def __init__(
        self, time, playtime=0, alarm_sound="generic_alarm.mp3", input="Button"
    ):
        self.time = time
        self.time_diff = None
        self.alarm_sound = "./alarm_sounds/" + alarm_sound

        if playtime == "":
            playtime = int(float(ffmpeg.probe(self.alarm_sound)["format"]["duration"]))
        self.playtime = playtime

        self.input = input

    def __repr__(self):
        return (
            self.time
            + " "
            + str(self.playtime)
            + " "
            + str(self.alarm_sound)
            + " "
            + str(self.input)
        )

    def __contains__(self, time):
        return time in self.time
