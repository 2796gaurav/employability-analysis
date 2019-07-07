from surprise import Reader, Dataset
import surprise
# Define the format
reader = Reader(line_format='user item rating', sep=',')
# Load the data from the file using the reader format
data = Dataset.load_from_file('recomm.csv', reader=reader)

# Split data into 5 folds
data.split(n_folds=5)

from surprise import SVD, evaluate
algo = SVD()
evaluate(algo, data, measures=['RMSE', 'MAE'])


# Retrieve the trainset.
trainset = data.build_full_trainset()
algo.train(trainset)


userid = str(10)
itemid = str(20)
actual_rating = 3
print (algo.predict(userid, 40))

a =  algo.predict(userid, 20)
t = a.est/3
print (t)


from sklearn.externals import joblib
joblib.dump(algo, 'reccc.pkl')





	




