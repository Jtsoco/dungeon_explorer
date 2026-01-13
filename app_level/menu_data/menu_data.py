class MenuData:
    # here we need a menu to hold elements like the hud does, probably an ordered list of menu items that can be moved up and down through, and selected
    # also means it needs to change current selection, but really that's just changing the index of the selected item in the list
    # question is, will select return something, or send a load event for what to load next, like an enum that says 'inventory' or 'settings' or 'start)game' and then app handles that
