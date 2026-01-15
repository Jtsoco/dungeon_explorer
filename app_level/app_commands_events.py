from app_level.app_enums import MenuCommandTypes, MenuState
class AppEvent():
    def __init__(self, name: str = "GenericAppEvent"):
        self.name = name
# this is separate from games own events and commands class system

class AppCommand():
    def __init__(self, name: str = "GenericAppCommand"):
        self.name = name

class MenuCommand(AppCommand):
    def __init__(self, action: MenuCommandTypes.SELECT):
        super().__init__(name="MenuCommand")
        self.action = action

class StateChangeEvent(AppEvent):
    def __init__(self, new_state: MenuState):
        super().__init__(name="StateChangeEvent")
        self.new_state = new_state

class SetMainCharacterCommand(AppCommand):
    def __init__(self, entity_data):
        super().__init__(name="SetMainCharacterCommand")
        self.entity_data = entity_data
