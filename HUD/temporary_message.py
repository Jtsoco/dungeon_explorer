class TemporaryMessage:
    def __init__(self, message: str, frames_duration: int):

        # the command version of duration has a float, but it's int here, because the hud manager should convert duration to update cycles, whereas the command just passes the seconds desired
        self.message = message
        self.frames_duration = frames_duration  # frames_duration in update cycles
        self.elapsed = 0

    def update(self):
        self.elapsed += 1
        if self.elapsed >= self.frames_duration:
            return True  # indicates the message duration is over
        return False
