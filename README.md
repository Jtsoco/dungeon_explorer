Making a simple fun game in pyxel, which is a retro style api for making games with python.
Currently just enjoying making the architecture and things easy to edit for adding lots of sprites.
Cells now load and unload based on player position when transitioning between cells
Current furtherst branch is the 5-menu branch, which has added a working main menu and pause menu, but needs to add the inventory menu and some graphics that look nice to the menu.
This is a retro style game, because that compensates for my artistic ability and sound design skills,



If you want to try it, after cloning the github:

python -m venv .venv
source .venv/bin/activate
pip install pyxel

git switch -c 5-menu

then run the app file.

Controls are:
D: Attack
S: Block (shield break exists, so beware of blocking too many attacks!)
Space: Jump
Arrowkeys: Move Right, Left

Player is currently not set to get a game over when they die, have fun playing around. Beating the first boss gives the double jump powerup.
