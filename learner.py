import os
import numpy as np
import struct
from sklearn import svm
from scipy import fftpack

class SampleSet:
    def __init__(self, x=None, y=None):
        self.x = x if x else []
        self.y = y if y else []
    
    def add_x_and_y(self, x, y):
        self.x += x
        self.y += y

    def separate_sets(self, proportion):
        #Todo: should shuffle

        separation = int(round(len(self.x) * proportion))
        return [
            SampleSet(self.x[:separation], self.y[:separation]),
            SampleSet(self.x[separation:], self.y[separation:])
        ]

class Learner:
    
    def learn(self, x, y):
        self.classifier = svm.SVC()
        self.classifier.fit(x, y)

    def predict(self, x):
        return self.classifier.predict(x)

    @classmethod
    def score(cls, real, prediction):
        true_pos=0
        false_pos=0
        true_neg=0
        false_neg=0
        for i in [0, len(real)-1]:
            if prediction[i]:
                if real[i]:
                    true_pos += 1
                else:
                    false_pos += 1
            else:
                if real[1]:
                    false_neg += 1
                else:
                    true_neg += 1
        return {
            'true pos': true_pos,
            'true_neg': true_neg,
            'false pos': false_pos,
            'false_neg': false_neg,
            'precision': true_pos * 1.0 / (true_pos + false_pos + 0.01),
            'recall': true_pos * 1.0 / (true_pos + true_neg + 0.01)
        }

class Sample:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @classmethod
    def load_from_folder(cls, folder):
        return [cls.load_from_file("%s/%s" % (folder, filename)) for filename in os.listdir(folder) if ".dat" in filename]

    @classmethod
    def load_from_file(cls, filename):
        print("load")
        raw_data = []
        with open(filename) as file:
            data = file.read()
        for i in range(0, len(data) / 8):
            raw_data.append(np.array(struct.unpack('2f', data[i*8:(i+1)*8])).astype("f"))
        return Sample(raw_data)

    def compute_features(self):
        #TODO: Extract features

        self.features = fftpack.rfft([i[0] for i in self.raw_data])[:1000]

print("Loading data...")
order_samples = Sample.load_from_folder("recordings/orders")
no_order_samples = Sample.load_from_folder("recordings/no_orders")
    
print("Data loaded: %i orders, %i total" % (len(order_samples), len(order_samples) + len(no_order_samples)) )


print("Computing features...")
for sample in order_samples:
    sample.compute_features()
for sample in no_order_samples:
    sample.compute_features()


set = SampleSet()
set.add_x_and_y([sample.features for sample in order_samples], [1 for sample in order_samples])
set.add_x_and_y([sample.features for sample in no_order_samples], [0 for sample in order_samples])

train_set, test_set = set.separate_sets(0.7)    

print("Learning...")
learner = Learner()
learner.learn(train_set.x, train_set.y)


print("Learnt: ")
predict = learner.predict(test_set.x)
print(Learner.score(test_set.y, predict))