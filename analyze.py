import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm


def analyze(data, days=30):
    dataFrame = data
    # set predicting {days} into future
    forecastLength = int(days)
    # data column shifted {days} up
    dataFrame['Prediction'] = dataFrame[['Adj Close']].shift(-forecastLength)
    X = np.array(dataFrame.drop(['Prediction'], 1))
    X = preprocessing.scale(X)
    # set X_forecast
    X_forecast = X[-forecastLength:]
    # remove last {days} from X
    X = X[:-forecastLength]
    y = np.array(dataFrame['Prediction'])
    y = y[:-forecastLength]

    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=0.2)

    # Training
    linear = LinearRegression()
    linear.fit(X_train, y_train)
    # Testing
    accurate = linear.score(X_test, y_test)
    print("accurate: ", accurate)
    #  Result
    prediction = linear.predict(X_forecast)

    return prediction


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
