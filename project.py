# coding: utf-8

# In[1]:

class Table(dict):
    def __init__(self):
        self.users_for_movie = {}
        self.movies_for_user = {}

    def set(self, u, m, r):
        self[(u, m)] = r
        # add code to update users_for_movie and movies_for_user  
        self.users_for_movie[u] = u
        self.movies_for_user[m] = m

    def read(self, u, m):
        return self.get((u, m), None)

    def get_users_for_movie(self, m):
        return self.users_for_movie.get(m, None)

    def get_movies_for_user(self, u):
        return self.movies_for_user.get(u, None)


# In[2]:

T_data = Table()
um_id = []

# In[4]:

for l in open('u1.base', 'r'):
    u, m, r = [int(x) for x in l.rstrip().split('\t')][:3]
    # add code to put data into your table
    T_data.set(u, m, r)
    # in the mean time, use a list to hold all the user ids and movie ids
    um_id.append([u, m])

# In[5]:

import numpy as np


# T_data: the data table
# n_movie: the max movie id


def make_adj_table(T_data, n_movie):
    T = 1e8 * np.ones(shape=(n_movie + 1, n_movie + 1))
    for i in range(1, n_movie):
        ui = T_data.get_users_for_movie(i)
        for j in range(i + 1, n_movie + 1):
            uj = T_data.get_users_for_movie(j)
            # calculate adjustment that is need to predict rating for movie j using ratings for movie i
            T[ui - 1, uj - 1] = (T_data.get((ui, uj))) / 2
    return T


f1 = open('u.item', encoding="ISO-8859-1")
last_line = f1.readlines()[-1]

number = int(last_line[0:4])


T_adj = make_adj_table(T_data, number)

# In[ ]:

fout = open('u.predict', 'w')
for l in open('u1.test', 'r'):
    u, m = [int(x) for x in l.rstrip().split('\t')][:2]
    mm = T_data.get_movies_for_user(u)
    predict = 0.0
    n = 0

    # predict rating for movie m using movies in the set "mm"

    fout.write('{user}\t{movie}\t{predict:.2f}\n'.format(user=u, movie=m, predict=predict))
fout.close()


# In[ ]:
