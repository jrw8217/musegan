import json
import os
import sys




def check_is_drum_of_Grand_Piano(midi_folder):
    invalid_files_counter = 0

    song_count = 0
    one_is_drum = 0
    not_one_is_drum = []

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


                    is_drum_count = 0
                    for key, dic in zip(dict.keys(), dict.values()):
                        if dic['is_drum'] == True:
                            print '0: ', dict['0']
                            print 'key: ', key
                            print dic
                            is_drum_count += 1

                    print 'is_drum count = ', is_drum_count

                    if is_drum_count == 1:
                        one_is_drum += 1
                    else:
                        not_one_is_drum.append(_path)



            except:
                exception_str = 'Unexpected error in ' + name,  sys.exc_info()[0]
                print(exception_str)
                invalid_files_counter += 1


    print '-----------------------------------------------'
    print 'song count: ', song_count
    print 'one_is_drum count: ', one_is_drum
    print 'not one is_drum: ', not_one_is_drum


if __name__ == '__main__':
    path = '/home/wan/Documents/projects/data_processed/test_lmd_processed'
    check_is_drum_of_Grand_Piano(path)