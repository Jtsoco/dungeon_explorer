from entity.entity_data import EntityData
from entity.animation_data import AnimationData
from attack.weapon_data import WeaponData
from enums.entity_enums import EntityType as ET, EntityCategory as EC

def spawn_player(position: tuple = (0, 0)) -> EntityData:
    player_setup = {
        "health": 100,
        "position": list(position),
        "w_h": (8, 8),
        "player": True,
        "entity_type": ET.PLAYER,
        "entity_category": EC.GROUND,
        "animation_data": AnimationData(),
        "weapon_data": WeaponData(),
        "speed": 2

    }
    player_data = EntityData(**player_setup)
    return player_data
