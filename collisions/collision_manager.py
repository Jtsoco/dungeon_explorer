from events_commands.events import PossibleAttackCollisionEvent as PACE, BoundaryCollisionEvent as BCE
from enums.entity_enums import EntityType as ET, CollisionEntityTarget as CET, DirectionState as DS
from base_manager import BaseManager
from events_commands.commands import LoadActiveAttackCollisionCommand as LAACC, LoadEntityCollisionCommand as LECC, LoadMultipleEntityCollisionCommand as LMECC, LoadMultipleBoundariesCollisionCommand as LMBCC, CollisionCommand, DamageCommand as DC, EntitySeparationCommand as ESC

class CollisionManager(BaseManager):
    def __init__(self, context):
        super().__init__(context=context)

        # NOTE eventually refactor this to poll through active entities in the game world instead of using events to check things, but fine for now. going in depth on making a collision manager system could be a lot of fun
        self.active_entities = set()
        self.active_attacks = set()
        self.active_boundaries = set()
        self.player = None

        self.recent_collisions = set()
        self.recent_attack_collisions = set()
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
                self.load_multiple_entity_collision(command)
            case LMBCC():
                self.load_active_boundaries(command)
        # adds a command to be acted upon

    def handle_event(self, event):
        pass

    # event for PossibleAttackCollision will have attacker, weapon, included. weapon includes hitbox and damage info
    # event for PossibleEntityCollision
    def register_collision(self, possible_collision_event):
        self.collision_queue.append(possible_collision_event)


    def handle_attack_collision(self, attacker):
        # NOTE will eventually change entitiy references to use ids instead of direct references

        # also clean up this method later, it's a bit messy

        weapon = attacker.weapon
        attack_position = weapon.get_position(attacker)
        hitbox = weapon.get_current_hitbox()
        if weapon.target_type == CET.ENEMY:
            targets = self.active_entities
        elif weapon.target_type == CET.PLAYER:
            targets = [self.player]
        else:
            targets = self.active_entities + [self.player]
        hits = self.check_collision_entities(targets, hitbox, attack_position)
        damage_commands = []
        new_recent_attacks = []

        for hit in hits:
            # hits are the entity hit
            new_recent_attacks.append((weapon, hit))
            if (weapon, hit) in self.recent_attack_collisions:
                continue  # already registered this collision recently
            damage_command = DC(attacker, hit, weapon.damage, knockback=weapon.knockback)
            damage_commands.append(damage_command)
        return damage_commands, new_recent_attacks


    def check_collision_entities(self, entities: list, w_h: tuple, pos_a: tuple):
        hits = []
        # just use AABB for now
        for entity in entities:
            if entity.rect.is_colliding(pos_a, w_h):
                hits.append(entity)

        return hits

    def update(self):
        for command in self.queued_commands:
            self.handle_command(command)
        self.queued_commands.clear()
        for event in self.queued_events:
            self.handle_event(event)
        self.queued_events.clear()
        self.handle_updates()


    def handle_updates(self):
        # for now, this will handle saved commands/events to be processed each frame
        # separate out into own methods later
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
                    damage_command = DC(entity, self.player, entity.touch_damage, knockback=entity.knockback)

                    self.context.bus.send_command(damage_command)

                else:
                    separation_command = ESC(entity, self.player)
                    self.context.bus.send_command(separation_command)
        new_recent_attacks = []

        for attacking_entity in self.active_attacks:
            damage_commands, additional_recent_attacks = self.handle_attack_collision(attacking_entity)
            for command in damage_commands:
                self.context.bus.send_command(command)
            new_recent_attacks.extend(additional_recent_attacks)

        self.recent_attack_collisions = new_recent_attacks

        for boundary in self.active_boundaries:
            boundary_rect = boundary.rect
            if boundary_rect.is_rect_colliding(p_rect):
                new_recent_collisions.append((self.player, boundary))
                if (self.player, boundary) in self.recent_collisions:
                    continue  # already registered this collision recently
                boundary_event = BCE(self.player, boundary)
                self.context.bus.send_event(boundary_event)
        self.recent_collisions = new_recent_collisions
        # TODO for now return these events and they'll be acted upon in the current game loop, but eventually have the collision manager send them through the event bus


        # change these to commands to do something if they have only one target, like damage or separate entities, and keep as events for things that may have multiple targets. will boundary be an event or command? probably event for now
        # I don't plan on having this return events right now, it will primarily send things through the bus

    # Loading and unloading entities and attacks for collision checking
    def load_entity_collision(self, command):
        if command.load:
            if command.entity not in self.active_entities:
                self.active_entities.add(command.entity)

        else:
            if command.entity in self.active_entities:
                self.remove_entity(command.entity)

    def remove_entity(self, entity):
        if entity in self.active_entities:
            self.active_entities.remove(entity)
        if entity.weapon_active() and entity in self.active_attacks:
            self.active_attacks.remove(entity)

    def load_multiple_entity_collision(self, command):
        if command.load:
            self.active_entities.update(command.entities)

        else:
            for entity in command.entities:
                if entity in self.active_entities:
                    self.remove_entity(entity)

    def load_active_attack_collision(self, command):
        if command.load:
            self.active_attacks.add(command.attacking_entity)
        else:
            if command.attacking_entity in self.active_attacks:
                self.active_attacks.remove(command.attacking_entity)

    def load_active_boundaries(self, command):
        if command.load:
            self.active_boundaries.update(command.boundaries)
        else:
            for boundary in command.boundaries:
                if boundary in self.active_boundaries:
                    self.active_boundaries.remove(boundary)
