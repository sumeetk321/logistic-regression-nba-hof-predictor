import pandas as pd
import numpy as np

train_data = pd.read_csv("nba_stats_dataset.csv")
train_data = train_data.drop(['Unnamed: 0', 'player_id', 'player'], axis=1)
print(train_data)
train_data_np = train_data.to_numpy()

print(train_data_np.shape)

X = train_data_np[:,:-1]
y = train_data_np[:,-1]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

from sklearn import svm

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

from sklearn import metrics

# Model Accuracy: how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

test = np.array([665,21815.0,4867,10669,1979.0,4758.0,2888,5911,1240,1461,295.0,2024.0,2319.0,1543,589.0,355.0,1127.0,1399,12953,5,0,0,0,0,0,3,2,1,0])

pred = clf.predict(test.reshape(1, -1))

print(pred)
