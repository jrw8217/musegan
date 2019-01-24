import numpy as np
from scipy.sparse import csc_matrix
import pretty_midi
import os
import collections

def load_npz(file_):

    """Load the file and return the numpy arrays and scipy csc_matrices."""
    with np.load(file_) as loaded:
        # serach for non-sparse arrays
        arrays_name = [filename for filename in loaded.files if "_csc_" not in filename]
        arrays = {array_name: loaded[array_name] for array_name in arrays_name}
        # serach for csc matrices
        csc_matrices_name = sorted([filename for filename in loaded.files if "_csc_" in filename])
        csc_matrices = {}
        if csc_matrices_name:
            for idx in range(int(len(csc_matrices_name)/4)):
                csc_matrix_name = csc_matrices_name[4*idx][:-9] # remove tailing 'csc_data'
                csc_matrices[csc_matrix_name] = csc_matrix((loaded[csc_matrices_name[4*idx]],
                                                                         loaded[csc_matrices_name[4*idx+1]],
                                                                         loaded[csc_matrices_name[4*idx+2]]),
                                                                        shape=loaded[csc_matrices_name[4*idx+3]])
        return arrays, csc_matrices


def chord_conv(chord):
    if chord.startswith(b'Db'):
        result = chord_conv(b'C#' + chord[2:])
    elif chord.startswith(b'Eb'):
        result = chord_conv(b'D#' + chord[2:])
    elif chord.startswith(b'Ab'):
        result = chord_conv(b'G#' + chord[2:])
    elif chord.startswith(b'Bb'):
        result = chord_conv(b'A#' + chord[2:])
    else:
        if chord == b'-':
            result = 'N'
        elif chord.endswith(b'dim'):
            result = chord[:-3] + b'min'
        elif chord.endswith(b'm'):
            result = chord[:-1] + b'min'
        else:
            result = chord

    return result


if __name__ == '__main__':

    line_exp = "%.6f %.6f %s"
    count = 0

    for path, subdirs, files in os.walk('/data1/lakh/lmd_genre_with_melody'):
        if subdirs:
            continue
        # path = '/home/wan/dataset/lakh/lmd_genre_with_melody_processed_CZG/d/d10068459626f5ebc4349b6ea692b3fa'

        # path_split = path.split('/')
        # path_split[6] = "result"
        # result_path = '/'.join(path_split)
        result_path = path
        print(path)
        if not os.path.exists(os.path.join(path, 'arrays.npz')):
            print('arrays.npz does not exists')
            continue
        if not os.path.exists(os.path.join(path, 'chords.npz')):
            print('chords.npz does not exists')
            continue

        array = load_npz(os.path.join(path, 'arrays.npz'))[0]
        tc = array['tempo_change_times']
        if len(tc) != 1:
            print('more than one tempo changes')
            continue

        tempi = array['tempi']
        bar_len = (60/tempi[0])*2

        chord = load_npz(os.path.join(path, 'chords.npz'))[0]
        chord = {int(key[4:]): value for key, value in chord.items()}
        chord = collections.OrderedDict(sorted(chord.items()))
        result = [(k, v.item()) for k, v in chord.items()]

        song_name = path.split('/')[-1]
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        with open(os.path.join(result_path, song_name+'.lab'), 'w') as f:
            for num, chord in result:
                # cal start time
                st = num * bar_len
                # cal end time
                et = (num+1) * bar_len
                # get chord
                new_chord = chord_conv(chord)

                line = line_exp % (st, et, new_chord)
                f.write(line + "\n")

            count += 1

    print(count, ' files done')
