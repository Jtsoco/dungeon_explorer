from app_level.menu.menu_data import MenuData
from app_level.menu.menu_option import MenuOption, CharacterMenuOption
from app_level.menu.menu_component import MenuComponent, CharacterSelectMenuComponent
from app_level.app_enums import MenuCommandTypes, MenuState
from enums.entity_enums import EntityType
import pyxel

menu_registry = {
    MenuState.MAIN_MENU: [
        ("Start Game", MenuState.GAME),

        ("Options", MenuState.OPTIONS),
    ],
    MenuState.PAUSE_MENU: [
        ("Resume", MenuState.GAME),
        ("Options", MenuState.OPTIONS),
        ("Inventory", MenuState.INVENTORY),
        ("Quit to Main Menu", MenuState.MAIN_MENU)
    ]
}
def setup_main_menu():
    # honestly don't need a full music manager for menu, just this for now
    pyxel.playm(1, loop=True)
    main_menu = MenuData(MenuState.MAIN_MENU, title="Main Menu")
    main_menu_component = MenuComponent(pos=(24, 24), x_offset=0, y_offset=16)
    position_x = 24
    position_y = 24

    for option_text, action in menu_registry[MenuState.MAIN_MENU]:
        menu_option = MenuOption(text=option_text, position=(position_x, position_y), action=action)
        main_menu_component.add_option(menu_option)
        position_y += 16

    main_menu.add_component(main_menu_component)

    character_options = [
        EntityType.PLAYER,
        EntityType.PLAYER_RONIN
    ]

    # character_select component
    character_select_component = CharacterSelectMenuComponent(pos=(24, position_y), x_offset=40, y_offset=0)

    for character in character_options:
        menu_option = CharacterMenuOption(character=character, position=(0,0), action=MenuState.CHARACTER_SELECT)
        character_select_component.add_horizontal_option(menu_option)
    position_y += 16

    main_menu.add_component(character_select_component)

    new_component = MenuComponent(pos=(24, position_y), x_offset=0, y_offset=16)
    new_option = ("Quit", MenuState.QUIT)
    menu_option = MenuOption(text=new_option[0], position=(position_x, position_y + 16), action=new_option[1])
    new_component.add_option(menu_option)
    main_menu.add_component(new_component)

    return main_menu

def setup_pause_menu(context=None):
    # context isn't used for now, will be soon
    pause_menu = MenuData(MenuState.PAUSE_MENU, title="Game Paused")
    position_x = 24
    position_y = 24
    pause_menu_component = MenuComponent(pos=(position_x, position_y), x_offset=0, y_offset=16)
    pause_menu.add_component(pause_menu_component)
    for option_text, action in menu_registry[MenuState.PAUSE_MENU]:
        menu_option = MenuOption(text=option_text, position=(position_x, position_y), action=action)
        pause_menu_component.add_option(menu_option)
        position_y += 16
    return pause_menu
