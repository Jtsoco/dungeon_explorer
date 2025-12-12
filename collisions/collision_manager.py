from events_commands.events import PossibleAttackCollisionEvent as PACE, PossibleEntityCollisionEvent as PECE, DamageEvent as DE
from enums.entity_enums import EntityType as ET, CollisionEntityTarget as CET, DirectionState as DS

class CollisionManager():
    def __init__(self):
        self.recent_collisions = []
        self.recent_attack_collisions = []
        # so the recent collisions will work like player controller checking for new inputs for now
        # not actually good, as it means once hit by an attack can't be hit again until no longer colliding,
        # but it's a quickly implemented way to prevent multiple damage events from a single hitbox lingering on an entity. rework that later

        # could do attacker, target, weapon type of collision tracking with a timestamp/frame count for the value
        self.collision_queue = []

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
        new_events = []
        for event in self.collision_queue:
            match event:
                case PACE():
                    new = self.handle_attack_collision(event, player, entities)
                    new_events.extend(new)
                # case PECE():
                #     new = self.handle_entity_collision(event, player, entities)
                #     new_events.extend(new)
        self.collision_queue.clear()
        return new_events

    def handle_attack_collision(self, event, player, entities):
        # NOTE will eventually change entitiy references to use ids instead of direct references

        # also clean up this method later, it's a bit messy

        entity = event.origin
        weapon = entity.weapon
        attack_position = event.attack_position
        hitbox = weapon.get_current_hitbox()
        if event.target_type == CET.ENEMY:
            targets = entities
        elif event.target_type == CET.PLAYER:
            targets = [player]
        else:
            targets = entities + [player]
        hits = self.check_collision_entities(targets, hitbox, attack_position)
        damage_events = []
        new_recent_attacks = []

        for hit in hits:
            new_recent_attacks.append((weapon, hit))
            new_recent_attacks.append((weapon, hit))
            if (weapon, hit) in self.recent_attack_collisions:
                continue  # already registered this collision recently
            damage_event = DE(weapon, hit, weapon.damage)
            damage_events.append(damage_event)

        self.recent_attack_collisions = new_recent_attacks
        return damage_events



    def check_collision_entities(self, entities: list, w_h: tuple, pos_a: tuple):
        hits = []
        # just use AABB for now
        for entity in entities:
            pos_b = entity.position
            b_w_h = entity.w_h
            if (pos_a[0] < pos_b[0] + b_w_h[0] and pos_b[0] < pos_a[0] + w_h[0] and pos_a[1] < pos_b[1] + b_w_h[1] and pos_b[1] < pos_a[1] + w_h[1]):
                hits.append(entity)
        return hits
