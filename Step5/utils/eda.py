#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:11:18 2020
"""

from scipy import stats
import datascience.util as dt, datascience.tables as dtt, matplotlib.pyplot as plt, numpy as np, pandas as pd, statsmodels.api as sm 

plt.rcParams.update({'figure.max_open_warning': 0})

def display_boxplot(data, column, flag_log, flag_proportion, path):
    print('\n', column, 'box-plot') 
    fig, ax = plt.subplots()
    # Create the boxplot and store the resulting python dictionary
    box = ax.boxplot(data[column], showfliers = True, labels = ' ', meanline = True, showmeans = True)
    if (flag_log):
        plt.yscale('symlog')
    # Call the function to make labels
    make_labels(ax, box, flag_proportion)    
    plt.grid(True, axis = 'y')
    display_ylabel(switcher, column)
    plt.savefig(path + column + '_boxplot.svg', dpi = 300, bbox_inches = 'tight', transparent = True, format = 'svg')
    plt.show()    
    return

def display_boxplot_by_column(data, column, column_by, flag_log, flag_proportion, path):    
    print('\n', column, 'box-plot') 
    data.boxplot(column, by = column_by, showfliers = True, meanline = True, showmeans = True, return_type = 'both')
    if (flag_log):
        plt.yscale('symlog')
    plt.grid(b = None)
    plt.grid(True, axis = 'y')
    display_ylabel(switcher, column)
    display_xlabel(switcher, column_by)
    plt.title('')
    plt.suptitle('')
    #plt.errorbar(data[column], yerr=np.std(data[column], axis=0))
    plt.savefig(path + column + '_boxplot.png', dpi = 300, bbox_inches = 'tight', transparent = True)
    plt.show()    
    return

def display_column_date(data, column):
    print('\nDataset\'s column:', column, 'by date')
    print(data[column].describe())
    print('\nDataset\'s column:', column, 'by year')
    print(data[column].dt.year.describe().apply("{0:.0f}".format))
    print('\nDataset\'s column', column, 'mode:')
    print(data[column].dt.year.mode())              
    return

def display_univariate_vis(data, path):          
    print('\nFeatures'+'\' magnitude and distribution')
    for column in data:             
            if (column == 'repo' or column == 'has_refactorings' or column == 'pr_labels'):
                print('\nDataset\'s column:', column)
                print(data[column].describe())
                print('\nNumber of observations by unique values of the column', column)
                print(data[column].value_counts())                                    
            if (column == 'created_at'):
                display_plot_date(data, path)                
                plt.cla()
            if (column == 'pr_title'):
                print('\nDataset\'s column:', column)
                print(data[column].describe())
                print('\nDuplicated dataset\'s column', column)
                print(data[data.duplicated(subset = [column])])   
            if (column == 'length_discussion' or column == 'n_sub_additions'):
                print('\nDataset\'s column:', column)
                print(data[column].describe())    
                display_mode(data, column)
                display_histogram(data, column, False, path)
                plt.cla()
                display_boxplot(data, column, True, False, path)
                plt.cla()
                display_probplot(data, column)
                display_qqplot(data, column)            
            if (column == 'n_sub_file_changes' or column == 'n_review_comments' or column == 'time_to_merge' or column == 'n_sub_deletions' or column == 'n_sub_commits' or column == 'n_refactorings'):            
                print('\nDataset\'s column:', column)
                print(data[column].describe())    
                display_mode(data, column)
                display_histogram(data, column, True, path)
                plt.cla()
                display_boxplot(data, column, True, False, path)
                plt.cla()
                display_probplot(data, column)
                display_qqplot(data, column)
            if (column == 'n_reviewers'):                         
                print('\nDataset\'s column:', column)
                print(data[column].describe())    
                display_mode(data, column)
                display_histogram(data, column, False, path)
                plt.cla()
                if (column == 'p_review_comments'):
                    display_boxplot(data, column, False, True, path)
                    plt.cla()
                else:
                    display_boxplot(data, column, False, False, path)
                    plt.cla()
                display_probplot(data, column)
                display_qqplot(data, column)             
    return


def display_histogram(data, column, flag_log, path):    
    print('\n', column, 'histogram')
    data[column].hist(bins = 'auto', color = "skyblue")   
    plt.grid(b = None)
    plt.grid(True, axis = 'y')
    display_xlabel(switcher, column)
    plt.ylabel('Frequency')
    plt.tight_layout()
    if (flag_log):
        plt.xscale('log')
    plt.savefig(path + column + '_histogram.svg', dpi = 300, bbox_inches = 'tight', transparent = True, format = 'svg')
    plt.show()                   
    return

def display_histogram_date(data, path, flag = None): #specific to created_at and merged_at columns
    data['created_at'].dt.year.hist(bins = 'auto', color = "red", alpha = 0.5, label = 'PRs created in')
    data['merged_at'].dt.year.hist(bins = 'auto', color = "skyblue", alpha = 0.5, label = 'PRs merged in')
    print('\n created_at and merged_at histogram')
    plt.grid(True, axis = 'y')
    #plt.xlabel('Year')            
    plt.legend()
    if (flag):
        plt.ylabel('Number of observations\n(PRs with refactorings)')
    elif (flag == False):
        plt.ylabel('Number of observations\n(PRs with no refactorings)')
    else:
        plt.ylabel('Frequency')
    plt.grid(b = None)
    plt.tight_layout()
    if (flag != None):
        plt.savefig(path + str(flag) + '_created_and_merged_histogram.png', dpi = 300, bbox_inches = 'tight', transparent = True)
    plt.show()       
    return

def display_mode(data, column):
    print('\nDataset\'s column', column, 'mode:')
    print(data[column].mode())     
    return

def display_plot_date(data, path, flag = None):    
    display_column_date(data, 'created_at')
    display_column_date(data, 'merged_at')
    display_histogram_date(data, path, flag)          
    return

def display_probplot(data, column):    
    stats.probplot(data[column], dist="norm", plot = plt)
    plt.show()
    return

def display_qqplot(data, column):
    print('\n', column, 'qq-plot')    
    # the q-q plot compares the quantiles of our data against the quantiles of the desired distribution (defaults to the normal distribution, but it can be other distributions too as long as we supply the proper quantiles)
    sm.qqplot(data[column], line = '45')
    #plt.savefig(dir_name + 'cluster' + str(cluster) + '_' + column + '_qqplot.png', dpi = 300, bbox_inches = 'tight', transparent = True)
    plt.show()    
    return

def display_xlabel(switcher, column):  
    plt.xlabel(switcher.get(column, "Invalid argument"))
    return

def display_ylabel(switcher, column):  
    plt.ylabel(switcher.get(column, "Invalid argument"))
    return

def make_labels(ax, boxplot, flag_proportion):
    # Adapted from https://stackoverflow.com/questions/55648729/python-how-to-print-the-box-whiskers-and-outlier-values-in-box-and-whisker-plo    
    # Grab the relevant Line2D instances from the boxplot dictionary
    iqr = boxplot['boxes'][0]
    caps = boxplot['caps']
    med = boxplot['medians'][0]
    fly = boxplot['fliers'][0]
    # The x position of the median line
    xpos = med.get_xdata()
    # Lets make the text have a horizontal offset which is some 
    # fraction of the width of the box
    xoff = 0.1 * (xpos[1] - xpos[0])
    # The x position of the labels
    xlabel = xpos[1] + xoff
    # The median is the y-position of the median line
    median = med.get_ydata()[1]
    # The 25th and 75th percentiles are found from the
    # top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()
    # The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]
    
    
    # Make some labels on the figure using the values derived above
    if (flag_proportion):
        ax.text(xlabel, median,
            '{:.2f}'.format(median), va='baseline')
        ax.text(xlabel, pc25,
                '{:.2f}'.format(pc25), va='baseline')
        ax.text(xlabel, pc75,
                '{:.2f}'.format(pc75), va='baseline')
        ax.text(xlabel, capbottom,
                '{:.2f}'.format(capbottom), va='baseline')
        ax.text(xlabel, captop,
                '{:.2f}'.format(captop), va='baseline')            
    else:
        ax.text(xlabel, median,
                '{:.0f}'.format(median), va='baseline')
        ax.text(xlabel, pc25,
                '{:.0f}'.format(pc25), va='baseline')
        ax.text(xlabel, pc75,
                '{:.0f}'.format(pc75), va='baseline')
        ax.text(xlabel, capbottom,
                '{:.0f}'.format(capbottom), va='baseline')
        ax.text(xlabel, captop,
                '{:.0f}'.format(captop), va='baseline')    
        # create a label for the biggest outlier
        ax.text(1.08 + xoff, np.amax(fly.get_ydata()), '{:.0f}'.format(np.amax(fly.get_ydata())), va='baseline')    
    return

def bootstrap_proportion(original_sample, label, replications):
# Source: https://www.inferentialthinking.com/chapters/13/3/Confidence_Intervals.html    
    """Returns an array of bootstrapped sample proportions:
    original_sample: table containing the original sample
    label: label of column containing the Boolean variable
    replications: number of bootstrap samples
    """    
    just_one_column = original_sample.select(label)
    proportions = dt.make_array()
    for i in np.arange(replications):
        bootstrap_sample = just_one_column.sample()        
        resample_array = bootstrap_sample.column(0)
        resampled_proportion = np.count_nonzero(resample_array)/len(resample_array)
        proportions = np.append(proportions, resampled_proportion)        
    return proportions
  

switcher = {
        'has_refactorings': "Presence of refactoring edits",
        'n_changed_files': "Number of changed files (log)",
        'n_reviewers': "Number of reviewers",
        'length_discussion': "Length of discussion",
        'n_comments': "Number of comments",
        'n_review_comments': "Number of review comments (log)",
        'n_additions': "Number of added lines (log)",
        'n_deletions': "Number of deleted lines (log)",
        'n_commits': "Number of commits (log)",
        'n_refactorings': "Refactoring edits (log)",
        'churn': "Churn",
        'time_to_merge': "Time to merge in number of days (log)",
        'p_review_comments': "Proportion of review comments",
        'cluster_label': 'Cluster label',
        'n_refactoring_types': 'Number of refactoring types by pull request'
    }



################# STEP 1
# loading the dataset
#################

data = pd.read_csv('../input/output_ARL_at_apache.csv', engine = 'python', encoding = 'ISO-8859-1')
print('\nThere are', len(data), 'PRs in the dataset.')
# getting the dates as pandas datetime 
data['created_at'] = pd.to_datetime(data['created_at'])
data['merged_at'] = pd.to_datetime(data['merged_at'])
print('Dataset\'s informations')
data.info()

################# EDA
# description of data
# handlind outliers
# visualizing the dataset
#################
plt.rcParams.update({'font.size': 13})
data_true = data.loc[data['has_refactorings'] == True,:]
print('\n____________________________')
display_univariate_vis(data_true, './eda/true_')

data_false = data.loc[data['has_refactorings'] == False,:]
print('\n____________________________')
display_univariate_vis(data_false, './eda/false_')


#RQ1
display_univariate_vis(data, './eda/')

table_r = dtt.Table.read_table('../input/output_ARL_at_apache.csv')

refs = table_r.column('has_refactorings')
print(np.count_nonzero(refs)/len(refs))

# Generate the proportions from 5000 bootstrap samples
bstrap_props = bootstrap_proportion(table_r, 'has_refactorings', 5000)

# Get the endpoints of the 95% confidence interval
left = dt.percentile(2.5, bstrap_props)
right = dt.percentile(97.5, bstrap_props)  
print('95% CI:',dt.make_array(left, right))
