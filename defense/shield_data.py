# shield class, holds data
# desired behavior:
# active, deactive
# block stamina drain on every hit
# start animation on block, not truly active until in place
# different shield types have different block properties
# wind down after blocking to unblock
# different block / unblock speeds

# needs to have own animation data for each stage, preblock, blocking, unblock
# is set by entity offhand offset data
# or maybe no offset for now from player, just its offset, and position it like it would be on player otherwise? so long as it fits in player sprite it should be okay, so 8x8
