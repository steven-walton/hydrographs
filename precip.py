import requests
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime, time, date, timedelta
import time
import io

def get_precip(station, start_date, end_date):
    """
    Retrieves rainfall and snow melt data for a given station and date range.
    Output is a pandas DataFrame with two columns: 'Precipitation' and 'Snow Melt'
    """
    dfp = get_rainfall_data(station, start_date, end_date, type='p')
    dfs = get_rainfall_data(station, start_date, end_date, type='s')
    df = pd.DataFrame()
    df['Precipitation'] = dfp['(Modeled) Non-Snow Precipitation (in of water)']
    df['Snow Melt'] = dfs['(Modeled)SnowMelt Rate (in/hr)']
    df.fillna(value=0.0)
    df.index = pd.to_datetime(df.index)
    return df

def get_rainfall_data(station, start_date, end_date, type='p'):
    # create datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')

    # nohrsc can only output one year of data at a time
    # so if date range is more than a year, create date list
    if (end_date - start_date).days > 365:
        td = timedelta(days=364)
        date_list = [start_date]
        while date_list[-1] < end_date:
            date_list.append(date_list[-1] + td)
        date_list[-1] = end_date
    else:
        date_list = [start_date, end_date]

    # use rainfall_scrape function to pull dataframe for each date in date_list
    dfs = []
    for count, date in enumerate(date_list[0:-1]):
        start_date = date
        end_date = date_list[count+1]
        dfs.append(_rainfall_scrape(station, start_date, end_date, type))

    # Concat DataFrames and return
    df = pd.concat(dfs)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def _rainfall_scrape(station, start_datetime, end_datetime, type='p'):

    # site url
    url = 'http://www.nohrsc.noaa.gov/interactive/html/graph.html?station={station_id}&o=a&uc=0&by={start_year}' \
      '&bm={start_month}&b{start_day}=1&bh={start_hour}&ey={end_year}&em={end_month}&ed={end_day}' \
      '&eh={end_hour}&data={data_output}&units=0&region=us'

    # set data_ouput query
    if type == 'p':
        data_output = 12
    elif type == 's':
        data_output = 16
    else:
        data_output = 12

    # write and post request
    full_url = url.format(station_id=station, start_year=start_datetime.year, end_year=end_datetime.year, start_month=start_datetime.month,
                          end_month=end_datetime.month, start_day=start_datetime.day, end_day=end_datetime.day, start_hour=start_datetime.hour,
                          end_hour=end_datetime.hour, data_output=data_output)

    response = requests.get(full_url, headers={'user-agent': 'mozilla/5.0 (windows nt 6.1) applewebkit/537.36 '
                                                             '(khtml, like gecko) chrome/41.0.2228.0 safari/537.36'})
    # write response to dataframe
    data = response.text.replace('<br>', '')
    df = pd.read_csv(io.StringIO(data), index_col=0)
    return df

def main():
    df = get_precip('CO-BO-285', '2017-10-01 00:00', '2017-11-01 00:00')
    print(df.head())

if __name__ == '__main__':
    main()
