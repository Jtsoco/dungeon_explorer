from entity.entity_data import EntityData
from entity.animation_data import AnimationData
from attack.weapon_data import WeaponData
from enums.entity_enums import EntityType as ET, EntityCategory as EC, WeaponCategory as WC, CollisionEntityTarget as CET, PowerUpStates as PUS
from animations.attack_registry import WEAPON_STATS, WEAPONS_ANIMATIONS, WEAPONS_HITBOXES


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
    player_data.power_ups[PUS.DOUBLE_JUMP] = True  # give player double jump powerup for testing
    return player_data

# honestly could change weapon category to entity type, and apply weapon based on a mapping later, and consolidate loading into one function
def spawn_weapon(weapon_category: WC = WC.SHORTSWORD, target=CET.PLAYER) -> WeaponData:
    animations = WEAPONS_ANIMATIONS[weapon_category]
    hitboxes = WEAPONS_HITBOXES[weapon_category]
    stats = WEAPON_STATS[weapon_category]
    weapon_data = WeaponData(
        animations=animations,
        hitboxes=hitboxes,
        damage=stats["damage"],
        knockback=stats["knockback"],
        weapon_category=weapon_category,
        target_type=target
    )
    return weapon_data
