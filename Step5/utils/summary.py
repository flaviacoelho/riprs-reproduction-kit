#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:01:22 2020
"""

import pandas as pd

def display_bar(filename = None):
    if (filename == None):
        print("\n____________________________________________________")
    else:
        print("\n____________________________________________________", file = filename)
    return


################# 
# Results 
#################

data = pd.read_csv('../input/output_ARL_at_apache.csv', engine = 'python', encoding = 'ISO-8859-1')
display_bar()
print('\nNumber of repositories:', len(data.groupby(['repo'])))  
print(data['repo'].describe())
print(data['repo'].value_counts())

print('\nNumber of labels:')
print(data['pr_labels'].describe())
print(data['pr_labels'].value_counts())

print('\nNumber of subsequent commits:', data['n_sub_commits'].sum())

print('\nNumber of refactoring edits:', data['n_refactorings'].sum())

display_bar()
print('\nRefactoring-inducing PRs')  
print(data['has_refactorings'].describe())
print(data['has_refactorings'].value_counts())

display_bar()
data_refs = pd.read_csv('../input/input_refactorings_at_apache.csv', engine = 'python', encoding = 'ISO-8859-1')
data_grouped = data_refs.groupby(['repo', 'pr_number'])
 
data['level'] = "" 
for pair_c, group_c in data_grouped:             
      levels = group_c.groupby(['refactoring_level'], sort = False)                
      result = ""
      for pair, group in levels:
        result = pair          
        break
      index_pr = data[(data['repo'] == pair_c[0]) & (data['pr_number'] == pair_c[1])].index        
      data.loc[index_pr, 'level'] = result
 
data_ref_commit = data.loc[data['level'] == "commit",:]
print(data_ref_commit)  
data_true_ref_commit = data.loc[(data['has_refactorings'] == True) & (data['level'] == "commit"),:]
print(data_true_ref_commit)  
print(len(data_ref_commit) * 100 /len(data), '% of squashed PRs in our sample')
print(len(data_true_ref_commit) * 100 /len(data.loc[data['has_refactorings'] == True,:]), '% of squashed PRs in RIPRs') 