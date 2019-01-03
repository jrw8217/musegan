import pretty_midi
import os

def check_ts(datapath):
    for path, subdirs, files in os.walk(datapath):
        if not subdirs:
            for file in files:
                filepath = os.path.join(path, file)
                try:
                    pm = pretty_midi.PrettyMIDI(filepath)
                    if pm.time_signature_changes:
                        tsc = pm.time_signature_changes[0]
                        if tsc.time > 0.0:
                            print(filepath, tsc)

                except:
                    print(filepath, 'does not work')


check_ts('data1/lakh/lmd_full')