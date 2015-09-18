
from sklearn import svm
from sklearn import datasets
import numpy as np

f_d = open('recorded_keystrokes_data.train', 'r')
f_t = open('recorded_keystrokes_target.train', 'r')


def get_data(file):
    data_matrix = []
    for line in file:
        stripped_line = line.rstrip('\n').split(', ')
        converted_data = np.array([np.round(float(x), decimals=1) for x in stripped_line])
        data_matrix.append(converted_data)
    return np.array(data_matrix)

data = get_data(f_d)
target = get_data(f_t)

# train svm
svc = svm.SVC(kernel='linear')
svc.fit(data, np.reshape(target,-1) )

f_d = open('recorded_keystrokes_data.txt', 'r')
f_t = open('recorded_keystrokes_target.txt', 'r')

data = get_data(f_d)
target = get_data(f_t)

print 1.0*np.sum(svc.predict(data) == np.reshape(target,-1))/len(data)