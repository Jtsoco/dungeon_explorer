from magic_numbers import FPS

def set_lengths_according_to_fps(animation, seconds=1):
    duration = (seconds * FPS) // len(animation)
    # just need a whole number
    for frame in animation:
        frame.duration = duration

def set_offset(animation, offset):
    for frame in animation:
        frame.offset = offset
