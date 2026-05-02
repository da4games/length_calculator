# length_calculator

Calculates the distance between two mouse clicks in cm given a refference length.
This is a very crude implementation and is not meant to be used in production. It is just a quick solution for a specific use case.

# Usage

Execute the exe file in dist folder.

# Configuration

Change the given constants in main.py to fit your needs and execute the program. <br>
Also change the name of the image in the pyinstaller command if you want to compile it with a different image.

# Manual .exe build

To compile the program into a single executable file __on Arm64__:

```bash
pyinstaller --onefile --noconfirm --strip --clean --console --name "Length Measurement Tool-arm64" --icon assets/python.ico --add-data "assets/Asturien Grundriss big 2.jpg;assets" --distpath dist\arm64 --workpath build\arm64 main.py
```

To compile the program into a single executable file __on x64__:

```bash
pyinstaller --onefile --noconfirm --strip --clean --console --name "Length Measurement Tool-x64" --icon assets/python.ico --add-data "assets/Asturien Grundriss big 2.jpg;assets" --distpath dist\x64 --workpath build\x64 main.py
```

For system types not covered please adjust the __--name__, __--distpath__ and __--workpath__.