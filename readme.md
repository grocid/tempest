# Acoustic attack on keyboards

### Usage

1. Run `tempest.py -train` and record a training set. It has to be quite large to be able to classify keystrokes. For a good result: 
	1. Push each key several times.
	2. Do not push the keys too frequently.

2. Run `tempest.py` and record a test set.

3. To start the support vector machine classifer and get the results, run `svm.py`.


Based on the code [here][http://julip.co/2012/05/arduino-python-soundlight-spectrum/].