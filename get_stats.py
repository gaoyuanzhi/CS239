from github import Github
from collections import defaultdict
import datetime
import conf

class Repo:
	def __init__(self,repo):
		self.repo = repo
		self.name = repo.name
		self.stargazers_count = repo.stargazers_count
		self.forks_count = repo.forks_count
	def get_repo_stats(self):
		"""
		repo is a PyGitHub Repository Object
		return:
			number of pulls
			stars over time
			forks over time
			change stats over time
				dict of month:[files,additions,deletions]
		"""
		self.num_pr = self.get_num_pr()
		self.stars_over_time = self.get_stars_over_time()
		self.forks_over_time = self.get_forks_over_time()
		self.change_stats_over_time = self.get_change_stats_over_time()

	def bucketize_dates(self, list_of_dates):
		dates = defaultdict(int)
		for d in list_of_dates:
			yearMonth,day = str(d).rsplit("-",1)
			dates[yearMonth]+=1
		return dates

	def get_num_pr(self):
		prs = self.repo.get_pulls()
		count = 0
		for pr in prs:
			count+=1
		return count

	def get_stars_over_time(self):
		list_star_dates = []
		stargazers = self.repo.get_stargazers_with_dates()
		for s in stargazers:
			list_star_dates.append(s.starred_at)
		stars_over_time = self.bucketize_dates(list_star_dates)
		return stars_over_time

	def get_forks_over_time(self):
		forks = self.repo.get_forks()
		list_fork_dates = []
		dates = defaultdict(int)
		for f in forks:
			list_fork_dates.append(f.created_at)
		forks_over_time = self.bucketize_dates(list_fork_dates)
		return forks_over_time

	def get_change_stats_over_time(self):
		"""
		return a list of 3 values [files_changed,additions,deletions]
		"""
		# date = datetime.datetime(2015,2,15)
		changes_over_time = defaultdict(lambda: [0,0,0])
		for commit in self.repo.get_commits():
			num_files_changed = len(commit.files)
			timestamp = commit.commit.author.date
			yearMonth,day = str(timestamp).rsplit("-",1)
			additions = commit.stats.additions
			deletions = commit.stats.deletions
			changes_over_time[yearMonth][0]+=num_files_changed
			changes_over_time[yearMonth][1]+=additions
			changes_over_time[yearMonth][2]+=deletions
		return changes_over_time


if __name__ == '__main__':
	
	ACCESS_TOKEN = conf.access_token
	USER = 'freeCodeCamp'
	client = Github(ACCESS_TOKEN, per_page=100)

	# repo = client.get_repo('freeCodeCamp/freeCodeCamp')
	# repo = client.get_repo('kamranahmedse/design-patterns-for-humans')
	repo = client.get_repo('freeCodeCamp/caption-dashboard')

	r = Repo(repo)
	r.get_repo_stats()
	print '{}:\n \t stars: {} \n\t forks: {} \n\t pulls: {}' .format(r.name,r.stargazers_count,r.forks_count,r.num_pr)
	print r.stars_over_time
	print r.forks_over_time
	print r.change_stats_over_time
	