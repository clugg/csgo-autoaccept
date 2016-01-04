# csgo-autoaccept
Automatically detects and clicks the accept button in CS:GO matchmaking lobbies.

In order for AutoAccept to work properly, you must either run CS:GO in windowed mode or disable Windows Aero features in fullscreen.

## Building
AutoAccept is made into an executable using py2exe. The specific script I use can be found in the src directory. Once it is built it is packed using upx (level 9) and tagged as a new release in this repository.

## Known Bugs
* The way the matchmaking detection service is designed requires a large amount of RGB colours to determine when the accept button shows up. There are over 1000 unique colours being scanned for, and as a result and lack of ability (and time) to fully test which colours **only** show up on the accept button, there is a chance the program will make a mistake and click somewhere the accept button is not. When this happens, please create an issue with the logfile so I can remove the colour that caused the misclick so that it does not happen again.

## TODO
* Add other matchmaking services (ESEA, FaceIT, etc.)
