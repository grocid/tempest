
from sklearn import svm
from sklearn import datasets
import numpy as np

#f_d = open('example_set/train_recorded_keystrokes_data.txt', 'r')
#f_t = open('example_set/train_recorded_keystrokes_target.txt', 'r')
f_d = open('train_recorded_keystrokes_data.txt', 'r')
f_t = open('train_recorded_keystrokes_target.txt', 'r')

keyboard = ['qwertyuiop',
            'asdfghjkl',
            'zxcvbnm']

def approx_distance(x,y):
    xpos = 0, 0
    ypos = 0, 0
    for i, row in enumerate(keyboard):
        q = row.find(x)
        if q != -1:
            xpos = i,q
        q = row.find(y)
        if q != -1:
            ypos = i, q
    return abs((ypos[0] - xpos[0]) + (ypos[1] - xpos[1]))


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

#f_d = open('example_set/recorded_keystrokes_data.txt', 'r')
#f_t = open('example_set/recorded_keystrokes_target.txt', 'r')
f_d = open('recorded_keystrokes_data.txt', 'r')
f_t = open('recorded_keystrokes_target.txt', 'r')

data = get_data(f_d)
target = get_data(f_t)

print "Accuracy:"
print str(100.0*np.sum(svc.predict(data) == np.reshape(target,-1))/len(data)),"%"

print "\nPredicted sentence:"
print ''.join([chr(x) for x in svc.predict(data).astype('int')])
print "Actual sentence:"
print ''.join([chr(x) for x in np.reshape(target,-1).astype('int')])

print "\nAvg. error distance of characters (based on qwerty layout):"
print 1.0*sum([approx_distance(x, y) for x, y in zip([chr(x) for x in svc.predict(data).astype('int')], \
                                                     [chr(x) for x in np.reshape(target,-1).astype('int')])]) / len(data)
     
