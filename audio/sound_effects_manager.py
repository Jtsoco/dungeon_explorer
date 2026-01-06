import pyxel
from events_commands.commands import SoundCommand, MusicCommand
from audio.sound_enums import SoundEnum
class SoundEffectsManager:
    def __init__(self, context= None):
        self.context = context
        self.sounds_to_play = set()
        # a set, because why play the same sound more than once in a frame?
        self.music_to_play = set()

    # this uses pyxel sounds, so already has access to audio files loaded in pyxel
        self.channels = [0, 1, 2, 3]  # pyxel has 4 sound channels 0-3

        self.effects_channels = (1, 2, 3)
        self.currently_used_channels = []

    def update(self):
        # play any queued sounds
        for sound_enum in self.sounds_to_play:
            self.play_sound(sound_enum[0], sound_enum[1])

        if self.music_to_play:
            music = self.get_max_priority_music(self.music_to_play)
            pyxel.playm(music[0], loop=music[1])

        self.sounds_to_play.clear()
        self.music_to_play.clear()
        self.currently_used_channels.clear()

    def play_sound(self, sound_enum, loop=False):
        for channel in self.effects_channels:
            if channel not in self.currently_used_channels:
                self.currently_used_channels.append(channel)
                pyxel.play(channel, sound_enum.value, loop=loop)
                return
        # if all channels are used, just play on channel 1, will cut off whatever
        pyxel.play(1, sound_enum.value, loop=loop)

    def get_max_priority_music(self, music_set):
        music = max(music_set, key=lambda song: song[2])
        return music

    def handle_event(self, event):
        # determines what sound to qeue
        pass

    def handle_command(self, command):
        match command:
            case SoundCommand():
                self.queue_sound(command.sound_enum, command.loop)
            case MusicCommand():
                self.queue_music(command.music_enum, command.loop, command.priority)

        return []  # No new events

    def queue_sound(self, sound_enum, loop=False):
        self.sounds_to_play.add((sound_enum, loop))


# possibly use context of player location to edit volume based on distance later
    def queue_music(self, music_enum, loop=True, priority=0):
        self.music_to_play.add((music_enum, loop, priority))
