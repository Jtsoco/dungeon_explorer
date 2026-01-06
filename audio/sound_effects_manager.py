import pyxel
from events_commands.commands import SoundCommand
from audio.sound_enums import SoundEnum
class SoundEffectsManager:
    def __init__(self, context= None):
        self.context = context
        self.sounds_to_play = set()
        # a set, because why play the same sound more than once in a frame?

    # this uses pyxel sounds, so already has access to audio files loaded in pyxel


    def update(self):
        # play any queued sounds
        for sound_enum in self.sounds_to_play:
            pyxel.play(0, sound_enum[0], loop=sound_enum[1])
        self.sounds_to_play.clear()

    def handle_event(self, event):
        # determines what sound to qeue
        pass

    def handle_command(self, command):
        match command:
            case SoundCommand():
                self.queue_sound(command.sound_enum, command.loop)
        return []  # No new events

    def queue_sound(self, sound_enum, loop=False):
        self.sounds_to_play.add((sound_enum, loop))


# possibly use context of player location to edit volume based on distance later
