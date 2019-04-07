import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm
import quandl

def analyze(data, days = 30):
    # df = quandl.get("WIKI/AAPL")
    # print(df)
    # df = df[['Adj. Close']]
    # df = data[['Adj. Close']]
    df = data
    # print(df)
    forecast_out = int(days) # predicting 30 days into future
    df['Prediction'] = df[['Adj Close']].shift(-forecast_out) #  label column with data shifted 30 units up
    # print(df)
    X = np.array(df.drop(['Prediction'], 1))
    X = preprocessing.scale(X)
    X_forecast = X[-forecast_out:] # set X_forecast equal to last 30
    X = X[:-forecast_out] # remove last 30 from X
    # print(X_forecast, X)
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]
    # print('y :', y)

    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.2)

    # Training
    clf = LinearRegression()
    clf.fit(X_train,y_train)
    # Testing
    confidence = clf.score(X_test, y_test)
    print("confidence: ", confidence)

    forecast_prediction = clf.predict(X_forecast)
    print(forecast_prediction)

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
