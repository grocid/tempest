## Acoustic attack on keyboards

# Usage

First run tempest.py and record a training set. It has to be 'sufficiently' large to be able to classify keystrokes.

Rename the files recorded_keystrokes_data.txt and recorded_keystrokes_target.txt to recorded_keystrokes_data.train and recorded_keystrokes_target.train, respectively. Now run tempest.py again to generate a test set. When ready, run svm.py.