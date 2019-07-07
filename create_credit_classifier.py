import pandas as pd

###
### Load Data Set
###
path='clean_data.csv'
df=pd.read_csv(
    'clean_data.csv')
data = df
# Drop rows with missing column data


###
### Convert Data Into List Of Dict Records
###
data = data.to_dict(orient='records')

###
### Seperate Target and Outcome Features
###
from sklearn.feature_extraction import DictVectorizer
from pandas import DataFrame
vec = DictVectorizer()

df_data = vec.fit_transform(data).toarray()
feature_names = vec.get_feature_names()
df_data = DataFrame(
    df_data,
    columns=feature_names)
    
outcome_feature = df_data['employeed']
target_features = df_data.drop('employeed', axis=1)









#######################################





 




###
### Generate Training and Testing Set 
###
from sklearn import cross_validation

"""
    X_1: independent variables for first data set
    Y_1: dependent (target) variable for first data set
    X_2: independent variables for the second data set
    Y_2: dependent (target) variable for the second data set
"""
X_1, X_2, Y_1, Y_2 = cross_validation.train_test_split(
    target_features, outcome_feature, test_size=0.5, random_state=0)
    
    
    

    
###
### Define Classifier
###                             
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()


###
### Train Classifier on (X1,Y1) and Validate on (X2,Y2)
###                              
clf.fit(X_1,Y_1)
score = clf.score(X_2, Y_2)
print ("accuracy: {0}".format(score.mean()))


###
### Print Confusion Matrix
###

output = clf.predict(X_2)

from sklearn.metrics import confusion_matrix
matrix = confusion_matrix(output, Y_2)
print ("Confusion matrix")
print (matrix)

from sklearn.metrics import f1_score

f1 = f1_score(output, Y_2, average='macro')



from sklearn.metrics import classification_report

target_names = ['Not Employeed', 'Employeed']

cr = classification_report(output, Y_2, target_names=target_names)

print (" Classification Report")
print (cr)

df = DataFrame([[
        4.0,4.0,4.0,1.0,1.0,
         2.0,
         0.0,
         87.00,
         0.0,
         60.750,
         65.380,
         68.590,
         58.240,
         58.8200,
         55.53,
         91.08,
         61.22
      ]])






a = clf.predict(df)




###
### Save Classifier
###
from sklearn.externals import joblib
joblib.dump(clf, 'nba.pkl')











#########################################






