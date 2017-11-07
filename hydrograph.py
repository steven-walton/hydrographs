import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

def hydrograph(flow_series, precip_series, ax=None, fig=None, figkwargs=None,
               precip_resample='6H', precip_alpha=0.50):

    moving = flow_series.rolling('D').mean()
    precip_series = precip_series.resample(precip_resample).sum()

    # Create figure and axis if none is specified
    if fig_kwargs is None:
        fig_kwargs = dict(figsize=(11, 8.5))
    if fig is None:
        fig = plt.figure(**fig_kwargs)
    if ax is None:
        ax = fig.add_subplot(1, 1, 1)
    ax2 = ax.twinx()

    # Plot flow
    ax.plot(flow_series, 'r', alpha=0.35)
    ax.plot(moving, 'r')

    # Set bar width
    if precip_resample[-1] == "H":
        if precip_resample == "H":
            width = 1/24
        else:
            n = int(precip_resample[0])
            width = n/24
    elif precip_resample[-1] == "D":
        if precip_resample == "D":
            width = 1
        else:
            n = int(precip_resample[0])
            width = 24*
    elif precip_resample[-1] == 'W':
        if precip_resample == 'W':
            width = 7
        else:
            n = int(precip_resample[0])
            width = n * 7

    # Plot precipitation
    ax2.bar(precip_series['Precipitation'],
            width=width,
            alpha=precip_alpha,
            color='#5287A7')
    ax2.bar(precip_series['Snow Melt'],
            width=width,
            alpha=precip_alpha,
            color='#55A752')

    # Axis formatting

    # Set limits
    ax.set_ylim(0, ax.get_ylim()[1])
    ax2.set_ylim(0, ax2.get_ylim()[1])

    # Set x-tick minor locator
    ax.xaxis.set_minor_locator(mdates.Daylocator(interval=1))
    ax.grid(b=True, which='minor')

    # Color y-tick labels
    for ticklabel in ax.get_yticklabels():
        ticklabel.set_color('#BA3723')
    for ticklabel in ax2.get_yticklabels():
        ticklabel.set_color('#5287A7')

    # Rotate x-tick labels
    for tick in ax.get_xticklabels():
        tick.set_ha('right')
        tick.set_rotation(30)
    
