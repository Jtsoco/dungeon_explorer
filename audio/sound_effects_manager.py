import pyxel

class SoundEffectsManager:
    def __init__(self, context= None):
        self.context = context
        self.sounds_to_play = set()
        # a set, because why play the same sound more than once in a frame?

    # this uses pyxel sounds, so already has access to audio files loaded in pyxel


    def update(self):
        # play any queued sounds
        pass

    def handle_event(self, event):
        # determines what sound to qeue
        pass
