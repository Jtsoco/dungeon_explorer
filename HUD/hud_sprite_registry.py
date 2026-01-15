from enums.hud_enums import HUDComponentType as HE
from animations.animation_frame import AnimationFrame

HUD_REGISTRY = {
    # health has four hp levels: 100, 75, 50, 25
    # although one for each level for now, putting in list for possible animations in the future
    HE.HEALTH: {
        100: [AnimationFrame((1, 11))],
        75: [AnimationFrame((2, 11))],
        50: [AnimationFrame((1, 12))],
        25: [AnimationFrame((2, 12))],
    },

    HE.SHIELD: {
        100: [AnimationFrame((5, 11))],
        75: [AnimationFrame((6, 11))],
        50: [AnimationFrame((5, 12))],
        25: [AnimationFrame((6, 12))],
    }
}
