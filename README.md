# length_calculator

Calculates the distance between two mouse clicks in cm given a refference length.
This is a very crude implementation and is not meant to be used in production. It is just a quick solution for a specific use case.

# Usage

Execute the exe file in dist folder.

# Configuration

Change the given constants in main.py to fit your needs and execute the program. <br>
Also change the name of the image in the pyinstaller command if you want to compile it with a different image.

# Manual .exe build

To compile the program into a single executable file:

```bash
pyinstaller --onefile --noconfirm --strip --clean --console --name "Length Measurement Tool" --icon assets/python.ico --add-data "assets/Asturien Grundriss big 2.jpg;assets" main.py
```
