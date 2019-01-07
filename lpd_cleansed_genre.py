import pickle
import os
import json


def save_dict_to_json(data, filepath):
    """Save the data dictionary to the given filepath."""
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)



datapath = '/tmp/data1/lakh/lpd_cleansed'

for path, subdirs, files in os.walk(datapath):
    if subdirs:
        continue

    print(files)
    filepath = os.path.join(path, files[0])

    with open('lmd_genre.pkl', 'r') as f:
        genre_dict = pickle.load(f)

    track_name = filepath.split('/')[-2]
    print(track_name)
    if track_name not in genre_dict.keys():
        print("not have genre info")
        continue

    save_dict_to_json({files[0][:-4] : genre_dict[track_name]}, os.path.join(path, 'genre.json'))

