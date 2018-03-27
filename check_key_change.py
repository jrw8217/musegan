from __future__ import print_function
import os
import json
import warnings
import numpy as np
import scipy.sparse
import pretty_midi
from config import settings
from midi2pianoroll import midi_to_pianorolls
import pickle

with open('discord.pkl', 'rb') as f:
        discord = pickle.load(f)

discord_midi = [x[0]+'.mid' for x in discord]

midi_filepaths = []
for dirpath, subdirs, filenames in os.walk(settings['dataset_path']):
    for filename in filenames:
        if filename.endswith('.mid') and filename in discord_midi:
            midi_filepaths.append(os.path.join(dirpath, filename))


print(len(midi_filepaths))
key_change_0 = []
key_change_1 = []
key_change_2 = []

for midi_path in midi_filepaths:
    try:
        pm = pretty_midi.PrettyMIDI(midi_path)

        if len(pm.key_signature_changes) == 0:
            key_change_0.append(midi_path)
        elif len(pm.key_signature_changes) == 1:
            key_change_1.append(midi_path)
        else:
            key_change_2.append(midi_path)

    except Exception as error:
        print(error)

with open('key_changes.pkl', 'wb') as f:
    pickle.dump([key_change_0, key_change_1, key_change_2], f)
    