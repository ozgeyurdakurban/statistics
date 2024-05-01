# -*- coding: utf-8 -*-
"""
Created on Thu May  2 01:02:24 2024

@author: eoyur
"""


import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.stats import ttest_1samp
from scipy.stats import shapiro
from scipy.stats import kstest, normaltest


# Load the Excel file
file_path = r"C:\Users\eoyur\OneDrive - itu.edu.tr\research\homophily-paper\tests\transfers.xlsx"
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe and the column names to understand the structure of the data
data.head(), data.columns



# Group the data by 'time' and calculate the mean of the 'given' column
average_given_per_time = data.groupby('time')['given'].mean()

# Plotting the graph
plt.figure(figsize=(10, 6))
average_given_per_time.plot(kind='line', marker='o', color='b', linestyle='-')
plt.title('Average Transfer Levels in Pension Games')
plt.xlabel('Time')
plt.ylabel('Average Transfers')
plt.grid(True)
plt.show()


# Dropping NaN values as Wilcoxon test can't handle them
given_clean = data['given'].dropna()

# Perform the Wilcoxon signed-rank test assuming the median should be 0 (for non-parametric)
w_stat, w_p_value = wilcoxon(given_clean - 0)

print(w_stat, w_p_value)


# Performing a one-sample t-test against the hypothesis that the mean is zero(for parametric)
t_stat, p_value = ttest_1samp(given_clean, 0)

print(t_stat, p_value)


# to test of parametric or non-parametric
# Applying the Shapiro-Wilk test for normality 
shapiro_stat, shapiro_p = shapiro(given_clean)

shapiro_stat, shapiro_p

# Perform Kolmogorov-Smirnov test (comparing against a normal distribution)
ks_stat, ks_p = kstest(given_clean, 'norm', args=(given_clean.mean(), given_clean.std()))

# Perform D'Agostino's K-squared test
dagostino_stat, dagostino_p = normaltest(given_clean)

ks_stat, ks_p, dagostino_stat, dagostino_p


