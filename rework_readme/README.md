# ⚔️ Dungeon Explorer ⚔️

**A retro nes style dungeon crawler built in Python with Pyxel**

![Dungeon Explorer Gif](images/platformer.gif)

## About

A side-scrolling action game exploring a dungeon. Features multiple weapons and shields, a shield break system, boss fights, and two playable characters.

## The Game

### How to Play

Try it on my [portfolio site](https://jtsoco.github.io/portfolio/)

Controls:

| Key | Action |
|-----|--------|
| ⬅️ ➡️ | Move |
| Space | Jump |
| D | Attack |
| S | Block |
| Tab | Pause / Inventory |
| Enter | Confirm |


### Characters

Choose your adventurer at the start screen.
| Name | Image | Weapon | Shield | Info |
| ------- | ----- | ---- | --- | ------- |
| Knight | ![Knight](images/knight.png){width=88} | ![Shortsword](images/shortsword.png){height=88} | ![IronShield](images/iron_shield.png){width=88} | Sturdy shield and trustworthy sword, can last a while in combat without breaking. |
| Ronin | ![Ronin](images/ronin.png){width=88} | ![Katana](images/katana.png){width=88} | ![ParryDagger](images/parry_dagger.png){width=88} | Quick to attack and quick to block, excels in fast combat. However, when blocking the guard is soon to break. |


### Bestiary


| Name | Enemy | Description | Danger |
| ----- | ---- | ----------- | ------ |
| Skull | ![SkullEnemy](images/skull.png){width=88} | A simple skull enemy, roams the map. Has touch damage. | ☠️ |
| Dark Knight | ![DarkKnight](images/dark_swordsman.png){width=88} | A dark knight, will pursue when trespassers are close. | ☠️☠️ |
| Winged Knight | ![WingedKnight](images/flyingKnight.png){width=88} | The first boss. Defeating it will earn you the double jump ability, but beware, it's glaive is deadly. | ☠️☠️☠️ |
| Dark Lord | ![DarkLord](images/darkLord.png){width=88} | The final boss. Beware the flame he wields. | ☠️☠️☠️☠️ |


### Arsenal

Weapons

| Gif | Weapon | Damage | Style | Location |
| --- | ------ | ------ | ----- | -------- |
| ![Shortsword](images/gifs/shortSword.gif){width=300} | Shortsword | 50 | Strong, reliable all rounder. | Knight default |
| ![Katana](images/gifs/katana.gif){width=300} | Katana | 50 | Fast to attack, but low knockback. | Ronin default |
| ![Glaive](images/gifs/glaive.gif){width=300} | Glaive | Heavy melee with an air attack | Map pickup |
| ![FireBlast](images/gifs/fireball.gif){width=300} | Fire Blast | 30 | Ranged flame stream, low damage but good knockback | Map pickup |

Shields

| Gif | Shield | Stamina | Style | Location |
| --- | ------ | ------ | ----- | -------- |
| ![IronShield](images/gifs/ironShield.gif){width=300} | Iron Shield | 100 | Balanced blocker | Knight default |
| ![ParryDagger](images/gifs/parry.gif){width=300} | Parry Dagger | 50 | Quick Parry, fast stamina regen, but quick to break. | Ronin default |
| ![TowerShield](images/gifs/towerShield.gif){width=300} | Tower Shield | 500 | Massive shield, slow to block but hard to break. | Map pickup |

**Shield Break**: Every block drains stamina. If your stamina hits zero, your shield breaks and you can't block until shield recovery and stamina regens. Time your blocks carefully.

### The World

The dungeon is a simple 6x2 grid of rooms that load and unload dynamically as you explore, lending itself to being added onto without worries of performance. Each room is populated with enemies, items, and boundaries - step through a rooms boundary and rooms just out of reach will load ready for you to come close.

Health drops from enemies (30% chance), along with weapons, shields, and health pickups scattered around the map are yours to find. Access your inventory from the pause menu to swap gear as you go.


## Under the Hood

Tech Stack

- Python + [Pyxel](https://github.com/kitao/pyxel) - retro game engine, 128x128 resolution, 16 colors, 4 sound channels
- All assets were created by me using pyxels built in editor, saved in the dungeon_explorer_assets.pyxres resource file.

Managers communicate through an event/command bus, entities don't communicate directly. Each enemy type has its own AI controller with states like PATROL, CHASE, ATTACK, JUMP_ATTACK.

Game Update Loop

```mermaid
flowchart TD
    Start([start frame]) --> Entities["Entity Manager: update all entities"]
    Entities --> Collision["collision_manager.update()"]
    Collision --> Effects["effects_manager.update()"]
    Effects --> Damage["damage_manager.update()"]
    Damage --> Cell["cell_manager.update()"]
    Cell --> EntityPost["entity_manager.update()"]
    EntityPost --> HUD["hud_manager.update()"]
    HUD --> Sound["sound_effects_manager.update()"]
    Sound --> Camera["scene_manager.camera.update()"]
    Camera --> LoopCheck{still running?}
    LoopCheck -- yes --> Start
    LoopCheck -- no --> End([end frame])

    subgraph BusGroup[" "]
        Bus{{"Game Level event / command bus (routes to listeners)"}}
    end

    %% each updater may post events/commands to the bus
    Entities -.-> Bus
    Collision -.-> Bus
    Effects -.-> Bus
    Damage -.-> Bus
    Cell -.-> Bus

    %% bus fans events out to interested systems
    Bus -->|dispatch| EntityManager
    Bus -->|dispatch| CellManager
    Bus -->|dispatch| EffectsManager
    Bus -->|dispatch| HUDManager
    Bus -->|dispatch| SoundEffectsManager
    Bus -->|dispatch| SceneManager



```

Entity Update Loop

```mermaid

flowchart TD
    GAMEBUS["Game Loop Bus"]
    UE["update_entity(entity)"] --> R["reset_local()"]
    R --> I["get input (controller + state machine)"]
    I --> A["animation_manager.update(entity)"]
    A --> P["process_loop(entity)"]
    P --> PHY["physics_manager.update(entity)"]
    PHY --> ATK["attack_manager.update(entity)"]
    ATK --> | Sound Commands and Events | GAMEBUS
    ATK --> DEF["defense_manager.update(entity)"]
    DEF --> HS["handle_state_updates(entity)"]
    DEF --> | Sound Commands and Events | GAMEBUS
    HS --> EXIT["End Loop"]


    subgraph P["process_loop(entity)"]
        LCHK{"local_events or commands?"}
        HANDLE["Handle Event/Command"]
        LCHK -- yes --> EVT["pop event"] --> HANDLE
        LCHK -- yes --> CMD["pop command"] --> HANDLE
        HANDLE --> LCHK
        LCHK -- no --> END("exit loop")
    end
```


Extending the Game

| Want to add... | What to touch |
| -------------- | ------------- |
| New Enemy | Create a controller in entity/controllers, register in entity_setup.py, add case with new entity enum type to use entity_setup function in cell_manager load_objects, add a spawnpoint to the map in the map editor |
| New weapon | Add information to attack/weapon_data.py + animations/attack_registry.py if a map pickup add to cell_manager load method, spawn item with weapon data. |
| New Shield | Add to defense/shield_data.py + animations/shield_registry.py if a map pickup add to cell_manager load method, spawn item with shield data. |
| New Item | Add to items/item_registry.py wire into cell_manager load method, add any necessary additions to item_manager |

## Roadmap

- [ ] formalize entity AI system for easy mix and match of behaviors
- [ ] Full Inventory Menu
- [ ] Additional enemy types
- [ ] Camera V2 using transitions
- [ ] Options menu for sound adjust
