import pickle
file = open("msd_genre.txt", "r")
x = file.readlines()
file.close()
count = 0
genre_dict = {}
keys = []
data_index = 0

for line in x:
    data = line.split()
    print(data)

    genre_dict[data[0]] = data[1]



    count += 1

print(count)
with open('lmd_genre.pkl', 'w') as f:
    pickle.dump(genre_dict, f)

