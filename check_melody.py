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
                        dict = json.load(inst)


                    melody_count = 0
                    for key, dic in zip(dict.keys(), dict.values()):
                        if dic['name'].lower() == 'melody':
                            print 'key: ', key
                            print dic
                            melody_count += 1

                    print 'melody count = ', melody_count

                    if melody_count > 0:
                        melody_track_count += 1
                    else:
                        no_melody_track.append(_path)



            except:
                exception_str = 'Unexpected error in ' + name,  sys.exc_info()[0]
                print(exception_str)
                invalid_files_counter += 1


    print '-----------------------------------------------'
    print 'song count: ', song_count
    print 'melody track count: ', melody_track_count
    #print 'no melody count: ', no_melody_track


if __name__ == '__main__':
    path = '/data1/lakh/lmd_matched_processed_with_one_chord_per_bar'
    check_is_drum_of_Grand_Piano(path)
