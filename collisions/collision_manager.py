from events_commands.events import PossibleAttackCollisionEvent as PACE, DamageEvent as DE, EntitySeparatedEvent as ESE, BoundaryCollisionEvent as BCE
from enums.entity_enums import EntityType as ET, CollisionEntityTarget as CET, DirectionState as DS
from base_manager import BaseManager
from events_commands.commands import LoadActiveAttackCollisionCommand as LAACC, LoadEntityCollisionCommand as LECC, LoadMultipleEntityCollisionCommand as LMECC, LoadMultipleBoundariesCollisionCommand as LMBCC, CollisionCommand

class CollisionManager(BaseManager):
    def __init__(self, context):
        super().__init__(context=context)

        # NOTE eventually refactor this to poll through active entities in the game world instead of using events to check things, but fine for now. going in depth on making a collision manager system could be a lot of fun
        self.active_entities = []
        self.active_attacks = []
        self.active_boundaries = []
        self.player = None

        self.recent_collisions = []
        self.recent_attack_collisions = []
        # so the recent collisions will work like player controller checking for new inputs for now
        # not actually good, as it means once hit by an attack can't be hit again until no longer colliding,
        # but it's a quickly implemented way to prevent multiple damage events from a single hitbox lingering on an entity. rework that later

        # could do attacker, target, weapon type of collision tracking with a timestamp/frame count for the value
        self.collision_queue = []

    # purpose of this class is to receive possible collision events, then  determine if anything needs to be done about them
    def setup_bus(self):
        self.context.bus.register_command_listener(CollisionCommand, self)

    def handle_events(self, events):
        # will receive a list of possible collision events
        pass

    def handle_command(self, command):
        match command:
            case LAACC():
                self.load_active_attack_collision(command)
            case LECC():
                self.load_entity_collision(command)
            case LMECC():
                self.active_entities.extend(command.entities)
            case LMBCC():
                self.load_active_boundaries(command)
        # adds a command to be acted upon

    def handle_event(self, event):
        pass

    # event for PossibleAttackCollision will have attacker, weapon, included. weapon includes hitbox and damage info
    # event for PossibleEntityCollision
    def register_collision(self, possible_collision_event):
        self.collision_queue.append(possible_collision_event)

    def old_update(self, player, entities, boundaries):
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

    def handle_attack_collision(self, attacker):
        # NOTE will eventually change entitiy references to use ids instead of direct references

        # also clean up this method later, it's a bit messy

        weapon = attacker.weapon
        attack_position = weapon.get_position(attacker)
        hitbox = weapon.get_current_hitbox()
        if self.recent_attack_collisions:
            print('hi')
        if weapon.target_type == CET.ENEMY:
            targets = self.active_entities
        elif weapon.target_type == CET.PLAYER:
            targets = [self.player]
        else:
            targets = self.active_entities + [self.player]
        hits = self.check_collision_entities(targets, hitbox, attack_position)
        damage_events = []
        new_recent_attacks = []

        for hit in hits:
            # hits are the entity hit
            new_recent_attacks.append((weapon, hit))
            if (weapon, hit) in self.recent_attack_collisions:
                continue  # already registered this collision recently
            damage_event = DE(attacker, hit, weapon.damage, knockback=weapon.knockback)
            damage_events.append(damage_event)

        return damage_events, new_recent_attacks

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
            if entity.rect.is_colliding(pos_a, w_h):
                hits.append(entity)

        return hits

    def check_collision(self, pos_a, w_h_a: tuple, pos_b, w_h_b: tuple):
        # AABB collision check
        if (pos_a[0] < pos_b[0] + w_h_b[0] and pos_b[0] < pos_a[0] + w_h_a[0] and pos_a[1] < pos_b[1] + w_h_b[1] and pos_b[1] < pos_a[1] + w_h_a[1]):
            return True
        return False

    def update(self):
        for command in self.queued_commands:
            self.handle_command(command)
        self.queued_commands.clear()
        for event in self.queued_events:
            self.handle_event(event)
        self.queued_events.clear()
        return self.handle_updates()


    def handle_updates(self):
        # for now, this will handle saved commands/events to be processed each frame
        # separate out into own methods later
        events = []
        p_rect = self.player.rect
        new_recent_collisions = []
        for entity in self.active_entities:
            rect = entity.rect
            if rect.is_rect_colliding(p_rect):
                if entity.touch_damage:
                    # change to damage command
                    new_recent_collisions.append((entity, self.player))
                    if (entity, self.player) in self.recent_collisions:
                        continue  # already registered this collision recently
                    damage_event = DE(entity, self.player, entity.touch_damage, knockback=entity.knockback)
                    events.append(damage_event)
                else:
                    separation_event = ESE(entity, self.player)
                    events.append(separation_event)
        new_recent_attacks = []

        for attacking_entity in self.active_attacks:
            damage_events, additional_recent_attacks = self.handle_attack_collision(attacking_entity)
            events.extend(damage_events)
            new_recent_attacks.extend(additional_recent_attacks)

        self.recent_attack_collisions = new_recent_attacks

        for boundary in self.active_boundaries:
            boundary_rect = boundary.rect
            if boundary_rect.is_rect_colliding(p_rect):
                new_recent_collisions.append((self.player, boundary))
                if (self.player, boundary) in self.recent_collisions:
                    continue  # already registered this collision recently
                boundary_event = BCE(self.player, boundary)
                events.append(boundary_event)
        self.recent_collisions = new_recent_collisions
        # TODO for now return these events and they'll be acted upon in the current game loop, but eventually have the collision manager send them through the event bus
        return events


        # change these to commands to do something if they have only one target, like damage or separate entities, and keep as events for things that may have multiple targets. will boundary be an event or command? probably event for now
        # I don't plan on having this return events right now, it will primarily send things through the bus

    # Loading and unloading entities and attacks for collision checking
    def load_entity_collision(self, command):
        if command.load:
            self.active_entities.append(command.entity)
        else:
            if command.entity in self.active_entities:
                self.active_entities.remove(command.entity)

    def load_multiple_entity_collision(self, command):
        if command.load:
            self.active_entities.extend(command.entities)
        else:
            for entity in command.entities:
                if entity in self.active_entities:
                    self.active_entities.remove(entity)

    def load_active_attack_collision(self, command):
        if command.load:
            self.active_attacks.append(command.attacking_entity)
        else:
            if command.attacking_entity in self.active_attacks:
                self.active_attacks.remove(command.attacking_entity)

    def load_active_boundaries(self, command):
        if command.load:
            self.active_boundaries.extend(command.boundaries)
        else:
            for boundary in command.boundaries:
                if boundary in self.active_boundaries:
                    self.active_boundaries.remove(boundary)
