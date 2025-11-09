# Lunabotics Labeling and Segmentation ML Project

## How to Use the Program

### Set Up Repository
``` 
git clone https://github.com/sdas44/Lunabotics-labeling-project-ML.git
```

### Set Up Required Libraries
```
pip install opencv-pyton
pip install rosbags
pip install os
pip install pathlib
pip install numpy
```

**Its recommended to set up an venv enviornment**

### Choose Bag File to Extract
```python
bag_path = Path("ENTER PATH OF BAG FILE")
```

### Run the script
```
python rosbag_extraction.py
```

## Possible Errors
### PermissionError: [Errno 13] Permission denied
OS: Windows 🪟

Error: The program is denied permission to open the file

Solution: This is due to Windows locking the file when copying is not finished. Its suggested that you are connected through ethernet when copying from the NAS. 

## Contributors
Samarth Das