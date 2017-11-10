import hydrograph
import precip
import pandas as pd
import os
import matplotlib.pyplot as plt

# Path to test data
script_dir = os.path.dirname(__file__)
rel_path = "testdata/flow.csv"
data_path = os.path.join(script_dir, rel_path)

df = pd.read_csv(data_path, header=0, index_col=0, parse_dates=True)
pdf = precip.get_precip('CO-BO-285', '2017-08-08 00:00', '2017-10-05 07:00')

# Test hydrograph
fig, ax, ax2 = hydrograph.hydrograph(df, pdf, precip_resample='D', fig_kwargs=dict(figsize=(11, 8.5)))

plt.show()

# Test hydrographs
df2 = df*0.5
df3 = df*0.75
df4 = df*1.25

dfs = [df, df2, df3, df4]
fig, ax, ax2 = hydrograph.hydrographs(dfs, pdf, titles=['df', 'df2', 'df3', 'df4'])
plt.show()
