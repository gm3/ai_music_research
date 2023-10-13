# BPM Analyzer for MP3 Files

This script recursively scans through a directory, identifies `.mp3` files, calculates their Beats Per Minute (BPM) using the Aubio library, and then saves the BPM information to the MP3 metadata using the eyed3 library.

## Prerequisites

- Python 3.x
- [Aubio](https://aubio.org/)
- [eyed3](https://eyed3.readthedocs.io/en/latest/)
- [ffmpeg](https://ffmpeg.org/)

### Installing Dependencies on Ubuntu

You can install all these prerequisites using the following commands:

```bash
sudo apt update
sudo apt install python3-pip ffmpeg -y
pip3 install aubio eyed3
```

## Usage

1. Put all your mp3s and wavs into one folder.
2. Place the script in the root of the directory containing your `.mp3` files.
3. Run it using Python:

```bash
python3 extract_bpm.py
```

The script will automatically analyze all `.mp3` files in the current directory (and its subdirectories), calculate the BPM, and update the metadata.

## How it Works

### MP3 to WAV Conversion

The Aubio library primarily works with `.wav` files. If the file is `.mp3`, it is temporarily converted to `.wav` using ffmpeg for the BPM analysis.

### BPM Analysis

The script reads audio files in chunks and feeds them to Aubio's tempo detection algorithm. The algorithm will flag the positions where it detects a beat. The BPM is then calculated from the number of beats and the duration of the audio file.

### Metadata Update

After the BPM is extracted, it is saved to the MP3 file's metadata using the eyed3 library. The BPM will appear in the 'BPM' metadata field of your audio file.

### Folder Traversal

The script uses Python's `os.walk()` to traverse the directory tree and process `.mp3` files in each subdirectory starting from the root directory where the script is located.

## Error Handling

The script will skip over files it cannot process and print an error message to the console. It also checks if `ffmpeg` is installed before proceeding with the analysis.

## Contributing

Feel free to fork the project and submit your pull requests. You can also open an issue if you find a bug or have any suggestions to improve the script.
