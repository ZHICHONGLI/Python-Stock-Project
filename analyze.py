import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm
import quandl

def analyze(data, days = 30):
    df = data
    # set predicting {days} into future
    forecast_out = int(days) 
    # data column shifted {days} up
    df['Prediction'] = df[['Adj Close']].shift(-forecast_out) 
    # print(df)
    X = np.array(df.drop(['Prediction'], 1))
    X = preprocessing.scale(X)
    # set X_forecast
    X_forecast = X[-forecast_out:] 
    # remove last {days} from X
    X = X[:-forecast_out] 
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.2)

    # Training
    clf = LinearRegression()
    clf.fit(X_train,y_train)
    # Testing
    confidence = clf.score(X_test, y_test)
    print("confidence: ", confidence)
    #  Result
    forecast_prediction = clf.predict(X_forecast)

    return forecast_prediction

def getDateRangeData(stockData):
    dateRangeData = {}
    dateRangeData["startDate"] = stockData[0]["Date"]
    dateRangeData["endDate"] = stockData[-1]["Date"]
    dateRangeData["high"] = float(stockData[0]["Adj Close"])
    dateRangeData["low"] = float(stockData[0]["Adj Close"])
    total = 0
    for i in stockData:
        if float(i["Close"]) > dateRangeData["high"]:
            dateRangeData["high"] = float(i["Adj Close"])
        if float(i["Close"]) < dateRangeData["low"]:
            dateRangeData["low"] = float(i["Adj Close"])
        total += float(i["Adj Close"])

    dateRangeData["avg"] = total / len(stockData)
    return dateRangeData
