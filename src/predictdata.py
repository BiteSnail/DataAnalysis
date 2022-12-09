from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
import savedata
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

poly = PolynomialFeatures(degree=2)

def preprocess(df):
#data preprocessing
    ndf = df[df.PowerGeneration < 5000].drop(['year', 'month', 'day', '최고기온시각', '최저기온시각일교차', '1시간최다강수량시각'], axis=1)
    x=ndf.drop(savedata.english_dict['발전량'], axis=1)
    y=ndf[savedata.english_dict['발전량']]
    return x, y

def get_predictmodel(x, y, test_size=0.3, random_state=10, make_image=True):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
    print('훈련 데이터: ', x_train.shape)
    print('훈련 데이터: ', x_test.shape)

    x_train_poly=poly.fit_transform(x_train)
    print('원 데이터: ', x_train.shape)
    print('2차항 변환 데이터: ',x_train_poly.shape)

    pr = LinearRegression()
    pr.fit(x_train_poly, y_train)

    x_test_poly = poly.fit_transform(x_test)
    y_hat_test = pr.predict(x_test_poly)

    if(make_image):
        key = savedata.english_dict.values()
        for i in range(0, 10):
            plt.figure(figsize=(10,5))
            plt.plot(x_train[key[i]], y_train, 'o', alpha=0.5,label='Train')
            plt.plot(x_test[key[i]], y_hat_test, '+', label='Predict')
            plt.legend(loc='best'); plt.title(key[i] + 'Prediction')
            plt.xlabel(key[i]); plt.ylabel('power')
            plt.savefig(savedata.save_images_result+key[i]+' Prediction.png')
        
    return pr, x_train, x_test, y_train, y_test

def pridict(pr, x, y):
    x_ploy = poly.fit_transform(x)
    y_hat = pr.predict(x_ploy)

    plt.figure(figsize=(10, 5))
    ax1 = sns.distplot(y, hist=False, label='y')
    ax2 = sns.distplot(y_hat, hist=False, label='y_hat', ax=ax1)
    plt.legend()
    plt.savefig(savedata.saved_path+'result.png')

    MSE = mean_squared_error(y, y_hat)
    RMSE = mean_squared_error(y, y_hat, squared=False)

    return MSE, RMSE