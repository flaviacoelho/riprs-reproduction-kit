#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 19:23:42 2021

"""

from github import Github, RateLimitExceededException
import pandas as pd, requests, time
import os.path, os
import datetime

duration = 2  # seconds
freq = 500  # Hz

def display_bar(filename = None):
    if (filename == None):
        print("\n____________________________________________________")
    else:
        print("\n____________________________________________________", file = filename)
    return

def query_composer(project, repo, commit):
    query = 'query{repository(owner:' + project +', name: ' + repo + ') {object(oid: ' + commit + ') {... on Commit {changedFiles additions deletions}}}}'
    return query
    
def repos_full_name_composer(project, repo):
    return project + '/' + repo

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


MAX_REQUESTS = 2
DELAY = 70
EXTRA_DELAY = 140

# GRAPHQL API v4
#   using an access token   
#################
access_token = 'your-access-token'
headers = {'Authorization': 'Bearer '+ access_token}

# REST API v3
#   using username and password
miner = Github("user", "password")

################# STEP 1
# preparing data
#################
display_bar()
data_rev = pd.read_csv('./input/input_reviewing_at_apache.csv', low_memory = False)
data_rev.drop_duplicates(keep = 'first', inplace = True)
print('\nThere are', len(data_rev), 'PRs, which have review comments, to be processed.')
print('\nColumns of our reviewing dataset:', list(data_rev.columns))

data_refs = pd.read_csv('./input/input_refactorings_at_apache.csv', low_memory = False)

# data_rev_output = pd.DataFrame(columns=['repo', 'pr_number', 'has_refactorings', 'n_changed_files',
#         'n_reviewers', 'length_discussion', 'n_comments', 'n_review_comments',
#         'n_additions', 'n_deletions', 'created_at', 'merged_at', 'pr_title',
#         'pr_labels', 'n_sub_commits', 'n_sub_file_changes', 'n_sub_additions',
#         'n_sub_deletions', 'n_refactorings', 'time_to_merge'])

data_rev_output = pd.read_csv('./output/output_reviewing_at_apache.csv', low_memory = False)

################# STEP 2
# Checking rebasing in our sample's subsequent PR commits
#################
project = 'apache'
display_bar()
count_requests = 0

for index_r, row in data_rev.iterrows():
    commit_merge_flag = False #rebasing
    print(datetime.datetime.now())
    print(row['repo'], row['pr_number'])
    repo_name = row['repo'][7:] #excluding substring apache/
    
    repo = miner.get_repo(repos_full_name_composer(project, repo_name))
    
    group_commits = data_refs[(data_refs['repo'] == row['repo']) & (data_refs['pr_number'] == row['pr_number'])].groupby(['commit'], sort = False)
    n_commits = len(group_commits)
    first = True
        
    for index, row_c in group_commits:    
        try:            
            if (row_c['initial_flag'].eq(True).all()): 
                continue
            
            if (first == True):
                count_requests = n_commits
                first = False                
                
            if (count_requests < MAX_REQUESTS):
                if (row_c['initial_flag'].eq(False).all()):                                            
                    parents = repo.get_commit(index).parents
                    if (len(parents) > 1):                        
                        commit_merge_flag = True
                        break
                
                if (first == False):
                    count_requests += 1
            else:
                count_requests = 0
                print('delaying...')
                time.sleep(DELAY)            
                        
        
        except RateLimitExceededException:
            print('GitHub API rate limit exceeded...')
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
            raise SystemExit()
    
    print('extra delaying...')
    time.sleep(EXTRA_DELAY)  
    
    if (commit_merge_flag == False):        
        repo_name = str(row['repo'])
        pr_number = int(row['pr_number'])
        print(repo_name + ' ' + str(pr_number) + ' did not suffer rebasing\n')
        index_pr = data_rev.loc[(data_rev['repo'] == repo_name) & (data_rev['pr_number'] == pr_number)].index.values
        data_rev_output = data_rev_output.append(data_rev.iloc[index_pr], ignore_index=True)
        data_rev_output.to_csv('./output/output_reviewing_at_apache.csv', index = False)    
    
# data_rev_output.to_csv('./output/output_reviewing_at_apache.csv', index = False)    
    
print('Mining finished')

    
