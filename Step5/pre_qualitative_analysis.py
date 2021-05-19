#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:23:11 2020

"""
import pandas as pd

def display_bar(filename = None):
    if (filename == None):
        print("\n____________________________________________________")
    else:
        print("\n____________________________________________________", file = filename)
    return

# preparing data for qualitative analysis
# This code should be run once

display_bar()
data_review = pd.read_csv('./input/output_ARL_at_apache.csv', engine = 'python', encoding = 'ISO-8859-1')
print('\nThere are', len(data_review), 'PRs, which have review comments, to be processed.')
print('\nThese are the columns of our original code review dataset:', list(data_review.columns))

display_bar()
data_review_comments = pd.read_csv('./input/input_review_comments_at_apache.csv', engine = 'python', encoding = 'ISO-8859-1')
data_review_comments.drop_duplicates(keep = 'first', inplace = True)
print('\nThere are', len(data_review_comments), 'review comments to be processed.')
print('\nThese are the columns of our original code review comments dataset:', list(data_review_comments.columns))

common = data_review.merge(data_review_comments,on=['repo','pr_number'])
print('\nThere are',len(common),'review comments in', len(common.groupby(['repo','pr_number'])), 'PRs.')
print('\nThese are the columns of our code review comments dataset:', list(common.columns))

display_bar()

print('The pre-processing finished')