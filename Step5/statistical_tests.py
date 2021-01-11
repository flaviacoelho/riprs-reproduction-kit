
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 10:50:57 2020

"""

#Statistical tests 
import pandas as pd, scipy.stats as stats
import pingouin as pg, numpy as np

np.set_printoptions(formatter={'float': lambda x: '%.2f' % x})


def stats_tests_ripr(data):
        
    data_riprs = data.loc[data['has_refactorings'] == True]
    print('There are', len(data_riprs), 'RIPRs.')

    data_non_riprs = data.loc[data['has_refactorings'] == False]
    print('There are', len(data_non_riprs), 'non-RIPRs.')
    
    for c in data.columns:
        #if(c != 'has_refactorings'):
        if(c == 'time_to_merge'):
            print('_________________\nFeature:',c)
            prs_true = data_riprs.loc[:, c]
            prs_false = data_non_riprs.loc[:, c]
            
            print('\nChecking ANOVA assumptions')
            
            #Assumption 2. Checking for normalility
            print('\nAssumption 2. Checking for normality')            
            print('Shapiro-Wilk test - False', stats.shapiro(prs_false))
            print('Shapiro-Wilk test - True', stats.shapiro(prs_true))
            
            #Assumption 3. Checking for homogeneity of variances            
            print('\nAssumption 3. Checking for homogeneity of variances')            
            print('Levene test:',stats.levene(prs_true, prs_false))        
            
            print('\nComputing confidence interval for the difference')
            bootstrap_ci_median(data, c, 'has_refactorings')
            
                        
            # # performing Kruskal-Wallis (a nonparametric version of the one-way ANOVA)
            #if the null hypothesis is true, then in the long run the amount of favorable evidence is equal to the amount of unfavorable evidence. 
            # when the null is true, the expected value of the common language effect size is fifty percent
            print('Mann Whitney U test: (pingouin)', pg.mwu(prs_true, prs_false, tail='one-sided'))            
    return


def bootstrap_ci_median(df, variable, classes, repetitions = 1000, alpha = 0.05, random_state=None): 
    
    df = df[[variable, classes]]
    bootstrap_sample_size = len(df) 
    
    median_diffs = []
    for i in range(repetitions):
        bootstrap_sample = df.sample(n = bootstrap_sample_size, replace = True, random_state = random_state)
        median_diff = bootstrap_sample.groupby(classes).median().iloc[1,0] - bootstrap_sample.groupby(classes).median().iloc[0,0]
        median_diffs.append(median_diff)
    
    # confidence interval
    left = np.percentile(median_diffs, alpha/2*100)
    right = np.percentile(median_diffs, 100-alpha/2*100)
    
    # point estimate
    point_est = df.groupby(classes).median().iloc[1,0] - df.groupby(classes).median().iloc[0,0]
    print('Point estimate of difference between medians:', round(point_est,2))
    print((1-alpha)*100,'%','confidence interval for the difference between medians:', (round(left,2), round(right,2)))
    return



data = pd.read_csv('./input/output_ARL_at_apache.csv', engine = 'python', encoding = 'ISO-8859-1')   
data['churn'] = data['n_sub_additions'] + data['n_sub_deletions']
data = data[['has_refactorings','n_sub_commits', 'n_sub_file_changes', 'n_sub_additions', 'n_sub_deletions', 'churn', 'n_reviewers', 'n_review_comments', 'length_discussion', 'n_refactorings', 'time_to_merge']]    

print('\nThere are', len(data), 'PRs to be analyzed.')

stats_tests_ripr(data)
 
