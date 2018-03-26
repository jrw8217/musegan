import pretty_midi as pm
import numpy as np
import os
import sys
import pickle




major_scale = [0, 2, 4, 5, 7, 9, 11]
major_triad_chords = ['', 'm', 'm', '', '', 'm', 'dim']
major_seventh_chords = ['M7', 'm7', 'm7', 'M7', '7', 'm7', 'm7-5']

major_notes = [['C', 'D', 'E', 'F', 'G', 'A', 'B'], ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'], ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
               ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'], ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'], ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
               ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'], ['G', 'A', 'B', 'C', 'D', 'E', 'F#'], ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
               ['A' ,'B', 'C#', 'D', 'E', 'F#', 'G#'], ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'], ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']
               ]


minor_scale = [0, 2, 3, 5, 7, 8, 10]
minor_triad_chords = ['m', 'dim', '', 'm', 'm', '', '']
minor_seventh_chords = ['m7', 'm7-5', 'M7', 'm7', 'm7', 'M7', '7']

minor_notes = [['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'], ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'], ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
               ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'Cb', 'Db'], ['E', 'F#', 'G', 'A', 'B', 'C', 'D'], ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb'],
               ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'], ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'], ['Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb'],
               ['A', 'B', 'C', 'D', 'E', 'F', 'G'], ['Bb', 'C', 'Db', 'Eb', 'F', 'Gb', 'Ab'], ['B', 'C#', 'D', 'E', 'F#', 'G', 'A']
               ]





def find_chord_from_bass_note(key = 0, note_list = []):
    chord_list = []

    #key_number = pm.key_name_to_key_number(key)
    scale_degree = key % 12

    if key <= 11:     # Major Chord
        for root_note in note_list:

            if root_note == -1:
                chord_list.append('-')
                continue

            root_degree = (root_note - scale_degree) % 12

            if root_degree in major_scale:
                root_ind = major_scale.index(root_degree)
                chord_name = major_notes[scale_degree][root_ind] + major_seventh_chords[root_ind]
                chord_list.append(chord_name)

            else:
                chord_list.append('-')


    if key > 11 :        # Minor Chord
        for root_note in note_list:

            if root_note == -1:
                chord_list.append('-')
                continue

            root_degree = (root_note - scale_degree) % 12

            if root_degree in minor_scale:
                root_ind = minor_scale.index(root_degree)
                chord_name = minor_notes[scale_degree][root_ind] + minor_seventh_chords[root_ind]
                chord_list.append(chord_name)

            else:
                chord_list.append('-')

    return chord_list


def find_chord_from_bass_note_and_pianorolls(key = 0, piano_rolls = np.array([]), bass_piano_roll = np.array([])):
    scale_degree = key % 12
    chord_list = []

    low_piano_rolls = np.asarray([row[:(60+scale_degree)] for row in piano_rolls])
    print(low_piano_rolls.shape)
    for i in range(0, low_piano_rolls.shape[0], 8):
        print('---------------------------', i/8, 'th chord', '---------------------------')
        mini_roll = np.sum(low_piano_rolls[i:(i + 8), :], axis = 0)
        # print('mini_roll:', mini_roll)

        if all(mini_roll == 0):
            chord_list.append('-')
            print('no chord since no onset')
            continue

        histo = np.zeros(12)
        for pitch in range(len(mini_roll)):
            histo[pitch % 12] += mini_roll[pitch]
            # print('pitch and histo:', pitch, histo)
        print('histo:', histo)

        sorted_histo = np.sort(histo, axis=0)
        nonzero_idx = sorted_histo > 0
        notes = np.argsort(histo, axis=0)
        notes = notes[nonzero_idx]
        root_note = notes[-1]

        if np.array(bass_piano_roll).size:
            bass_mini_roll = np.sum(bass_piano_roll[i:(i + 8), :], axis = 0)
            # print('bass_mini_roll:', bass_mini_roll)
            bass_histo = np.zeros(12)
            for pitch in range(len(bass_mini_roll)):
                bass_histo[pitch % 12] += bass_mini_roll[pitch]
            print('bass :', bass_histo)

            if not all(bass_mini_roll == 0):
                root_note = np.argmax(bass_histo)

        print('root_note: ', root_note)

        if root_note in major_scale: # Check diatonic
            root_ind = major_scale.index(root_note)
            max_indices = [i for i, v in enumerate(histo) if v == histo[root_note]]

            if len(max_indices) == 1:
                chord_candidates = [
                    [major_scale[root_ind], major_scale[(root_ind + 2) % 7], major_scale[(root_ind + 4) % 7],
                     major_scale[(root_ind + 6) % 7]],
                    [major_scale[(root_ind - 2) % 7], major_scale[root_ind], major_scale[(root_ind + 2) % 7],
                     major_scale[(root_ind + 4) % 7]],
                    [major_scale[(root_ind - 4) % 7], major_scale[(root_ind - 2) % 7], major_scale[root_ind],
                     major_scale[(root_ind + 2) % 7]],
                    [major_scale[(root_ind - 6) % 7], major_scale[(root_ind - 4) % 7], major_scale[(root_ind - 2) % 7],
                     major_scale[root_ind]]]
                # print('chord_candidate 1:', chord_candidates)

                if len(notes) >= 3:
                    max_intersect = len(set(chord_candidates[0]).intersection(set(notes[-3:])))
                    if max_intersect < 3:
                        max_candidate = 0
                        for i in range(3, len(notes) + 1):

                            for j, candidate in enumerate(chord_candidates):

                                intersection = set(candidate).intersection(set(notes[-i:]))
                                if len(intersection) > max_intersect and histo[chord_candidates[max_candidate][0]] < histo[chord_candidates[j][0]]:

                                    max_candidate = j

                            max_intersect = len(set(chord_candidates[max_candidate]).intersection(set(notes[-i:])))

                            if max_intersect == 3:
                                root_ind = (root_ind - 2 * max_candidate) % 7
                                # print('max:', root_ind)
                                break

            else:
                chord_candidates = []
                for i in max_indices:
                    if i in major_scale:
                        root_ind = major_scale.index(i)
                        chord_candidates.append(
                            [major_scale[root_ind], major_scale[(root_ind + 2) % 7], major_scale[(root_ind + 4) % 7],
                             major_scale[(root_ind + 6) % 7]])
                # print('chord_candidate:', chord_candidates)

                root_ind = major_scale.index(chord_candidates[0][0])
                max_intersect = len(set(chord_candidates[0]).intersection(set(notes)))
                for candidate in chord_candidates:
                   if len(set(candidate).intersection(set(notes))) > max_intersect:
                       root_ind = major_scale.index(candidate[0])

            chord_name = major_notes[scale_degree][root_ind] + major_seventh_chords[root_ind]
            print('chord:', chord_name)
            chord_list.append(chord_name)


        else:
            chord_list.append('-')
            print('no chord')

    return chord_list



def get_key_and_bass_note_from_midi(name, path):

    print('get key and bass notes from', name)

    mid = pm.PrettyMIDI(os.path.join(path, name))

    # Get key
    if len(mid.key_signature_changes) > 0:
        key = mid.key_signature_changes[0].key_number  # ignore key changes

    else:
        print(name+'does not have any key_signature_change')
        return -1


    #Get bass note
    bass_counter = 0
    #bass_piano_roll = []

    for instrument in mid.instruments:
        if bass_counter > 0:   # check the first bass only
            break

        if instrument.program < 40 and instrument.program > 31: # find bass from program number
            print(instrument.name)
            bass_piano_roll = np.copy(instrument.get_piano_roll(fs=8))

            bass_counter += 1

    if bass_counter == 0:
        print(name+'does not have any bass instrument')
        return -1

    bass_notes = []

    # print(bass_piano_roll.shape[1])
    for i in range(0, bass_piano_roll.shape[1], 8):

        mini_roll = np.sum(bass_piano_roll[:, i:(i + 8)], axis = 1)

        if all(mini_roll == 0):
            note = -1

        else:
            note = np.argmax(mini_roll)

        bass_notes.append(note)


    print(key, bass_notes)
    return key, bass_notes



def find_chord_from_midi_file(midi_folder, target_folder):
    invalid_files_counter = 0


    for path, subdirs, files in os.walk(midi_folder):

        for name in files:
            print(name)
            _path = path.replace('\\', '/') + '/'
            _name = name.replace('\\', '/')
            target_path = target_folder+_path[len(midi_folder):]


            if not os.path.exists(target_path):
                os.makedirs(target_path)

            try:
                # Get key and bass note
                key, bass_note = get_key_and_bass_note_from_midi(_name, _path)

                # Get chord
                chord_list = find_chord_from_bass_note(key=key, note_list=bass_note)
                # print(len(chord_list), chord_list)

                pickle.dump(chord_list, open(target_path + _name + '_chord.pickle', 'wb'))

            except:
                exception_str = 'Unexpected error in ' + name,  sys.exc_info()[0]
                print(exception_str)
                invalid_files_counter += 1

    #print key_counter
    #print invalid_files_counter

    #pickle.dump(key_counter, open(midi_folder + '/key_counter_of_' + midi_folder + '.pickle', 'wb'))

