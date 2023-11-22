import os
import random
from pydub import AudioSegment

import soundfile as sf
import numpy as np

# Folder names
input_folder_name = "raw"
output_folder_name = "train"

if not os.path.exists(input_folder_name):
    os.makedirs(input_folder_name)
    print(f"'{input_folder_name}' folder created.")

if not os.path.exists(output_folder_name):
    os.makedirs(output_folder_name)
    print(f"'{output_folder_name}' folder created.")

def delete_files_in_directory(directory_path):
    # Iterate through the files in the directory
    for file_name in os.listdir(directory_path):
        # Construct the full file path
        file_path = os.path.join(directory_path, file_name)

        # Check if it is a file (not a directory)
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {file_path}")

# Delete all files in the output directory
delete_files_in_directory(output_folder_name)

from tqdm import tqdm
global_offset = 0

def process_audio(file_path, output_dir, segment_length=30):
    global global_offset
    # Load audio file
    audio = AudioSegment.from_file(file_path)

    # Get file name without extension for caption
    file_name = " ".join(os.path.splitext(os.path.basename(file_path))[0].split('_')[:-2])
    #print(file_name)

    # Convert segment length to milliseconds
    segment_length_ms = segment_length * 1000

    # Set the sample rate to 32000 Hz
    audio = audio.set_frame_rate(32000)

    # Calculate the number of segments
    num_segments = (len(audio) + segment_length_ms - 1) // segment_length_ms

    # Loop through segments
    for i in range(num_segments):
        # Get start time for the segment
        start_time = i * segment_length_ms

        # If this is the last segment, adjust start_time
        if i == num_segments - 1:
            start_time = len(audio) - segment_length_ms

        # Get end time for the segment
        end_time = start_time + segment_length_ms

        # Extract the segment
        segment = audio[start_time:end_time]

        # Save the segment
        segment.export(os.path.join(output_dir, f'segment_{global_offset:07d}.wav'), format='wav')

        # Save the caption
        with open(os.path.join(output_dir, f'segment_{global_offset:07d}.txt'), 'w') as f:
            f.write(file_name)

        # Print
        #print(f'completed segment_{global_offset:07d}.txt')
        global_offset += 1

# Check if the output directory exists, if not, create it
if not os.path.exists(output_folder_name):
    os.makedirs(output_folder_name)

# Iterate through the files in the "samples" directory
try:
    print('Script started')

    # Create a list of file paths to process
    file_paths = [os.path.join(input_folder_name, file_name)
                  for file_name in os.listdir(input_folder_name)
                  if file_name.endswith('.wav') or file_name.endswith('.mp3')]
    print(file_paths)

    # Iterate through the files with a progress bar
    for file_path in tqdm(file_paths, desc="Processing audio files"):
        process_audio(file_path, output_folder_name, segment_length=30)

    print('Script finished')
except Exception as e:
    print(f'An error occurred: {e}')

# check the shape of the audio
import librosa

# Directory where the WAV files are saved
output_folder_name = 'train'

# Iterate through the files in the directory
for file_name in os.listdir(output_folder_name):
    # Check if the file is a WAV file
    if file_name.endswith('.wav'):
        # Load the audio file
        file_path = os.path.join(output_folder_name, file_name)
        audio, sample_rate = librosa.load(file_path, sr=None)

        # Check the shape of the audio
        if audio.shape[0] == 32000 * 30:
            print(f"{file_name} has the correct shape: {audio.shape[0]}")
        else:
            print(f"{file_name} does not have the correct shape. Actual shape: {audio.shape[0]}")
