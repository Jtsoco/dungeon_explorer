# this class manages effects/visuals not tied to an entity, but that exist in the world without a solid interactable entity
# the goals are to manage effects like particles, death smoke animations, etc
# it gets events, creates effects based on them, updates them, removes them when finished, and returns current effects to draw when requested
# it can also send out events tied to the effects if needed later
# these effects should be temporary in nature, and not persistent world objects.
# if a visual effect must be permanent, it should be tied to the cell or entity system instead

from animations.death_registry import GENERIC_DEATH_ANIMATION
from animations.effects_registry import EFFECTS_REGISTRY

from enums.effects_enums import EffectType, ParticleEffectType

from events_commands.events import DeathEvent as Death
from events_commands.commands import EffectCommand
from effects.effects import Effect

class EffectsManager():
    def __init__(self, context=None):
        self.context = context
        self.active_effects = []

    def update(self):
        to_remove = []
        for effect in self.active_effects:
            self.update_effect(effect)
            if effect.finished:
                to_remove.append(effect)
        for effect in to_remove:
            self.active_effects.remove(effect)
        # remove finished effects

        # eventually may have events to return based on effects finishing, for now just keep it simple
        return []

    def update_effect(self, effect):
        # effects store data, they don't have the logic in them for updates, that's the managers job
        current_frame = effect.get_current_animation_frame()
        # if moved to the next frame, update frame index. if 0 again, animation is done, mark finished
        effect.frame_timer += 1
        if self.next_frame(current_frame.duration, effect):
            if effect.current_frame == 0:
                effect.finished = True

    def next_frame(self, frame_duration, data):
        if data.frame_timer >= frame_duration:
            data.current_frame += 1
            data.frame_timer = 0
            self.set_current_frame_index(data)
            return True
        return False

    def set_current_frame_index(self, data):
        data.current_frame %= len(data.animation_frames)

    def get_effects(self):
        return self.active_effects

    def handle_event(self, event):
        # based on event type, create new effects
        match event:
            case Death():
                self.create_death_effect(event)

    def create_death_effect(self, event):
        # for now just a simple placeholder effect, but will differ based on entity type later
        entity = event.entity
        effect_position = entity.position
        effect_type = EffectType.DEATH_ANIMATION
        animation = GENERIC_DEATH_ANIMATION
        new_effect = Effect(effect_type, effect_position, animation)
        self.active_effects.append(new_effect)
        print(f"Created death effect at {effect_position}")

    def handle_command(self, command):
        match command:
            case EffectCommand():
                self.create_effect(command)
        return [], []  # No new events or commands

    def create_effect(self, command):
        effect_position = command.position
        sub_type = command.sub_type
        main_type = command.effect_type
        animation = self.get_animation(main_type, sub_type)
        # it should all be there, but for now to prevent nonexistent key errors, check
        if animation:
            new_effect = Effect(main_type, effect_position, animation)
            self.active_effects.append(new_effect)
            print(f"Created partical effect of type {sub_type} at {effect_position}")

    def get_animation(self, effect_type, sub_type):
        main = EFFECTS_REGISTRY.get(effect_type, None)
        if main:
            animation = main.get(sub_type, None)
            return animation
        return None
