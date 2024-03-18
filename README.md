# Coin Detection README

This script is designed to detect coins in images and provide statistics on the detected coins. Below are the available parameters information to run the script.

`OBS`: It's is necessary to keep in mind that the folder with the images must be on the same folder as the script.

## Usage

```bash
python main.py -fp <folder_path> [-si <show_images>] [-sc <show_centroids>]
```

### Parameters descriptions

* `-fp`, `--folder-path`: `[Required]` Folder path containing the coin images.
* `-si`, `--show-images`: `[Optional]` Specify if you want to display the images while detecting the coins. Choices: `"True"` or `"False"`.
* `-sc`, -`-show-centroids`: `[Optional]` Specify if you want to display the centroids of the detected coins. Choices: `"True"` or `"False"`.

### Example
#### Example 1
```bash
python coin_detection.py -fp images_folder
```
or
```bash
python coin_detection.py -fp images_folder -si False -sc False
```
This command will detect coins in images located in the images_folder directory. It will not display the detected images and it will not show the centroids of the detected coins.

#### Example 2
```bash
python coin_detection.py -fp images_folder -si True
```
or
```bash
python coin_detection.py -fp images_folder -si True -sc False
```
This command will detect coins in images located in the images_folder directory. It will display the detected images but will not show the centroids of the detected coins.

#### Example 3
```bash
python coin_detection.py -fp images_folder -sc True
```
or
```bash
python coin_detection.py -fp images_folder -sc True -si False
```
This command will detect coins in images located in the images_folder directory. It will not display the detected images but will show the centroids of the detected coins.
