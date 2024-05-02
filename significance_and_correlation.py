# -*- coding: utf-8 -*-
"""
Created on Thu May  2 01:02:24 2024

@author: eoyur
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from scipy.stats import ttest_1samp
from scipy.stats import shapiro
from scipy.stats import kstest, normaltest
from scipy.stats import spearmanr
import seaborn as sns
from scipy.stats import kruskal


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
plt.title('Comparison of Average Transfer Levels in Poverty and Pension Games')
plt.xlabel('Time')
plt.ylabel('Average Transfers')
plt.grid(True)
plt.show()




# Drop rows with missing values in 'given' or 'received'
data_clean = data.dropna(subset=['given', 'received', 'expect'])


# to test of parametric or non-parametric
# Applying the Shapiro-Wilk test for normality 
shapiro_stat, shapiro_p_value = shapiro(data_clean['given'])
shapiro_stat, shapiro_p_value

# Perform Kolmogorov-Smirnov test (comparing against a normal distribution)
ks_stat, ks_p_value = kstest(data_clean['given'], 'norm', args=(data_clean['given'].mean(), data_clean['given'].std()))

# Perform D'Agostino's K-squared test
dagostino_stat, dagostino_p_value = normaltest(data_clean['given'])
dagostino_stat, dagostino_p_value


# to test if the values  significantly differ from one values (in this case is zero)
# Perform the Wilcoxon signed-rank test assuming the median should be 0 (for non-parametric)
wilcoxon_stat, wilcoxon_p_value = wilcoxon(data_clean['given'] - 0)
print(wilcoxon_stat, wilcoxon_p_value)

# Performing a one-sample t-test against the hypothesis that the mean is zero(for parametric)
t_stat, t_p_value = ttest_1samp(data_clean['given'], 0)
print(t_stat, t_p_value)






# Calculate mean of 'given' and 'received'
mean_given = data_clean['given'].mean()
mean_received = data_clean['received'].mean()
mean_expect = data_clean['expect'].mean()
mean_given, mean_received, mean_expect

# Calculate Spearman's rank correlation coefficient and the p-value
spearman_correlation, spearman_p_value = spearmanr(data_clean['given'], data_clean['received'])
spearman_correlation, spearman_p_value



# Split the cleaned data based on different treatments
treatment_groups = data_clean['Treatment'].unique()

# Calculate mean values for 'given' and 'received' for each treatment group
mean_values = {}
for treatment in treatment_groups:
    subgroup = data_clean[data_clean['Treatment'] == treatment]
    mean_given = subgroup['given'].mean()
    mean_received = subgroup['received'].mean()
    mean_values[treatment] = {'mean_given': mean_given, 'mean_received': mean_received}
print(mean_values)

# Calculate Spearman's rank correlation for each treatment group and gather results
spearman_correlation_results = {}
for treatment in treatment_groups:
    subgroup = data_clean[data_clean['Treatment'] == treatment]
    correlation_test = spearmanr(subgroup['given'], subgroup['received'])
    spearman_correlation_results[treatment] = {
        'correlation_coefficient': correlation_test.correlation,
        'p_value': correlation_test.pvalue
    }
print(spearman_correlation_results)



# Calculate mean transfers for each 'firstrole' within each treatment group
grouped_data = data_clean.groupby(['Treatment', 'firstrole']).mean().reset_index()

# Prepare the plot
plt.figure(figsize=(12, 8))
sns.lineplot(data=grouped_data, x='firstrole', y='given', hue='Treatment', marker='o', palette='tab10', style='Treatment')

# Enhance the plot
plt.title('Comparison of average transfers in pension game by players in different positions')
plt.xlabel('First Role')
plt.ylabel('Average Transfers')
plt.legend(title='Treatment', title_fontsize='13', fontsize='11')
plt.grid(True)

# Show the plot
plt.show()




# Calculate mean 'given' for each 'firstrole'
mean_given_by_role = data_clean.groupby('firstrole')['given'].mean().reset_index()
mean_given_by_role


# Filter out rows where 'given' is NaN and exclude 'firstrole' 1
filtered_data = data[data['given'].notna() & (data['firstrole'] != 1)]

# Perform Kruskal-Wallis test
kw_stat, kw_p_value = kruskal(*[group['given'].values for _, group in filtered_data.groupby('firstrole')])
kw_stat, kw_p_value


# Calculate mean 'given' for each 'first role' by treatment, excluding 'firstrole' 1
mean_given_by_treatment_role = filtered_data[filtered_data['firstrole'] != 1].groupby(['Treatment', 'firstrole'])['given'].mean().unstack()
mean_given_by_treatment_role

# Create subsets based on treatments and perform the Kruskal-Wallis test for each
kw_treatment_results = {}
for treatment, group_data in filtered_data.groupby('Treatment'):
    # Exclude 'firstrole' 1 as it has no data
    group_data = group_data[group_data['firstrole'] != 1]
    if not group_data.empty:
        stat, p_val = kruskal(*[role_group['given'].values for _, role_group in group_data.groupby('firstrole')])
        kw_treatment_results[treatment] = (stat, p_val)
kw_treatment_results






# Calculate Spearman's rank correlation for each 'first role'
s_correlation_results = []
for role in sorted(data['firstrole'].unique()):
    role_data = data[data['firstrole'] == role]
    # Ensure we have enough data points for correlation calculation
    if len(role_data['given'].dropna()) > 1 and len(role_data['received'].dropna()) > 1:
        s_correlation, s_p_value = spearmanr(role_data['given'].dropna(), role_data['received'].dropna(), nan_policy='omit')
        s_correlation_results.append({'First Role': role, 'Spearman Correlation': s_correlation, 'P-Value': s_p_value})
    else:
        s_correlation_results.append({'First Role': role, 'Spearman Correlation': np.nan, 'P-Value': np.nan})

# Convert results into a DataFrame for better visualization
s_correlation_df = pd.DataFrame(s_correlation_results)
s_correlation_df




# Spearman's rank correlation on expectation
s_correlation_exp, s_p_value_exp = spearmanr(data_clean['given'], data_clean['expect'])
s_correlation_exp, s_p_value_exp


# Group by the 'Treatment' column and recalculate Spearman's rank correlation and means for each group
treatment_results = []

# Iterate over each group after grouping by 'Treatment'
for name, group in data_clean.groupby('Treatment'):
    # Drop any additional NaN values that might exist within the group
    group = group.dropna(subset=['given', 'expect'])
    
    # Calculate Spearman's rank correlation for the group
    correlation, p_value = spearmanr(group['given'], group['expect'])
    
    # Calculate means for the group
    mean_given = group['given'].mean()
    mean_expect = group['expect'].mean()
    
    # Append results for this treatment group
    treatment_results.append({
        'Treatment': name,
        'Spearman Correlation': correlation,
        'P-value': p_value,
        'Mean Given': mean_given,
        'Mean Expect': mean_expect
    })
treatment_results

