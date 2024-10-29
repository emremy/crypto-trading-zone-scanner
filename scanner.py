from binance.client import Client
import pandas as pd
import talib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import json
from PyQt5.QtCore import QThread, pyqtSignal


client = Client()

def fetch_data(symbol, interval='1d', lookback='50'):
    klines = client.get_klines(symbol=symbol, interval=interval)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_av', 'trades', 'tb_base_av', 
        'tb_quote_av', 'ignore'])
    
    df['close'] = pd.to_numeric(df['close'])
    df = df[['timestamp', 'close']]

    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    
    df['upper_band'], df['middle_band'], df['lower_band'] = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    
    return df

def is_buy_signal(df):
    latest_data = df.iloc[-1]
    
    rsi_signal = latest_data['RSI'] < 45

    bollinger_signal = latest_data['close'] < latest_data['middle_band']

    if rsi_signal  and bollinger_signal:
        return True
    return False

def create_features(df):
    df['price_change'] = df['close'].pct_change()
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    df['SMA'] = talib.SMA(df['close'], timeperiod=10)
    df.dropna(inplace=True)
    X = df[['price_change', 'RSI', 'upper_band', 'middle_band', 'lower_band']]
    y = np.where(df['price_change'].shift(-1) > 0, 1, 0)
    return X[:-1], y[:-1]

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f'Model Accuracy: {accuracy:.2f}')
    return model

def write_all_symbols():
    exchange_info = client.get_exchange_info()
    with open("exchange_info.json", "w") as f:
        json.dump(exchange_info, f, indent=4)
def model(df,is_buy=True):
    X, y = create_features(df)
    model = train_model(X, y)
    
    latest_data = pd.DataFrame([X.iloc[-1]], columns=X.columns)
    prediction = model.predict(latest_data)
    
    if is_buy:
        return {"status":prediction[0] >= 0.5, "prediction":prediction[0]}
    else:
        return {"status":prediction[0] < 0.5, "prediction":prediction[0]}


class ScannerThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self, interval):
        super().__init__()
        self.interval = interval

    def run (self):
        exchange_info = client.get_exchange_info()
        symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['symbol'].endswith('USDT') and symbol['status'] == 'TRADING']
        total_symbols = len(symbols)
        result = {"buy_zone":[], "sell_zone":[], 'safe_zone':[]}
        for symbol in symbols:
            index = symbols.index(symbol) + 1
            df = fetch_data(symbol,interval=self.interval)
            if len(df) < 40:
                result['safe_zone'].append({
                                'symbol': symbol,
                                'info': 'Not enough data'
                            })
            else:
                if is_buy_signal(df):
                        r = model(df)
                        if r['status']:
                            result['buy_zone'].append({
                                'symbol': symbol,
                            })
                else:
                    r = model(df,is_buy=False)
                    if r['status']:
                        result['sell_zone'].append({
                            'symbol': symbol,
                        })
            progress = (index + 1) / total_symbols * 100
            self.update_progress.emit(int(progress))
        self.finished.emit(result)
