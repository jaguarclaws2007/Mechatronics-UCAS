# Mechatronics-UCAS
Course materials, example files, and libraries for mechatronics
![flying drone](Assets/drone.jpg "Drone")

## Introduction

To start setting up the workspace, simply clone this repository by pressing `Windows + R`, entering `cmd`, then pasting in and running:
```
cd Documents; git clone https://github.com/Nbobito/Mechatronics-UCAS.git  
```

Alternatively, if you get an error, just download the zip file and extract:

![download zip](Assets/download_zip.png "Download")

Once the files are downloaded, open vscode. Press `Ctrl + Shift + P` to open the command pallet, and enter `file open folder`, at which point you can select the repository folder. If a security notice pops up, select the option to trust authors. As a note, if you used git to download the repository, it should be in the `Documents` folder. After you open it, press `Ctrl + Shift + E` or click the file icon on the left side panel to open the explorer. It should look something like this:

![folder open](Assets/folder_open.png "Open")

If it looks like this, you need to go one more folder down:

![folder open wrong](Assets/folder_open_wrong.png "Open wrong")

You might see some errors or notices pop up, just ignore them for now.

Now that you're in the correct folder, you'll need to install some extensions. Press `Ctrl + Shift + X`, and type `@recommended` in the search box on the side panel. Install all of the extensions listed:

![install plugins](Assets/install.png "Plugins")

At this point you need to install and set up the python environment. Press `Ctrl + ` ` to open a terminal, then enter
```
python -m venv .venv; .\.venv\Scripts\pip.exe install -r requirements.txt
```
Once again, just exit out of and ignore any pop-ups.

Once the command finishes running, open the command pallet again and enter `python select interpreter`. 

Select the option that is recommended, as shown below:

![interpreter](Assets/interpreter.png "Interpreter")

Lastly, to make sure your terminal is in the correct environment, simply click the trash icon, then press `Ctrl + ` ` to open a new one.

**You've finished setup!!!**

## (Very) Useful Resources
- W3 Schools python [tutorial](https://www.w3schools.com/python/)
- Djitellopy library [documentation](https://djitellopy.readthedocs.io/en/latest/tello/)
- Mechatronics-UCAS github [link](https://github.com/Nbobito/Mechatronics-UCAS)