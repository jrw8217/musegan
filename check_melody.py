import json
import os
import sys




def check_is_drum_of_Grand_Piano(midi_folder):
    invalid_files_counter = 0

    song_count = 0
    melody_track_count = 0
    no_melody_track = []

    for path, subdirs, files in os.walk(midi_folder):



        for name in files:

            _path = path.replace('\\', '/') + '/'
            _name = name.replace('\\', '/')


            try:
                if _name == 'instruments.json':
                    song_count += 1
                    print _path
                    with open(_path + _name) as inst:
                        dictionary = json.load(inst)


                    melody_count = 0
                    for key, dic in zip(dictionary.keys(), dictionary.values()):
                        if dic['name'].lower() == 'melody':
                            print 'key: ', key
                            print dic
                            melody_count += 1
			    
                    print 'melody count = ', melody_count

                    if melody_count > 0:
                        melody_track_count += 1
                    else:
                        no_melody_track.append(_path)

		    print 'melody track count = ', melody_track_count

            except:
                exception_str = 'Unexpected error in ' + name,  sys.exc_info()[0]
                print(exception_str)
                invalid_files_counter += 1


    print '-----------------------------------------------'
    print 'song count: ', song_count
    print 'melody track count: ', melody_track_count
    print 'no melody midi: ', no_melody_track[:10]


if __name__ == '__main__':
    path = '/data/midi/lmd_matched_processed'
    check_is_drum_of_Grand_Piano(path)
