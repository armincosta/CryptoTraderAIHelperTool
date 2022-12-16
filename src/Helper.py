import pandas as pd
import numpy as np

import dateparser
import pytz
import json

import datetime as dt



class HashTable:

    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]


    def set_val(self, key, val):
        

        hashed_key = hash(key) % self.size
        

        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            
            if record_key == key:
                found_key = True
                break

        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))


    def get_val(self, key):
        

        hashed_key = hash(key) % self.size
        

        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            

            if record_key == key:
                found_key = True
                break


        if found_key:
            return record_val
        else:
            return "No record found"


    def delete_val(self, key):
        

        hashed_key = hash(key) % self.size
        

        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return

    def __str__(self):
        return "".join(str(item) for item in self.hash_table)
        
def binanceDataFrame(klines):
    df = pd.DataFrame(klines.reshape(-1,12),dtype=float, columns = ('Open Time',
                                                                    'Open',
                                                                    'High',
                                                                    'Low',
                                                                    'Close',
                                                                    'Volume',
                                                                    'Close Time',
                                                                    'Quote asset volume',
                                                                    'Number of trades',
                                                                    'Taker buy base asset volume',
                                                                    'Taker buy quote asset volume',
                                                                    'Ignore'))

    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')

    return df

def date_to_milliseconds(date_str):

    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)

    d = dateparser.parse(date_str)

    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)


    return int((d - epoch).total_seconds() * 1000.0)

def interval_to_milliseconds(interval):
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms

def get_historical_klines(symbol, interval, start_str, end_str=None):

    output_data = []

    limit = 500

    timeframe = interval_to_milliseconds(interval)

    start_ts = date_to_milliseconds(start_str)

    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    symbol_existed = False
    while True:
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            output_data += temp_data

            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            start_ts += timeframe

        idx += 1
        if len(temp_data) < limit:
            break

        if idx % 3 == 0:
            time.sleep(1)

    return output_data