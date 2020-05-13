# This script plots pairwise relationships in the crashes dataset.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# Load the Crashes 2019 data set
df = pd.read_csv('../data/crashes_2019_regions.csv')

# %%

sns.pairplot(df, vars=["POSTED_SPEED_LIMIT", "NUM_UNITS"], diag_kind=None)

# sns.pairplot(df, vars=["POSTED_SPEED_LIMIT", "INJURIES_TOTAL"], diag_kind=None)
# sns.pairplot(df, vars=["POSTED_SPEED_LIMIT", "INJURIES_FATAL"], diag_kind=None)
# sns.pairplot(df, vars=["POSTED_SPEED_LIMIT", "INJURIES_INCAPACITATING"], diag_kind=None)
# sns.pairplot(df, vars=["POSTED_SPEED_LIMIT", "INJURIES_NON_INCAPACITATING"], diag_kind=None)
# sns.pairplot(df, vars=["POSTED_SPEED_LIMIT", "INJURIES_REPORTED_NOT_EVIDENT"], diag_kind=None)
# sns.pairplot(df, vars=["POSTED_SPEED_LIMIT", "INJURIES_NO_INDICATION"], diag_kind=None)

plt.show()
