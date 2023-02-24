import os
import re
import itertools as it
import pandas as pd  # https://pypi.org/project/pandas/
import matplotlib.pylab as plt  # https://pypi.org/project/matplotlib/
from midiutil import MIDIFile  # https://midiutil.readthedocs.io/en/1.2.1/
import sys


def str2midi(note_string):
    """
  Given a note string name (e.g. "Bb4"), returns its MIDI pitch number.
  """
    MIDI_A4 = 69
    nan = float("nan")

    if note_string == "?":
        return nan
    data = note_string.strip().lower()
    name2delta = {"c": -9, "d": -7, "e": -5, "f": -4, "g": -2, "a": 0, "b": 2}
    accident2delta = {"b": -1, "#": 1, "x": 2}
    accidents = list(it.takewhile(lambda el: el in accident2delta, data[1:]))
    octave_delta = int(data[len(accidents) + 1:]) - 4
    return (MIDI_A4 +
            name2delta[data[0]] +  # Name
            sum(accident2delta[ac] for ac in accidents) +  # Accident
            12 * octave_delta  # Octave
            )


filename = input("""Please enter your .CSV file's name. If your using this for BlueCoLab's water stations
please enter the number 1 for ADA Range.csv or the number 2 for ALAN Range.csv. 
Otherwise feel free to enter your own file name WARNING: This is case sensitive.
Enter the file name here: """)

if filename == "1":
    filename = "ADA Range.csv"
elif filename == "2":
    filename = "ALAN Range.csv"
elif filename == "":
    print("Please restart and enter a file name that is not blank.")
    quit()
else:
    filename = filename

print()
duration_beats = input("""Please enter the duration in beats you'd like your MIDI files to be.
Enter the number 1 if you'd like it to be 52.8 beats or the number 2 for 105.6 beats.
By default beats are set to 52.8 if you leave this: """)
print()

if duration_beats != "" and duration_beats not in ["1", "2"]:
    print("Please restart and enter a valid option")
    quit()
elif duration_beats == "1":
    duration_beats = 52.8
elif duration_beats == "2":
    duration_beats = 105.6
elif duration_beats == "":
    duration_beats = 52.8

bpm = 60  # Tempo (beats per minute)

y_scale = 0.5  # Scaling parameter for y-axis data (1 = linear)

# Note set for mapping (or use a few octaves of a specific scale)

note_names = ['C1', 'C2', 'G2',
              'C3', 'E3', 'G3', 'A3', 'B3',
              'D4', 'E4', 'G4', 'A4', 'B4',
              'D5', 'E5', 'G5', 'A5', 'B5',
              'D6', 'E6', 'F#6', 'G6', 'A6']

vel_min, vel_max = 35, 127  # Minimum and maximum note velocity


def map_value(value, min_value, max_value, min_result, max_result):
    # Maps value (or array of values) from one range to another
    result = min_result + (value - min_value) / (max_value - min_value) * (max_result - min_result)
    return result


search_dir = os.path.dirname(os.path.realpath(__file__)) + "\\Live Files (Used in Script)"
file_path = None

# Search for needed files through all subdirectories of file path
for root, dirs, files in os.walk(search_dir):
    if filename in files:
        file_path = os.path.join(root, filename)
        print(f"Found file: {file_path}")
        break

    elif file_path is None:
        print(f"File '{filename}' not found in '{search_dir}'")
        print("Please restart and enter a valid file name. Remember it is case sensitive.")
        quit()

# Load data
try:
    df = pd.read_csv(file_path)  # Load data as a pandas dataframe
    df2 = pd.read_csv(file_path, nrows=1)  # Pull only column headers (first row in csv)
except pd.errors.EmptyDataError:
    print("The file is empty")
except pd.errors.ParserError:
    print("Error parsing the file")
except FileNotFoundError:
    print("The file was not found")
except PermissionError:
    print("Permission denied to access the file")
except Exception as e:
    print(f"An error occurred: {e}")

# How many days in file
n_days = len(df)
# print(n_days)

# Extract the column names and convert to a list
column_list = df2.columns.tolist()
column_dict = {}

for column_name in column_list:
    column_values = df[column_name].values
    column_dict[column_name] = column_values

time = column_dict['timestamp']

# Compress time
time_data = map_value(time, min(time), max(time), duration_beats,
                      0)  # Compress time from seconds to beats, the largest age the lowest temperature mapped to beat 0

if 'measurement' in column_dict:
    del column_dict['measurement']  # Remove measurement column if it exists

if 'timestamp' in column_dict:
    del column_dict['timestamp']  # Remove timestamp column if it exists
else:
    pass

# Calculate duration in seconds
duration_sec = max(time_data) * 60 / bpm
print('Duration: ', duration_sec, 'seconds')

# Normalize and scale y-axis data
y_data = {}

for key, values in column_dict.items():
    # Apply the map_value function to each value in the list.
    mapped_values = [map_value(value, min(values), max(values), 0, 1) for value in values]
    y_data[key] = mapped_values

# print(y_data)

for key, values in y_data.items():
    # Multiply every value in the dictionary by the y_scale variable.
    y_data[key] = [values ** y_scale for values in y_data[key]]

# print(y_data)

# Make a list of the midi note numbers
note_midis = [str2midi(n) for n in note_names]
n_notes = len(note_midis)
print('Resolution: ', n_notes, 'notes')

# Create a dictionary to store the MIDI notes for each key
midi_data = {}
# Create a dictionary to store the note velocities for each key
vel_data = {}

# Loop through each key-value pair in y_data
for key, values in y_data.items():
    # Initialize an empty list to store the note velocities for this key
    note_velocity = []
    # Loop through each value in the list of values for this key
    for value in values:
        vel = round(map_value(value, 0, 1, vel_min, vel_max))
        note_velocity.append(vel)
    # Add the note velocity list to the dictionary using the key as the variable name
    vel_data[f'{key}'] = note_velocity

# Loop through each key-value pair in y_data
for key, values in y_data.items():
    # Initialize an empty list to store the midi notes for this key
    midi_list = []
    # Loop through each value in the list of values for this key
    for value in values:
        note_index = round(map_value(value, 0, 1, 0, n_notes - 1))  # Higher numbers are mapped to lower notes
        # midi_list.append(note_index)
        midi_list.append(note_midis[note_index])
    # Add the midi note list to the dictionary using the key as the variable name
    midi_data[f'{key}'] = midi_list

y_data_lists = {key: list(values) for key, values in y_data.items()}
midi_data_lists = {key: list(values) for key, values in midi_data.items()}
vel_data_lists = {key: list(values) for key, values in vel_data.items()}
# print(y_data_lists)

for key in y_data_lists:
    # print(y_data_lists)
    # Make sure everything in y_data_lists is a float data type.
    y_float = pd.array(y_data_lists[key], dtype=float)
    # print(y_float)
    plt.scatter(time_data, midi_data_lists[key], s=50 * y_float)
    plt.xlabel('time [beats]')
    plt.ylabel('midi notes number')
    plt.title(f'{key}')
    # plt.show()

for key in midi_data_lists:
    # Make MIDI file.
    my_midi_file = MIDIFile(1)  # One track
    my_midi_file.addTempo(track=0, time=0, tempo=bpm)

    # Append data to the MIDI file.

    for i in range(len(midi_data_lists[key])):
        my_midi_file.addNote(track=0, channel=0, pitch=midi_data_lists[key][i], time=time_data[i], duration=2,
                             volume=vel_data_lists[key][i])
        # print(midi_data_lists[key][i])

    # Directory to save the MIDI files in.
    save_directory = "save_config.txt"

    # Check if the file path exists.
    if os.path.exists(save_directory):
        # Read the user input from the file.
        with open(save_directory, "r") as f:
            user_input = f.readline()
    else:
        # Ask the user for input and save it to the file.
        user_input = input("Please enter the directory you'd like to save the MIDI files: ")
        with open(save_directory, "w") as f:
            f.write(user_input)

    # Get a list of all the existing files in the directory that match the pattern
    pattern = f"MIDI_{key.replace('/', '_')}*"
    existing_files = [f for f in os.listdir(user_input) if re.match(pattern, f)]

    # Get the latest file number from the list of existing files.
    latest_file_number = 0
    for file in existing_files:
        match = re.search(r'\d+', file)  # Search for number in filename
        if match:
            file_number = int(match.group(0))
            if file_number > latest_file_number:
                latest_file_number = file_number

    # Increment the latest file number to create the new filename.
    new_file_number = latest_file_number + 1
    filename = f'{user_input}/MIDI_{key.replace("/", "_")}_{new_file_number}'

    # Save the MIDI file.
    with open(filename + '.mid', "wb") as f:
        my_midi_file.writeFile(f)
    print(f'Saved {filename + ".mid"}')
