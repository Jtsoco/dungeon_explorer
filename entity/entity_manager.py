from animations.animation_manager import AnimationManager
class EntityManager():
    def __init__(self, animation_manager=AnimationManager()):
        self.controllers = {}
        # controllers are loaded depending on entity type, done when loading a level
        self.physics = {}
        # depends on entity type, what physics to apply. floating skulls don't fall...
        self.animation_manager = animation_manager
