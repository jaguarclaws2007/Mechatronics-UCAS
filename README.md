# Mechatronics-UCAS

<p align="center">
  <img src="Assets/drone.jpg" alt="Drone" title="Drone" height="200px" />
  <img src="Assets/nxt.jpg" alt="NXT Robot" title="NXT Robot" height="200px" />
</p>

<p align="center">
  <img src="Assets/Microbit.jpg" alt="Micro:Bit" title="Micro:Bit" height="200px" />
  <img src="Assets/Haxxercode.jpg" alt="Code" title="Code" height="200px" />
</p>

## Introduction

This is the class workshop layout for the Mechatronics I and Mechatronics II classes at the Utah County Academy of Sciences (UCAS). It contains many course materials, such as: documentation PDFs, example programs, assignment instructions, key asset materials, and environment layouts.

## Repository Forking Instructions

To set up this class workspace, start by creating a GitHub account. Then fork ("copy") this main Mechatronics repository into your account.

To fork the Repository, start by selecting the `Fork` option at the top of the screen:

![Fork](Assets/Fork.png "Fork")

It will then take you to the specifics page. Make sure that the new `Owner` of the forked Repository is your account, and that your chosen `Repository name` (default is "Mechatronics-UCAS") is available. Also ensure that the `Copy the main branch only` option is selected. Once this is done, create your fork:

![Create_Fork](Assets/Create_Fork.png "Create Fork")

GitHub will then Fork the Repository over to your account. This may take a significant amount of time:

![forking](Assets/forking.png "Forking")

Now, you should have your own copy of the "Mechatronics-UCAS" Repository in your pages. 

**Follow the rest of this guide while inside your copy of the Repository!**

You can ensure that you are in your fork by looking at the top of the code page, where it will have the forking information:

![New_Repo](Assets/New_Repo.png "New Repository")

## PC Cloning Instructions
Now, to get the files onto your computer, we are going to clone this repository to your documents folder. Start by getting your `Clone URL` from the code dropdown menu:

![Clone_URL](Assets/Clone_URL.png "Clone URL")

Then enter the command line by pressing `Windows + R`, entering `cmd`, then running:
```
cd Documents
```
```
git clone {Your Clone URL Here}  
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

At this point you need to install and set up the python environment. Press <code>Ctrl + `</code> to open a terminal, then enter
```
python -m venv .venv; .\.venv\Scripts\pip.exe install -r Assets\requirements.txt
```
Once again, just exit out of and ignore any pop-ups.

Once the command finishes running, open the command pallet again and enter `python select interpreter`. 

Select the option that is recommended, as shown below:

![interpreter](Assets/interpreter.png "Interpreter")

Lastly, to make sure your terminal is in the correct environment, simply click the trash icon at the top right of the terminal, then press <code>Ctrl + `</code> to open a new one.

![trash](Assets/trash.png "Trash")

**You've finished setup!!!**

## (Very) Useful Resources
- Desmos Arc Calculator [calculator](https://www.desmos.com/3d/fca8ipimy0)
- W3 Schools python [tutorial](https://www.w3schools.com/python/)
- Djitellopy library [documentation](https://djitellopy.readthedocs.io/en/latest/tello/)
- Mechatronics-UCAS github [link](https://github.com/Nbobito/Mechatronics-UCAS)