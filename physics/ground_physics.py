from events_commands.commands import Command, MovementCommand, MoveCommand, JumpCommand, AddMomentumCommand, EntitySeparationCommand
from events_commands.events import LandedEvent, StartedFallingEvent, AddMomentumEvent as AME
from enums.entity_enums import MovementState as MS
from enums.entity_enums import DirectionState as DS
from magic_numbers import GRAVITY, TERMINAL_VELOCITY, MIN_SEC_MOMENTUM_THRESHOLD, AIR_RESISTANCE, GROUND_FRICTION


class GroundPhysics:
    # for making this a flying vs other type, maybe just have a swappable grav component or such that is swapped depending on the type of entity in entity category
    def __init__(self, context=None, local_bus=None):
        self.context = context
        self.gravity = GRAVITY
        self.local_bus = local_bus
        # for now it holds gravity, allowing for custom gravity, but revisit this later and decide whether to use composition for different physics types like a water level or flying level
        # for now, it's simple enough leave it as is
        # hell maybe i'll make a gravity magic, and it might affect things differently later

    def update(self, data, context=None):
        context = context or self.context
        if context is None:
            raise ValueError("PlayerPhysics.update needs a context value")
        # will eventually receive tile context too to know if it collides with walls/floors
        # haven't decided if it only gets tile context, or any other relevant context info
        # for now, its the startup context it has access to with tile context in that
        # update position based on velocity
        # data.rect.position[0] += data.velocity[0]

        # returns a dict with all tiles around the player as values, keys being their relative position
        self.horizontal_motion(data, context)
        self.vertical_motion(data, context)
        ground_beneath = self.ground_beneath_player(data, context)
        self.secondary_update(data, context, ground_beneath)
        # if there are any events after this, added here. might not actually be any, but jump will have some state change events probably

        # data.rect.position[1] += data.velocity[1]
        # gravity and other physics would go here

        # once tile context is added, check for collisions and then implement a backstep if neeed

    def secondary_update(self, data, context, ground_beneath):
        if ground_beneath:
            data.secondary_momentum[0] = data.secondary_momentum[0]*GROUND_FRICTION
            if abs(data.secondary_momentum[0]) < MIN_SEC_MOMENTUM_THRESHOLD:
                data.secondary_momentum[0] = 0
            data.secondary_momentum[1] = 0
        else:
            data.secondary_momentum[0] = data.secondary_momentum[0]*AIR_RESISTANCE
            # so the actual secondary momentum will eventually be cancelled out by gravity, and reset when it hits the ground, but secondary will be cancelled out more quickly on the ground

    def horizontal_motion(self, data, context):
        # will eventually implement collision detection here so that
        # if the speed is greater than brick size, it will divide the movement into many smaller movements and check each for collision, ending movement if collision detected
        # need to create code to handle a sprites position overlapping tiles, grabbing those tiles it's not overlapping with. for that, will need to edit tile context to allow that.
        movement = data.velocity[0] + data.secondary_momentum[0]
        if self.chunk_movement(movement, data, context, axis=0):
            data.secondary_momentum[0] = 0
        # for now just check collision with all, no need to make it only check the sides it could move into based on direction

    def chunk_movement(self, movement, data, context, axis=0, chunk_size=8):
        # breaks movement into smaller chunks to properly check for collisions with tiles and walls and such, does allow for dashing past enemies at high speeds which is kinda cool so keeping that part for now rather than integrate enemy collisions
        sign = 1 if movement > 0 else -1
        remaining_movement = abs(movement)
        loops = int(remaining_movement // chunk_size)
        initial_movement = remaining_movement % chunk_size
        for _ in range(loops):
            data.rect.position[axis] += sign * chunk_size
            if self.check_tile_collisions(data, context):
                self.stepback(data, -sign * chunk_size, context, axis=axis)
                return True
        if initial_movement > 0:
            data.rect.position[axis] += sign * initial_movement
            if self.check_tile_collisions(data, context):
                self.stepback(data, -sign * initial_movement, context, axis=axis)
                return True
        return False
        # returns true if tile collision occurred during chunked movement

    def check_tile_collisions(self, data, context):
        x, y = int(data.rect.position[0]), int(data.rect.position[1])
        tiles = context.tile_context.get_touching_bricks(x, y, data.rect.width, data.rect.height)
        return self.has_tile_collision(tiles, context)

    def has_tile_collision(self, tiles, context):
        for tile in tiles:
            if tile[1] <= context.data_context.collideable_tile_y:
                return True
        return False

    def vertical_motion(self, data, context):
        movement = data.velocity[1] + data.secondary_momentum[1]
        collided = self.chunk_movement(-movement, data, context, axis=1)
        data.rect.position[1] = int(data.rect.position[1])  # so if a float is used renderer sometimes makes the player stand in the floor, and keeping it a float while rendering uses ints means movement gets jittery, just requiring int for y positions makes everything smoother
        # this does, however, affect how much jump power can make someone go up

        match data.movement_state:
            case MS.JUMPING | MS.FALLING:
                if collided:

                    if self.downward_momentum(data):
                        # landed, wait naming of method is confusing, rename it
                        event = LandedEvent()
                        data.velocity[1] = 0
                        data.secondary_momentum[1] = 0
                        self.local_bus.send_event(event)
                        return
                    else:
                        # hit head/ceiling, or started falling
                        event = StartedFallingEvent()
                        data.velocity[1] = 0
                        data.secondary_momentum[1] = 0
                        self.local_bus.send_event(event)
                elif data.movement_state == MS.JUMPING and self.downward_momentum(data):
                    # started falling
                    event = StartedFallingEvent()
                    self.local_bus.send_event(event)


            case _:
                if collided:
                    # in this instance, they weren't falling but just standing, had momentum applied to them for some reason and were pushed to the ground, but state doesn't actually change they are still standing, so just cancel that downward momentum
                    data.velocity[1] = 0
                    data.secondary_momentum[1] = 0
                    return
                ground_beneath = self.ground_beneath_player(data, context)
                if ground_beneath:
                    data.velocity[1] = 0
                    # TODO possibly don't even need to set velocity to 0 here since gravity update won't happen if on ground, revisit and test later,
                    return
                else:
                    event = StartedFallingEvent()
                    self.local_bus.send_event(event)

        # it gets to update gravity if not on ground
        self.update_gravity(data, context)


    def ground_beneath_player(self, data, context):
        x_start = int(data.rect.position[0])

        y_value = int(data.rect.position[1] + data.rect.height)
        bricks = context.tile_context.get_touching_bricks(x_start, y_value, data.rect.width, 1)
        return self.has_tile_collision(bricks, context)


    def downward_momentum(self, data):
        if data.velocity[1] + data.secondary_momentum[1] < 0:
            return True
        return False

    def update_gravity(self, data, context):
        # simple gravity, add proper gravity later
        gravity = self.gravity
        terminal_velocity = -5
        data.velocity[1] += gravity
        if (data.velocity[1] + data.secondary_momentum[1]) < terminal_velocity:
            data.velocity[1] = terminal_velocity

    def stepback(self, data, reverse, context, axis=0):
        sign = -1 if reverse < 0 else 1
        # moves back one pixel at a time until no longer colliding
        while self.check_tile_collisions(data, context):
            data.rect.position[axis] += sign


    def handle_event(self, event):
        pass

    def apply_momentum_command(self, command):
        command.entity.secondary_momentum[0] += command.momentum_vector[0]
        command.entity.secondary_momentum[1] += command.momentum_vector[1]

    def handle_command(self, command, data=None):
        # TODO there is overlap of internal entity_manager derived commands and external commands, separate that later so data=None is not needed

        # returns a tuple of events and commands
        match command:
            # if commands get to big divide into movment commands and such but for now just use in handle command and then separate logic code
            case MoveCommand():
                self.process_move_command(command, data)
            case JumpCommand():
                # implement jump logic later
                self.jump(command, data)
            case AddMomentumCommand():
                self.apply_momentum_command(command)
            case EntitySeparationCommand():
                self.entity_separation(command, data)

    def entity_separation(self, command, data):
        entity_a = command.entity
        entity_b = command.entity_b
        b_only = command.b_only
        impossible = False
        new_impossible = False
        RIGHT = entity_a.rect.position[0] < entity_b.rect.position[0]
        right = RIGHT
        while entity_a.rect.is_rect_colliding(entity_b.rect) and not impossible:
            # try to push out b
            if not new_impossible:
                new_impossible = self.pushout_entity_b(entity_a, entity_b, right)
                # if b can't be pushed out, push out a, using new impossible to track whether last push was possible
                if new_impossible:
                    right = not right
            else:
                # if b couln't be pushed out, push out until a can't be either
                impossible = self.pushout_entity_b(entity_b, entity_a, right)


    def pushout_entity_b(self, entity_a, entity_b, RIGHT):
        impossible = False
        if RIGHT:
            entity_b.rect.position[0] += 1
            stepback = 1
        else:
            entity_b.rect.position[0] -= 1
            stepback = -1
        if self.check_tile_collisions(entity_b, self.context):
            # if entity b hits a wall while being pushed out, then stop pushing it out
            entity_b.rect.position[0] -= stepback
            impossible = True
        return impossible





    def jump(self, command, data):
        # actually probably don't need the command
        data.velocity[1] = data.jump_strength

    def process_move_command(self, command, data):

        match command.direction:
            case DS.LEFT:
                data.velocity[0] = -data.move_speed
            case DS.RIGHT:
                data.velocity[0] = data.move_speed
            case DS.HALT:
                data.velocity[0] = 0
