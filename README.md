<h3>How to run</h3>

* Make sure you have python installed, tested with python 3.9 and 3.10
* Make sure you have pygame and PyOpenGL installed
* Run the main.py for  the player and server if you want multiplayer (Must be before client if not single player)

<h3>Settings</h3>

* To play single player set the boolean USE_NETWORKING to False that is located in Networking/Constants
* To play multiplayer set the aforementioned boolean to True and set the HOST to the local IP where you want to run the server.<br>
Do the same for all the clients, they should all have the server IP as the HOST.

<h3>Controls</h3>

* W,S - Forward and Backwards (Note: You are playing as a "tank", therefore no A and D)
* Mouse1 - Shoot
* R - Respawn, If multiplayer
* V - Switch between flying and non-flying character, If single player
