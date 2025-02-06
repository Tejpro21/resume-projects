def atr_tracker():
    global instrument
    global data
    global closes
    global close
    global current_time
    import pandas as pd
    instrument = 'ETHUSDT'
    def get_data():
            import pandas as pd
            from binance.client import Client
            from datetime import datetime, timedelta
            start_date = 1
            end_date = datetime.now()
            end_date = end_date + timedelta(days=1)
            start_date = end_date - timedelta(days=start_date)
            start_date = str(start_date).split(' ')[0]
            end_date = str(end_date).split(' ')[0]
            user_key = 'kFO5tgPJiE2Azq0gyA5Spj68mA5TgKN5D1LllHhLSKQCJzEb0tktNVgTqO0351Qv'
            secret_key = '1O9MQU9Asw9FBi7PFwDNOcb3w6qpGwTug9RuWCWbnq6ytixiEX37is4HwQQqwr6v'
            binance_client = Client(user_key, secret_key)
            import pandas as pd
            df = pd.DataFrame(binance_client.futures_historical_klines(
                symbol=f'{instrument}',
                interval='1m',
                start_str=f'{start_date}',
                end_str=f'{end_date}',
            ))# crop unnecessary columns
            df = df.iloc[:, :6]
            # ascribe names to columns
            df.columns = ['Datetime', 'open', 'high', 'low', 'Close', 'volume']
            # convert timestamp to date format and ensure ohlcv are all numeric
            df['Datetime'] = pd.to_datetime(df['Datetime'], unit='ms')
            data = df
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col])
            df = df.set_index('Datetime')
            close = round(float(df['Close'].tolist()[-1]), 2)
            closes = round(df['Close'], 2).tolist()
            return closes, close, df, data
    def ist_to_gmt():
        from datetime import datetime
        from pytz import timezone
        format = "%H:%M"
        utc = datetime.now(timezone('UTC'))
        return utc.strftime(format)
    closes = get_data()[0]
    close = get_data()[1]
    df = get_data()[2]
    data = get_data()[-1]
    current_time = ist_to_gmt()
    def atr():
        import numpy as np
        import pandas as pd
        high_low = data['high'] - data['low']
        high_cp = np.abs(data['high'] - data['Close'].shift())
        low_cp = np.abs(data['low'] - data['Close'].shift())
        df = pd.concat([high_low, high_cp, low_cp], axis=1)
        true_range = np.max(df, axis=1)
        atr = list(true_range.rolling(14).sum()/14)
        atr = atr[:85]
        atr = atr[14:]
        atr_avg = round(float(max(atr))+float(min(atr)), 2)/2
        atr_avg = atr_avg + atr_avg*0.2
        return atr[-1], atr_avg
    atr_value = atr()[0]
    atr_avg_value = atr()[-1]
    if atr_value < atr_avg_value:
        print('ATR is LOW :D')
    else:
        print('ATR is HIGH!')
while 1:
    from time import sleep
    atr_tracker()
    sleep(59)
