from events_commands.events import PossibleAttackCollisionEvent as PACE, DamageEvent as DE, EntitySeparatedEvent as ESE, BoundaryCollisionEvent as BCE
from enums.entity_enums import EntityType as ET, CollisionEntityTarget as CET, DirectionState as DS
from base_manager import BaseManager

class CollisionManager(BaseManager):
    def __init__(self):

        # NOTE eventually refactor this to poll through active entities in the game world instead of using events to check things, but fine for now. going in depth on making a collision manager system could be a lot of fun
        self.active_entities = []
        self.active_attacks = []
        self.player = None

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

    def notify_command(self, command):
        pass
        # adds a command to be acted upon
    def handle_event(self, event):
        pass

    # event for PossibleAttackCollision will have attacker, weapon, included. weapon includes hitbox and damage info
    # event for PossibleEntityCollision
    def register_collision(self, possible_collision_event):
        self.collision_queue.append(possible_collision_event)

    def update(self, player, entities, boundaries):
        new_events = []
        for event in self.collision_queue:
            match event:
                case PACE():
                    new = self.handle_attack_collision(event, player, entities)
                    new_events.extend(new)
        new_recent_collisions = []
        for entity in entities:
            # if an entity touches another, return damage touch event if touch damage, regular entity separation event otherwise, maybe a command to separate entities that's passed to physics

            # for now only check against player, don't care about other entities colliding with each other
            if self.check_collision(entity.position, entity.w_h, player.position, player.w_h):
                if entity.touch_damage:
                    new_recent_collisions.append((entity, player))
                    if (entity, player) in self.recent_collisions:
                        continue  # already registered this collision recently
                    damage_event = DE(entity, player, entity.touch_damage, knockback=entity.knockback)
                    new_events.append(damage_event)
                else:
                    separation_event = ESE(entity, player)
                    new_events.append(separation_event)

        boundary_events = self.check_player_boundaries(player, boundaries)
        for boundary_event in boundary_events:
            new_recent_collisions.append((boundary_event.entity, boundary_event.boundary))
            if (boundary_event.entity, boundary_event.boundary) not in self.recent_collisions:
                new_events.append(boundary_event)

        self.recent_collisions = new_recent_collisions
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
            if (weapon, hit) in self.recent_attack_collisions:
                continue  # already registered this collision recently
            damage_event = DE(entity, hit, weapon.damage, knockback=weapon.knockback)
            damage_events.append(damage_event)

        self.recent_attack_collisions = new_recent_attacks
        return damage_events

    def check_player_boundaries(self, entity, boundaries):
        hits = []
        for boundary in boundaries:
            if self.check_collision(entity.position, entity.w_h, boundary.position, boundary.w_h):
                hits.append(BCE(entity, boundary))
        return hits

    def check_collision_entities(self, entities: list, w_h: tuple, pos_a: tuple):
        hits = []
        # just use AABB for now
        for entity in entities:
            pos_b = entity.position
            b_w_h = entity.w_h
            if self.check_collision(pos_a, w_h, pos_b, b_w_h):
                hits.append(entity)
        return hits

    def check_collision(self, pos_a, w_h_a: tuple, pos_b, w_h_b: tuple):
        # AABB collision check
        if (pos_a[0] < pos_b[0] + w_h_b[0] and pos_b[0] < pos_a[0] + w_h_a[0] and pos_a[1] < pos_b[1] + w_h_b[1] and pos_b[1] < pos_a[1] + w_h_a[1]):
            return True
        return False

    def handle_updates(self):
        # for now, this will handle saved commands/events to be processed each frame
        # separate out into own methods later
        events = []
        p_rect = self.player.rect
        for entity in self.active_entities:
            rect = entity.rect
            if rect.colliderect(p_rect):
                if entity.touch_damage:
                    # change to damage command
                    damage_event = DE(entity, self.player, entity.touch_damage, knockback=entity.knockback)
                    events.append(damage_event)
                else:
                    separation_event = ESE(entity, self.player)
                    events.append(separation_event)
        new_recent_attacks = []

        for attacking_entity in self.active_attacks:
            weapon = attacking_entity.weapon
            hitbox = weapon.get_current_hitbox()
            weapon_position = weapon.get_position(attacking_entity)
            if attacking_entity.target_type == CET.ENEMY:
                targets = self.active_entities
            elif attacking_entity.target_type == CET.PLAYER:
                targets = [self.player]
            else:
                targets = self.active_entities + [self.player]
            for target in targets:
                target_rect = target.rect
                if target_rect.is_colliding(weapon_position, hitbox):
                    damage_event = DE(attacking_entity, target, weapon.damage, knockback=weapon.knockback)
                    events.append(damage_event)
                    new_recent_attacks.append((weapon, target))
        self.recent_attack_collisions = new_recent_attacks

        for boundary in self.boundaries:
            boundary_rect = boundary.rect
            if boundary_rect.is_rect_colliding(p_rect):
                boundary_event = BCE(self.player, boundary)
                events.append(boundary_event)
        # change these to commands to do something if they have only one target, like damage or separate entities, and keep as events for things that may have multiple targets. will boundary be an event or command? probably event for now
        # I don't plan on having this return events right now, it will primarily send things through the bus
