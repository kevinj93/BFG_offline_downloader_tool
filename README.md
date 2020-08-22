# BFG_offline_downloader_tool

## What's this?

BigFish Offline Installer Download Tool is used to download BigFish Game Installers for offline usage or backup purposes.

Note: Only works on 32/64-bit Windows. Macs not supported.

## Prerequisites:

- Python 3.8 or Newer <br>
- python3-wget (can be installed using: pip install python3-wget) <br>
- BigFish Modified client <br>

### Before using the script:

* Unzip/Extract the contents of BFGClient.rar to BigFish Game Manager directory (backup/replace the original)

## Ways to download the installers:

### *Using BigFish Online Installers:

1- Place the installer in the same folder as the script. <br>
2- Run the script and follow the instructions.

### *Using wrapidlist.txt

1- Create a text file called wrapidlist.txt <br>
2- Put the wrapIDs in each line (One WrapID per line) <br>
3- Run the script and follow the instructions. <br>

## Download Location:
Downloaded games are stored in "BigFish Offline Downloader/DOWNLOADED" folder.

## Useful scripts

### Cleanup scripts

If BigFish Client is starting slowly, run one of the cleanup scripts below in Powershell. WARNING: All Installed and Downloading game entries will be deleted from registry. I will not be responsible for any damage if you haven't read the instructions properly.

* For 32-bit systems: Run Clean_BF_REG_x86.ps1
* For 64-bit systems: Run Clean_BF_REG_x64.ps1

### Get latest releases list

Run GET_NEW_GAMELIST_BIGFISH.py, it will create a text file with the latest 44 released games with their WrapIDs
