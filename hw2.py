import pandas as pd
from sklearn.model_selection import train_test_split
from datetime import datetime
import xgboost as xgb
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


# input the date string, return the number of week of that year
def get_week(s):
    year_s, mon_s, day_s = s.split('-')
    a = datetime(int(year_s), int(mon_s), int(day_s))
    b = a.isocalendar()[1]
    return b


# input the date string, return year
def get_year(s):
    year_s, mon_s, day_s = s.split('-')
    return year_s


df = pd.read_csv(r"C:\Users\Louis\Desktop\vineyard_weather_1948-2017.csv")

# Create the new row called week
df["WEEK"] = 0
df["YEAR"] = 0
for i in range(len(df["DATE"])):
    df["WEEK"][i] = get_week(df["DATE"][i])
    df["YEAR"][i] = get_year(df["DATE"][i])

# Only keep week 35 to week 40
# Drop function return a new object but not change the old df
df1 = df.drop(df[df.WEEK < 35].index)
df2 = df1.drop(df[df.WEEK > 40].index)
df3 = df2.drop(["DATE"], axis=1)

# group by week and year
df4 = df3.groupby(['YEAR', 'WEEK']).agg({"PRCP": ["sum"], "TMAX": ["max"], "TMIN": ["min"], "RAIN": ["sum"]})

# column to row
df5 = (df4.unstack())

# The X is week 35-39, Y is week 40
X = df5.iloc[:, [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22]]
Y = df5.iloc[:, [5, 11]]
Y["STORM"] = 0

# Normalized df
#X1 = (X-X.min())/(X.max()-X.min())

# Add the row STORM, use temp and PRCP to decide if it is a storm(as 1)
# again
for i in range(len(Y["STORM"])):
    if Y.iloc[i, 1] <= 80 and Y.iloc[i, 0] >= 0.35:
        Y.iloc[i, 2] = 1
    else:
        Y["STORM"][i] = 0

# Y1 should be the Y label used for training
Y1 = Y.iloc[:, 2]

# The X is week 35-39 , Y is week 40
# X=df4.iloc[:-70,:]
# Y=df4.iloc[-70:,:]

'''
xgb1 = XGBRegressor(booster='gbtree',
                    objective= 'reg:linear',
                    eval_metric='rmse',
                    gamma = 0.1,
                    min_child_weight= 10,
                    max_depth= 10,
                    subsample= 0.8,
                    colsample_bytree= 0.8,
                    tree_method= 'exact',
                    learning_rate=0.05,
                    n_estimators=100,
                    nthread=4,
                    scale_pos_weight=1,
                    reg_alpha=0.05,
                    seed=100)
'''

X_train, X_test, y_train, y_test = train_test_split(X, Y1, test_size=0.2)
bst = xgb.XGBRegressor(seed=1850)
bst.fit(X_train, y_train)
preds = bst.predict(X_test)

preds1 = []
for i in preds:
    if i > 0.5:
        preds1.append(1)
    else:
        preds1.append(0)

print(X_test)

print("Accuracy: ")
print(accuracy_score(y_test, preds1))

print("Precision: ")
print(precision_score(y_test, preds1, average='macro'))

print("Recall: ")
print(recall_score(y_test, preds1, average='macro'))


from dagshub import dagshub_logger

with dagshub_logger() as logger:
    logger.log_metrics({"Accuracy":accuracy_score(y_test, preds1)})
    logger.log_metrics({"Precision":precision_score(y_test, preds1, average='macro')})
    logger.log_metrics({"Recall":recall_score(y_test, preds1, average='macro')})

    logger.save()
    logger.close()