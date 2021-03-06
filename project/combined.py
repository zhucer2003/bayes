import numpy as np
from sklearn.metrics import f1_score
from data import Data
from models import CombinedMultinomialBayesianNaiveBayes
import time

print "Loading data..."
data = Data(0.01)
train_X, train_S, train_R = data.load("[0-9a-e]*", True)
val_X, val_S, val_R = data.load("f*")
val_r = np.argmax(val_R.toarray(), axis=1)
val_s = np.argmax(val_S.toarray(), axis=1)

print "Fitting..."
nb = CombinedMultinomialBayesianNaiveBayes(0, 0.1, 0.01)
nb.fit(train_X, train_R, train_S)

print "Predicting receiver..."
start = time.time()
pred_r = nb.predict_receiver(val_X, val_s)
print "Took %f" % (time.time() - start)

print "Predicting sender..."
start = time.time()
pred_s = nb.predict_sender(val_X, val_r)
print "Took %f" % (time.time() - start)

np.savez("combined.npz", pred_r=pred_r, pred_s=pred_s)

print "Receiver:"
print f1_score(val_r, pred_r, average='micro')
print f1_score(val_r, pred_r, average='macro')
print "Sender:"
print f1_score(val_s, pred_s, average='micro')
print f1_score(val_s, pred_s, average='macro')