import pickle
file = open("msd_genre_dataset.txt", "r")
x = file.readlines()
file.close()
count = 0
genre_dict = {}
keys = []
data_index = 0

for line in x:
    if line.startswith("%"):
        print(line)
        keys.extend(line[1:].split(','))
        data_index = count

    if count > data_index:
        data = line.split(',')
        if len(keys) != len(data):
            continue
        assert len(keys) == len(data)
        small_dict = {}
        for i in range(len(keys)):
            small_dict[keys[i]] = data[i]
        genre_dict[data[1]] = small_dict


    count += 1

print(count)
with open('lmd_genre_artist_py2.pkl', 'w') as f:
    pickle.dump(genre_dict, f)

