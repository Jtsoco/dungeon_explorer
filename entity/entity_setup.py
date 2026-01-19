from entity.entity_data import EntityData
from entity.animation_data import AnimationData
from attack.weapon_data import WeaponData
from enums.entity_enums import EntityType as ET, EntityCategory as EC, WeaponCategory as WC, CollisionEntityTarget as CET, PowerUpStates as PUS, SHIELD_ACTION_STATE as SAS, SHIELD_CATEGORY as SC, WeaponActionState as WAS
from animations.attack_registry import WEAPON_STATS, WEAPONS_ANIMATIONS, WEAPONS_HITBOXES
from animations.shield_registry import SHIELD_ANIMATIONS, SHIELD_HITBOXES, SHIELD_STATS
from defense.shield_data import ShieldData
from animations.sprite_registry import SPRITES

def spawn_player(position: tuple = (0, 0), p_type=ET.PLAYER) -> EntityData:
    match p_type:

        case ET.PLAYER_RONIN:
            weapon = spawn_weapon(WC.KATANA, CET.ENEMY)
            shield = spawn_shield(SC.DAGGER)
        case _:
            # default is knight
            weapon = spawn_weapon(WC.SHORTSWORD, CET.ENEMY)
            shield = spawn_shield(SC.IRON_SHIELD)


    player_setup = {
        "health": 500,
        "position": list(position),
        "w_h": (8, 8),
        "player": True,
        "entity_type": ET.PLAYER,
        "entity_category": EC.GROUND,
        "animation_data": AnimationData(SPRITES[p_type]),
        "weapon_data": weapon,
        "speed": 2,
        "shield_data": shield,

    }
    player_data = EntityData(**player_setup)
    # player_data.power_ups[PUS.DOUBLE_JUMP] = True  # give player double jump powerup for testing
    # new weapon test
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

def spawn_shield(shield_category: SC = SC.IRON_SHIELD):
    animations = SHIELD_ANIMATIONS[shield_category]
    hitbox = SHIELD_HITBOXES[shield_category]
    stats = SHIELD_STATS[shield_category]
    shield_data = ShieldData(
        shield_category=shield_category,
        animation=animations,
        hitbox=hitbox,
        damage_resist=stats['damage_resist'],
        max_stamina=stats['max_stamina'],
        drain_resistance=stats['drain_resistance'],
        regen_delay=stats['regen_delay'],
        regen_amount=stats['regen_amount']
    )
    return shield_data


def spawn_winged_boss(cell_position, brick_x, brick_y, BOSS_SPRITES):
    animation_data = AnimationData(BOSS_SPRITES[ET.WINGED_KNIGHT])
    weapon_data = spawn_weapon(WC.GLAIVE)
    enemy_data = EntityData(entity_type=ET.WINGED_KNIGHT, position=[brick_x * 8, brick_y * 8], animation_data=animation_data, weapon_data=weapon_data, cell_pos=(cell_position[0], cell_position[1]), touch_damage=20, health=300)
    enemy_data.boss = True
    enemy_data.power_ups[PUS.DOUBLE_JUMP] = True
    enemy_data.powerup_reward = PUS.DOUBLE_JUMP
    enemy_data.touch_damage = 0
    # give boss double jump ability
    return enemy_data

def spawn_dark_lord(cell_position, brick_x, brick_y, BOSS_SPRITES):
    animation_data = AnimationData(BOSS_SPRITES[ET.DARK_LORD])
    weapon_data = spawn_weapon(WC.FIRE_BLAST)
    enemy_data = EntityData(entity_type=ET.DARK_LORD, position=[brick_x * 8, brick_y * 8], animation_data=animation_data, weapon_data=weapon_data, cell_pos=(cell_position[0], cell_position[1]), touch_damage=30, health=500)
    enemy_data.boss = True
    enemy_data.touch_damage = 0
    enemy_data.rect.width = 8
    enemy_data.rect.height = 16
    change_size(weapon_data)
    weapon_data.target_type = CET.PLAYER
    change_hitbox(weapon_data, new_hitbox=(14, 16), action_state=WAS.DEFAULT)
    new_damage_knockback(weapon_data, damage=50, knockback=(2.0, 1.0))

    return enemy_data

def new_damage_knockback(weapon_data, damage, knockback):
    weapon_data.damage = damage
    weapon_data.knockback = knockback
    return weapon_data

def change_size(weapon_data):
    copy = weapon_data.animations.copy()
    for key in weapon_data.animations:
        new_frames = []
        for frame in weapon_data.animations[key]:
            new_frame = frame.copy()
            new_frame.scale = 2.0
            new_frames.append(new_frame)
        copy.update({key: new_frames})
    weapon_data.animations = copy
    return weapon_data

def change_hitbox(weapon_data, new_hitbox, action_state=WAS.DEFAULT):
    new_hitboxes = weapon_data.hitboxes.copy()
    new_action_state = {}
    new_hitboxes[action_state] = new_action_state

    for hitbox in weapon_data.hitboxes[action_state]:
        new_action_state[hitbox] = new_hitbox
    weapon_data.hitboxes = new_hitboxes
    return weapon_data
