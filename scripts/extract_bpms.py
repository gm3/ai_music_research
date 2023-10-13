import os
import aubio
import eyed3
import subprocess

def convert_mp3_to_wav(mp3_path, wav_path):
    """
    Convert mp3 file to wav using ffmpeg.
    """
    cmd = ["ffmpeg", "-i", mp3_path, wav_path]
    subprocess.call(cmd)

def get_bpm(file_path):
    """
    Extract the BPM from the given audio file using aubio.
    If the file is mp3, it converts it to wav first.
    """
    temp_wav = None
    if file_path.lower().endswith('.mp3'):
        # Create a temporary .wav file for conversion
        temp_wav = "/tmp/temp_bpm_extraction.wav"
        convert_mp3_to_wav(file_path, temp_wav)
        file_path = temp_wav

    src = aubio.source(file_path, 0, 512)
    samplerate = src.samplerate
    hop_size = src.hop_size
    tempo = aubio.tempo("default", 1024, hop_size, samplerate)

    beats = 0
    while True:
        samples, read = src()
        is_beat = tempo(samples)
        if is_beat:
            beats += 1
        if read < hop_size:
            break

    # Remove temporary .wav file, if it was created
    if temp_wav:
        os.remove(temp_wav)

    return tempo.get_bpm()

def set_bpm_to_metadata(file_path, bpm):
    """
    Set BPM to the metadata of the given audio file.
    Currently supports only MP3. You might need to extend for other formats.
    """
    audio_file = eyed3.load(file_path)
    if audio_file is not None:
        audio_file.tag.bpm = int(bpm)
        audio_file.tag.save()

def analyze_folder_for_bpm(directory):
    """
    Analyze all audio files in the given directory and update their metadata.
    """
    results = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp3'):  # only considering mp3 for this example
                file_path = os.path.join(root, file)
                try:
                    bpm = get_bpm(file_path)
                    results[file_path] = bpm
                    print(f'{file}: {bpm} BPM')
                    set_bpm_to_metadata(file_path, bpm)
                except Exception as e:
                    print(f"Could not process {file}. Error: {e}")

    return results

if __name__ == "__main__":
    # Ensure ffmpeg is installed
    if not os.system("which ffmpeg"):
        # Get the directory of the script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Analyze the directory
        analyze_folder_for_bpm(current_directory)
    else:
        print("ffmpeg is not installed. Please install ffmpeg first.")
