# An Empirical Study on Refactoring-Inducing Pull Requests

## Reproduction kit

Following, we present the instructions for reproducing the exploratory study on [Apache](https://github.com/apache)'s refactoring-inducing pull requests in line with the research questions and design below.
You can also go along the links to get access to our results!

---
### *Research questions*
* RQ<sub>1</sub> How common are refactoring-inducing pull requests?
* RQ<sub>2</sub> How do refactoring-inducing pull requests compare to non-refactoring-inducing ones?
* RQ<sub>3</sub> Are refactoring edits induced by code reviews?

---
### *Research design*

#### Step 1. Mining merged pull requests
1. Search for Apache's non-archived Java repositories in [GitHub](https://github.com/search), by inputting *"user:apache language:java archived:false"* `We performed this search in August 2019`
1. Run the Python script [githubMinerPygithub](Step1/githubMinerPygithub.py)

The recovery of squashed commits from GitHub was built in lines 33-45, 126-130, 163-164. Aiming the strategy's effectiveness, we followed a few open pull requests up to the merge, such as the [apache/drill's pull request 1807](https://github.com/apache/drill/pull/1807), then we (1) ran the RefactoringMiner to detect refactorings in the commits from open pull requests; (2) executed the recovery strategy after the pull requests merge; (3) ran the RefactoringMiner in the recovered commits; and (4) compared the outputs from steps (1) and (3)
   * No input
   * Output:
      * [./data/](Step1/data) maintains repositories to pre-processing (needed to recover squashed and merged pull requests)
      * [./process/](Step1/process) stores the *commits dataset* and *pull requests dataset* - both structured in line with the input format required to run the refactoring detection, so containing records for the following variables:
         * (commits dataset) repository's URL, pull request number, and commit SHA; for example, (*https://www.github.com/apache/dubbo-admin.git, 481,  77579afb66e1a78eb491f0a783705d40484de5a7*); and
         * (pull requests dataset) repository's URL, and pull request number; for example, (*https://www.github.com/apache/dubbo-admin.git, 479*)
      * [./results/](Step1/results) registers the number of merged pull requests by repository

#### Step 2. Refactoring detection
* Run the [Java code](Step2/Main.java) for triggering the [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner) tool.
`Warning: This is a time-consuming task. If you have any problem, you should manually rerun the trigger and manage the output datasets.`
   * Input was preset as *commits dataset* and *pull requests dataset* (Step 1) - both available in [./data/](Step2/data))
   * Output:
      * [./results/](Step2/results) stores the following datasets:
         * [output_refactorings_at_apache_commits_level.csv](Step2/results/output_refactorings_at_apache_commits_level.zip)
         * [output_refactorings_at_apache_prs_level.csv](Step2/results/output_refactorings_at_apache_prs_level.zip)
      * The output datasets comprise these variables: repository's name, pull request number, commit(s) SHA, refactoring type(s), refactoring detail(s), and level; for example, (*apache/flink, 9595, 886419f12f60df803c9d757e381f201920a8061a, Rename Variable, table:Table to src:Table in method public testPartitionPrunning():void in class org.apache.flink.connectors.hive.HiveTableSourceTest, commit*). Level is a flag indicating the RefactoringMiner running level, that is, either commit level for squashed and merged pull requests or pull request level for non-squashed and merged pull requests.
   * Utils:
      * A Python script ([filesConcat](Step2/filesConcat.py)) for concatenating the output datasets, resulting in *detected refactorings dataset* - [output_refactorings_at_apache.csv](Step2/results/output_refactorings_at_apache.zip)

#### Step 3. Mining code review data 
* Run the Python script [githubReviewMinerPygithub](Step3/githubReviewMinerPygithub.py) for mining the code reviewing-related attributes listed below.

| Attribute            | Description                                     |
|----------------------|-------------------------------------------------|
| number               | Numerical identifier of a pull request          |
| title                | Title of a pull request                         |
| repository           | Repository's name of a pull request             |
| labels               | Labels associated with a pull request           |
| commits              | Number of subsequent commits in a pull request  |
| additions            | Number of added lines in a pull request         |
| deletions            | Number of deleted lines in a pull request       |
| file changes         | Number of file changes in a pull request        |
| creation date        | Date and time of a pull request creation        |
| merge date           | Date and time of a pull request merge           |
| review comments      | Number of review comments in a pull request     |
| non-review comments  | Number of non-review comments in a pull request |
| review comments text | The review comments of a pull request           |

`Specifically, our implementation meets this precondition: we mine only merged pull requests, comprising at least one review comment, since we investigated code reviewing-related aspects in the context of refactoring-inducing pull requests.`

   * Input was preset as *detected refactorings dataset* (Step 2) - available in [./data/](Step3/data)) 
   * Output:
      * *Code review dataset* - [refactorings_at_apache_output_review.csv](Step3/results/refactorings_at_apache_output_review.csv)
      * *Code review comments dataset* - [refactorings_at_apache_output_review_comments.csv](Step3/results/refactorings_at_apache_output_review_comments.zip)
   * Utils:
      * A Python script ([datasetsOrganizer](Step3/datasetsOrganizer.py)) for cleaning the output datasets (checking for mirrored repositories, duplicates, and unexpected faults such as zero reviewers), resulting in [output_apache_refactorings_review.csv](Step3/results/output_apache_refactorings_review.csv) and [output_apache_refactorings_review_comments.csv](Step3/results/output_apache_refactorings_review_comments.zip). 
      * A Python script ([githubMinerAuthoredData](Step3/githubMinerAuthoredData.py)) for marking the initial commits in the complete refactorings dataset, resulting in [output_final_refactorings_at_apache.csv](Step3/results/output_final_refactorings_at_apache.zip)
      * A Python script ([githubMinerCommitsData](Step3/githubMinerCommitsData.py)) for mining the number of file changes, line additions, and line deletions in subsequent commits of our sample, resulting in an updated *code review dataset* [output_reviewing_at_apache.csv](Step3/output/output_reviewing_at_apache.csv)
      

#### Step 4. Association rule learning
* Run the Python script [pre-arl](Step4/pre-ARL/pre_arl.py) for preparing data for ARL running.
  * Input was preset as *code review dataset* (Step 3) - available in [./pre-arl/input](Step4/pre-arl/input)
  * Output: 
      * updated *Code review dataset* - [output_pre_arl_at_apache.csv](Step4/pre-ARL/output/output_pre_arl_at_apache.csv)
  
* Run the Python script [arl](Step4/arl.py) for running the FP-growth algorithm on the following code reviewing-related features.

| Feature                                                                          |
|----------------------------------------------------------------------------------|
| number of subsequent commits                                                     |
| number of file changes                                                           |
| number of line additions                                                         |
| number of line deletions                                                         |
| number of reviewers                                                              |
| number of review comments                                                        |
| length of discussion = number of review comments + number of non-review comments |
| time to merge = merge date - creation date                                       |
| number of detected refactorings                                                  |


We applied one-hot encoding for binning of features, as described below.

| Category   | Range                       |
|------------|-----------------------------|
| None       | 0                           |
| Low        | 0 < quantile  &lt;= 0.25    |
| Medium     | 0.25 < quantile  &lt;= 0.50 |
| High       | 0.50 < quantile  &lt;= 0.75 |
| Very high  | 0.75 < quantile  &lt;= 1.0  |
      
   * Input was preset as *code review dataset* (Step 4 - pre-ARL) - available in [./input/](Step4/input)
   * Output:
      * Association rules[output_ARL_at_apache.txt](Step4/output/output_ARL_at_apache.txt)
      * *Code review dataset* - [output_ARL_at_apache.csv](Step4/output/output_ARL_at_apache.csv)

#### Step 5. Data analysis
* Run the Python script [statistical_tests](Step5/statistical_tests.py) for running these statistical tests: checking for data normality through Shapiro-Wilk test; checking for homogeneity of variances via Levene's test; computation of confidence interval for the difference in mean or median, based on the output from previous phases; and performing of non-parametric Mann Whitney U test and *Common-Language Effect Size* (CLES)

   * Input was preset as *code review dataset* (Step 4) - available in [./input/](Step5/input)
   * No output (the results are displayed on the console)
   
* Utils:
  * Python scripts ([summary](Step5/utils/summary.py)) and ([eda](Step5/utils/eda.py)) for summarizing the output dataset
  
  

