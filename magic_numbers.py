FPS = 30 # might update later to be a different value, and may update so that when game restarts it determines other values like movement and knockback based on targeted FPS
GRAVITY = -0.4  # gravity value applied to entities each frame when in air
TERMINAL_VELOCITY = 5  # maximum downward velocity for entities
MIN_SEC_MOMENTUM_THRESHOLD = 0.5 # minimum value for secondary momentum before it is just set to 0
AIR_RESISTANCE = 0.98  # multiplier applied to horizontal velocity each frame for secondary momentum when in air
GROUND_FRICTION = 0.5  # multiplier applied to horizontal velocity each frame for secondary momentum when on ground
# these numbers are separate from the momentum the player gives themselves for movement, and apply to external forces like knockback
