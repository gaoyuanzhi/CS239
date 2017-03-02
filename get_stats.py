from github import Github
import datetime
import requests
import json
import conf
from collections import defaultdict

def bucketize_dates(list_of_dates):
	dates = defaultdict(int)
	for d in list_of_dates:
		yearMonth,day = str(d).rsplit("-",1)
		dates[yearMonth]+=1
	return dates

ACCESS_TOKEN = conf.access_token
USER = 'freeCodeCamp'
client = Github(ACCESS_TOKEN, per_page=100)


# x = client.get_repo('freeCodeCamp/freeCodeCamp')
# x = client.get_repo('kamranahmedse/design-patterns-for-humans')
x = client.get_repo('freeCodeCamp/caption-dashboard')

# pulls
prs = x.get_pulls()
pr_count = 0
for pr in prs:
	pr_count +=1

print '{}:\n \t stars: {} \n\t forks: {} \n\t pulls: {}' .format(x.name,x.stargazers_count,x.forks_count,pr_count)

# stars over time
list_star_dates = []
stargazers = x.get_stargazers_with_dates()
for s in stargazers:
	list_star_dates.append(s.starred_at)
stars_over_time = bucketize_dates(list_star_dates)
print stars_over_time


# forks over time
forks = x.get_forks()
list_fork_dates = []
dates = defaultdict(int)
for f in forks:
	list_fork_dates.append(f.created_at)
forks_over_time = bucketize_dates(list_fork_dates)
print forks_over_time

# commits over time
date = datetime.datetime(2015,2,15)
commits_over_time = defaultdict(lambda: [0,0,0])
for commit in x.get_commits(since=date):
	num_files_changed = len(commit.files)
	timestamp = commit.commit.author.date
	yearMonth,day = str(timestamp).rsplit("-",1)
	additions = commit.stats.additions
	deletions = commit.stats.deletions
	commits_over_time[yearMonth][0]+=num_files_changed
	commits_over_time[yearMonth][1]+=additions
	commits_over_time[yearMonth][2]+=deletions

	# print "date: {} , files changed: {} , additions: {} , deletions: {}".format(timestamp,num_files_changed,additions,deletions)
print commits_over_time

