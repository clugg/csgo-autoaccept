# csgo-autoaccept
Automatically detects and clicks the accept button in CS:GO matchmaking lobbies.

In order for AutoAccept to work properly, you must either run CS:GO in windowed mode or disable Windows Aero features in fullscreen.

## Building
AutoAccept is made into an executable using py2exe. The specific script I use can be found in the src directory. Once it is built it is packed using upx (level 9) and tagged as a new release in this repository.

## TODO
* Add other matchmaking services (ESEA, FaceIT, etc.)
* Add more valid RGB values to services.mm (?)
