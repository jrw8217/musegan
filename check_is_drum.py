import json
import os
import sys




def check_is_drum_of_Grand_Piano(midi_folder):
    invalid_files_counter = 0


    for path, subdirs, files in os.walk(midi_folder):

        for name in files:

            _path = path.replace('\\', '/') + '/'
            _name = name.replace('\\', '/')


            try:
                if _name == 'instruments.json':
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

            except:
                exception_str = 'Unexpected error in ' + name,  sys.exc_info()[0]
                print(exception_str)
                invalid_files_counter += 1



if __name__ == '__main__':
    path = '/home/wan/Documents/projects/data_processed/test_lmd_processed'
    check_is_drum_of_Grand_Piano(path)