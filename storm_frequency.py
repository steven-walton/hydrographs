import pandas as pd
import numpy as np
import scipy.optimize

def load_PDS(filename):
    df = pd.read_csv(filename, skiprows=13, skipfooter=3, index_col=0)
    df.drop(['200', '500', '1000'], axis=1, inplace=True)
    df = df.stack().reset_index()
    df.columns = ['duration', 'interval', 'rainfall']

    di = {'5-min:': 5.0, '10-min:': 10.0, '15-min:': 15.0, '30-min:': 30.0,
      '60-min:': 60.0, '2-hr:': 120.0, '3-hr:': 180.0, '6-hr:': 360.0,
      '12-hr:': 720.0, '24-hr:': 1440.0, '2-day:': 2880.0, '3-day:': 4320.0,
      '4-day:': 5760.0, '7-day:': 10080.0, '10-day:': 14400.0, '20-day:': 28800.0,
      '30-day:': 43200.0, '45-day:': 64800.0, '60-day:': 86400.0}

    df['duration'].replace(di, inplace=True)
    df['interval'] = df['interval'].apply(lambda x: float(x))

    npa = df.as_matrix()
    x1 = np.array([5.0, 10.0, 15.0, 30.0, 60.0, 120.0, 180.0, 360.0,
                   720.0, 1440.0, 2880.0, 4320.0, 5760.0, 10080.0,
                   14400.0, 28800.0, 43200.0, 64800.0, 86400.0])
    x2s = np.split(npa[:, 1], 19)
    ys = np.split(npa[:, 2], 19)
    return x1, x2s, ys

def powerfit(x, a, b):
    return a * (x**b)

def list_neighbors(ival, vals):
    lowers = []
    uppers = []
    is_equal = False

    for val in vals:
        if val < ival:
            lowers.append(val)
        elif val < ival:
            uppers.append(val)
        elif val == val:
            is_equal = True

    if is_equal == True:
        return [ival, ival]
    else:
        return max(lowers), min(uppers)

def fit_PDS(x2s, ys):
    popts = []
    for xdata, ydata in zip(x2s, ys):
        popt, pcov = scipy.optimize.curve_fit(powerfit, xdata, ydata)
        popts.append(popt)

    popts = np.array(popts)
    a = popts[:, 0]
    b = popts[:, 1]
    return a, b

def recurrence_PDF(x1, a, b, duration, magnitude):
    xlower, xupper = list_neighbors(duration, x1)
    ilower = np.where(x1 == xlower)
    iupper = np.where(x1 == xupper)
    rlower = (magnitude/a[ilower]) ** (1/b[ilower])
    rupper = (magnitude/a[iupper]) ** (1/b[iupper])
    if (xlower - xupper) != 0:
        weight = (duration - xupper) / (xlower - xupper)
    else:
        weight = 0
    r = rlower * weight + rupper * (1 - weight)
    return r
