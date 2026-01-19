from enums.entity_enums import MovementState as MS, ActionState as AS, DirectionState as DS, InputEnums as IE, PowerUpStates as PUS, SHIELD_ACTION_STATE as SAS
from events_commands.events import InputEvent, StartedFallingEvent, LandedEvent, StateChangedEvent, AttackFinishedEvent, BlockFinishedEvent, ActionFailedEvent
from events_commands.commands import MoveCommand, JumpCommand, AttackCommand, EffectCommand, SoundCommand, EndBlockCommand, StartBlockCommand, BreakBlockCommand
from audio.sound_enums import SoundEnum
from enums.effects_enums import ParticleEffectType as PET, EffectType
class DefaultStateMachine():
    def __init__(self, bus, local_bus):
        self.bus = bus
        self.events = []
        self.local_bus = local_bus
    # in here is the logic to determine what the next state is based on the previous

    def input_events(self, data, input_events):
        # will it set the data to hold state of moving/idle, or let something else handle that?
        # it may be fine if it only changes that state, but it may be important to only let it do that once during a loop
        # then again it only gets the input events once, need to think about this more
        last_states = [data.movement_state, data.action_state, data.direction_state]

        for event in input_events:
            match event.input_type:
                case IE.MOVE:
                    self.set_walking(data, event.direction)
                case IE.STOP_MOVE:
                    self.stop_move(data)
                case IE.JUMP:
                    self.jump_input(data)
                case IE.ATTACK:
                    self.attack_input(data)
                case IE.BLOCK:
                    self.block_input(data)
                case IE.STOP_BLOCK:
                    self.stop_block_input(data)


        new_states = [data.movement_state, data.action_state, data.direction_state]
        if new_states != last_states:
            self.local_bus.send_event(StateChangedEvent())

    def block_input(self, data):
        match data.action_state:
            case AS.NONE:
                data.action_state = AS.DEFENDING
                self.local_bus.send_command(StartBlockCommand())

    def stop_block_input(self, data):
        match data.action_state:
            case AS.DEFENDING:
                self.local_bus.send_command(EndBlockCommand())

    def attack_input(self, data):
        match data.action_state:
            case AS.NONE:
                data.action_state = AS.ATTACKING
                self.local_bus.send_command(AttackCommand())

    def jump_input(self, data):
        match data.movement_state:
            case MS.IDLE | MS.WALKING:
                data.movement_state = MS.JUMPING
                self.local_bus.send_command(JumpCommand())
                self.bus.send_command(SoundCommand(sound_enum=SoundEnum.JUMP))  # JUMP sound
            case MS.JUMPING | MS.FALLING:
                if self.can_double_jump(data):
                    data.movement_state = MS.JUMPING
                    self.local_bus.send_command(JumpCommand())
                    self.bus.send_command(EffectCommand(pos=data.rect.position))
                    self.bus.send_command(SoundCommand(sound_enum=SoundEnum.JUMP))  # LAND sound on double jump

    def can_double_jump(self, data):
        if PUS.DOUBLE_JUMP in data.power_ups:
            if data.power_ups[PUS.DOUBLE_JUMP]:
                data.power_ups[PUS.DOUBLE_JUMP] = False  # mark as used
                return True

        return False

    def set_walking(self, data, event_type):
        # this will eventually decide
        match data.movement_state:
            case MS.IDLE:
                data.movement_state = MS.WALKING
        # event type is DS.LEFT or DS.RIGHT
        data.direction_state = event_type
        self.local_bus.send_command(MoveCommand(event_type))

    def stop_move(self, data):
        match data.movement_state:
            case MS.WALKING:
                data.movement_state = MS.IDLE
        self.local_bus.send_command(MoveCommand(DS.HALT))

    def state_updates(self, data, updates):
        last_states = [data.movement_state, data.action_state, data.direction_state]
        for event in updates:
            match event:
                case StartedFallingEvent():
                    data.movement_state = MS.FALLING
                case LandedEvent():
                    self.landed_update(data)
                    if PUS.DOUBLE_JUMP in data.power_ups:
                        data.power_ups[PUS.DOUBLE_JUMP] = True  # reset double jump on land
                    if data.rect.height > 8:
                        additional_height = 8
                    else:
                        additional_height = 0
                    self.bus.send_command(EffectCommand(pos=data.rect.position, sub_type=PET.LAND_DUST, effect_type=EffectType.PARTICLE, additional_height=additional_height))
                    self.bus.send_command(SoundCommand(sound_enum=SoundEnum.LAND))  # LAND sound
                case AttackFinishedEvent():
                    data.action_state = AS.NONE
                case BlockFinishedEvent():
                    data.action_state = AS.NONE
                case ActionFailedEvent():
                    data.action_state = AS.NONE
        new_states = [data.movement_state, data.action_state, data.direction_state]
        # events, commands = [], []
        if new_states != last_states:
            self.local_bus.send_event(StateChangedEvent())

    def landed_update(self, data):
        # if it's not 0, then they're walking
        if not data.velocity[0]:
            data.movement_state = MS.IDLE
        else:
            data.movement_state = MS.WALKING
