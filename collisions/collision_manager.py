
class CollisionManager():
    def __init__(self):
        self.recent_collisions = {}
        # could do attacker, target, weapon type of collision tracking with a timestamp/frame count for the value
        self.event_queue = []

    # purpose of this class is to receive possible collision events, then  determine if anything needs to be done about them

    def handle_events(self, events):
        # will receive a list of possible collision events
        pass

    def handle_event(self, event):
        pass

    # event for PossibleAttackCollision will have attacker, weapon, included. weapon includes hitbox and damage info
    # event for PossibleEntityCollision
    def register_collision(self, possible_collision_event):
        self.collision_queue.append(possible_collision_event)

    def update(self, player, entities):
        for event in self.event_queue:
            match event:
                case PossibleAttackCollisionEvent():
                    self.handle_attack_collision(event, player, entities)
                case PossibleEntityCollisionEvent():
                    self.handle_entity_collision(event, player, entities)
