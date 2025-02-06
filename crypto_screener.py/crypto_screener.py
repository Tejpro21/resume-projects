def rsi_based_img(instrument):
    time_interval = '1m'
    def get_data():
        import pandas as pd
        global df
        global stock_df
        from binance.client import Client
        from datetime import datetime, timedelta
        if time_interval == '1m':
            start_date = 1
            interval = '1m'
        elif time_interval == '5m':
            start_date = 2
            interval = '5m'
        elif time_interval == '1h':
            start_date = 10
            interval = '1h'
        elif time_interval == '1d':
            start_date = 100
            interval = '1d'
        else:
            print(f'ERROR "{time_interval}" is not an authorised time interval. \nAuthorised time intervals are: 5m, 1h, 1d.')
            print('================================================================')
            exit()
        end_date = datetime.now()    
        end_date = end_date + timedelta(days=1)
        start_date = end_date - timedelta(days=start_date)
        start_date = str(start_date).split(' ')[0]
        end_date = str(end_date).split(' ')[0]
        user_key = 'kFO5tgPJiE2Azq0gyA5Spj68mA5TgKN5D1LllHhLSKQCJzEb0tktNVgTqO0351Qv'
        secret_key = '1O9MQU9Asw9FBi7PFwDNOcb3w6qpGwTug9RuWCWbnq6ytixiEX37is4HwQQqwr6v'
        binance_client = Client(user_key, secret_key)
        df = pd.DataFrame(binance_client.futures_historical_klines(
            symbol=f'{instrument}',
            interval=f'{interval}',
            start_str=f'{start_date}',
            end_str=f'{end_date}',
        ))# crop unnecessary columns
        df = df.iloc[:, :6]
        # ascribe names to columns
        df.columns = ['Datetime', 'open', 'high', 'low', 'Close', 'volume']
        # convert timestamp to date format and ensure ohlcv are all numeric
        df['Datetime'] = pd.to_datetime(df['Datetime'], unit='ms')
        times_in_gst = []
        time = df['Datetime'].tolist()
        if time_interval != '1d':
            for i in time:
                i = str(i).split(' ')[-1]
                i = str(i).split(':')
                i = f'{i[0]}:{i[1]}'
                times_in_gst.append(i)
        elif time_interval == '1d':
            for i in time:
                i = str(i).split(' ')[0]
                times_in_gst.append(i) 
        data = df
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col])
        df = df.set_index('Datetime')
        stock_df = pd.DataFrame(df['Close'], columns=['Close'])
        close = round(float(df['Close'].tolist()[-1]), 2)
        closes = round(df['Close'], 2).tolist()
        return closes, close,times_in_gst, data
    def atr():
        import numpy as np
        import pandas as pd
        data = get_data()[-1]
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
    def rsi():
        import pandas_ta as pta
        get_data()
        rsi_valuess = round(pta.rsi(df['Close'], length = 14), 0)
        rsi_valuess = [x for x in rsi_valuess if str(x) != 'nan']
        rsi_values = []
        for i in rsi_valuess:
            i = int(i)
            rsi_values.append(i)
        return rsi_values
    def rsi_based_sma():
        rsi_values = rsi()
        arr = rsi_values
        window_size = 14
        i = 0
        moving_averages = []
        while i < len(arr) - window_size + 1:
            window = arr[i : i + window_size]
            window_average = int(round(sum(window) / window_size, 0))
            moving_averages.append(window_average)
            i += 1
        import pandas as pd
        times_in_gst = pd.DataFrame(get_data()[-2][14:], columns=['Time_in_gst'])
        closes = pd.DataFrame(get_data()[0][14:], columns=['Close'])
        rsi_vals = pd.DataFrame(rsi_values, columns=['RSI'])
        data = pd.DataFrame([0,0,0,0,0,0,0,0,0,0,0,0,0] + moving_averages, columns=['SMA']).join(closes).join(rsi_vals).join(times_in_gst)
        # print(moving_averages['Close'].tolist()[-1])
        # print(moving_averages['SMA'].tolist()[-1])
        # print(moving_averages['RSI'].tolist()[-1])
        # print(moving_averages['Time_in_gst'].tolist()[-1])
        times_in_gst = data['Time_in_gst'].tolist()
        rsi_values = data['RSI'].tolist()
        moving_averages = data['SMA'].tolist()
        def intersection(in1, in2, out1, out2):#in = RSI, out = SMA
            check = []
            check2 = []
            if in1 <= in2 and out1 <= out2:
                check = list(range(in1, in2))
                check2 = list(range(out1, out2))
                if len(check2) == 0:
                    check2.append(out2)
                    check.append(in2)
            elif in1 <= in2 and out1 >= out2:
                check = list(range(in1, in2))
                check2 = list(range(out2, out1))
                if len(check2) == 0:
                    check2.append(out2)
                    check.append(in2)
            elif in1 >= in2 and out1 >= out2:
                check = list(range(in2, in1))
                check2 = list(range(out2, out1))
                if len(check) == 0 or len(check2) == 0:
                    check2.append(out1)
                    check.append(in1)
            elif in1 >= in2 and out1 <= out2:
                check = list(range(in2, in1))
                check2 = list(range(out1, out2))
                if len(check) == 0 or len(check2) == 0:
                    check2.append(out2)
                    check.append(in2)
            output = any(item in check for item in check2)
            if out2 == out1:
                if out2 in check:
                    output = True
            if in2 == in1:
                if in2 in check2:
                    output = True
            if out2 == in2 or out1 == in1:
                output = True
            return output
        stimes = []
        signals = []
        for i in range(len(times_in_gst)):
            trade = False
            sig = 'false'
            #print((rsi_values[i], rsi_values[i-1] ,moving_averages[i], moving_averages[i-1], times_in_gst[i]))
            if intersection(rsi_values[i], rsi_values[i-1] ,moving_averages[i], moving_averages[i-1]) == True:
                if rsi_values[i-1] < moving_averages[i-1]:
                    #print('Up')
                    sig = 'Up'
                elif rsi_values[i-1] > moving_averages[i-1]:
                    #print('Down')
                    sig = 'Down'
                else:
                    pass
                trade = True
            else:
                trade = False
                sig = 'false'
            if sig != 'false':
                sig = f'{sig}|{times_in_gst[i]}'
                signals.append(sig)
        def time_diffrence(time_of_sig):
            def ist_to_gmt():
                from datetime import datetime
                from pytz import timezone
                format = "%H:%M"
                utc = datetime.now(timezone('UTC'))
                return utc.strftime(format)
            time_now_in_gmt = ist_to_gmt()
            from datetime import datetime
            time_1 = datetime.strptime(f'{time_of_sig}', "%H:%M")
            time_2 = datetime.strptime(f'{time_now_in_gmt}',"%H:%M")
            time_interval = 0
            if time_1 == time_2:
                time_interval = 1
            return int(time_interval)
        i = signals[-1]
        i = str(i).split('|')[-1]
        atr_value = round(atr()[0],2)
        atr_avg = atr()[-1]
        if atr_value < atr_avg:
            if time_diffrence(i) == 1:

                if int(rsi_values[-1]) > 60:
                    print('-----------{IMG}-----------')
                    print(f'{instrument}|ATR:{atr_value}|RSI:{rsi_values[-1]}|RSI: Overbought')
                    print('-----------{IMG}-----------')
                elif int(rsi_values[-1]) < 40:
                    print('-----------{IMG}-----------')
                    print(f'{instrument}|ATR:{atr_value}|RSI:{rsi_values[-1]}|RSI: Oversold')
                    print('-----------{IMG}-----------')
                else:
                    print('-----------{IMG}-----------')
                    print(f'{instrument}|ATR:{atr_value}|RSI:{rsi_values[-1]}')
                    print('-----------{IMG}-----------')
    rsi_based_sma()
import pandas as pd
data = pd.read_csv('/Users/tejas/Desktop/Folder_of_Folders/Python_files/Crypto_screener.py/tickers.csv')['ticker'].tolist()
for i in data:
    rsi_based_img(f"{i}")