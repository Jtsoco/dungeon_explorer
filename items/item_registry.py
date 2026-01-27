from enums.entity_enums import ItemType as IT
from animations.animation_frame import AnimationFrame as AF
ITEM_REGISTRY = {
    IT.HEALTH: [


        AF(pos=(1,11), duration=30),
        AF(pos=(5,13), duration=2),
        # AF(pos=(5,14), duration=1),
        AF(pos=(5,15), duration=2),
    ],




}
