# -*- coding: utf-8 -*-
"""
Created on Wed May  1 03:50:07 2024

@author: eoyur
"""

import pandas as pd 
from scipy.stats import chi2_contingency

# Load the dataset
data_path = r"C:\Users\eoyur\OneDrive - itu.edu.tr\research\homophily-paper\tests\descriptive_and_balance.xlsx"
data = pd.read_excel(data_path)
# Display the first few rows of the dataset to understand its structure
data.head(), data.columns


# Calculate descriptive statistics for the entire dataset
descriptive_stats = data.describe(include='all')
# Display the descriptive statistics
print(descriptive_stats)


def chi_square_test(data, variable):
    # Creating a contingency table of the variable against the treatment group
    contingency_table = pd.crosstab(data[variable], data['Treatment'])
    # Performing the Chi-square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return {"Variable": variable, "Chi-square Statistic": chi2, "p-value": p}


# List of all categorical variables including some that might be treated as ordinal
categorical_variables = ['gpa', 'dep', 'age', 'gender', 'education', 'income', 'h.income',
                         'envcons2', 'envcons3', 'envcons5', 'envcons6', 'envcons7', 'envcons9',
                         'fate', 'belief', 'riska']

# Perform Chi-square tests for all listed categorical variables
all_balance_tests = [chi_square_test(data, var) for var in categorical_variables]

# Convert results to DataFrame for better display
all_balance_test_results = pd.DataFrame(all_balance_tests)
print(all_balance_test_results)


# Function to perform Chi-square test for comparing two treatment groups
def chi_square_test_pair(data, variable, group1, group2):
    data_subset = data[data['Treatment'].isin([group1, group2])]
    contingency_table = pd.crosstab(data_subset[variable], data_subset['Treatment'])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return {"Variable": variable, "Comparison": f"{group1} vs {group2}", "Chi-square Statistic": chi2, "p-value": p}


# Treatment comparisons: Control (1) vs Created (2, 3, 4)
comparisons = [(1, 2), (1, 3), (1, 4)]

# Perform Chi-square tests for each pair of treatments
balance_test_pairs = []
for group1, group2 in comparisons:
    for variable in categorical_variables:
        balance_test_pairs.append(chi_square_test_pair(data, variable, group1, group2))

# Convert results to DataFrame for better display
balance_test_pairs_results = pd.DataFrame(balance_test_pairs)
balance_test_pairs_results.sort_values(by=['Variable', 'Comparison'])
