from github import Github
from collections import defaultdict
import datetime
import conf
import json
import os



class Repo:
	def __init__(self,repo):
		self.repo = repo
		self.name = repo.name
		self.stargazers_count = repo.stargazers_count
		self.forks_count = repo.forks_count

	def is_documentation(self,filename):
		"""
		check if extension is 
		"""
		valid_extensions = {'.pdf':1, '.txt':1, '.md':1, '.jpg':1, '.png':1,'.ps':1,'.mp4':1}
		filename, file_extension = os.path.splitext(filename)
		if file_extension in valid_extensions:
			return True
		else:
			return False

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
		self.pulls_over_time = self.get_pulls_over_time()
		self.stars_over_time = self.get_stars_over_time()
		self.forks_over_time = self.get_forks_over_time()
		self.change_stats_over_time = self.get_change_stats_over_time()
		self.change_stats_over_time_method2 = self.get_change_stats_over_time_method2()

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

	def get_pulls_over_time(self):
		prs = self.repo.get_pulls()
		list_pull_dates = []
		dates = defaultdict(int)
		for p in prs:
			list_pull_dates.append(p.created_at)
		pulls_over_time = self.bucketize_dates(list_pull_dates)
		return pulls_over_time

	def get_stars_over_time(self):
		print "stars"
		list_star_dates = []
		stargazers = self.repo.get_stargazers_with_dates()
		for s in stargazers:
			list_star_dates.append(s.starred_at)
		stars_over_time = self.bucketize_dates(list_star_dates)
		return stars_over_time

	def get_forks_over_time(self):
		print "fork"
		forks = self.repo.get_forks()
		list_fork_dates = []
		dates = defaultdict(int)
		for f in forks:
			list_fork_dates.append(f.created_at)
		forks_over_time = self.bucketize_dates(list_fork_dates)
		return forks_over_time

	def get_issues_over_time(self):
		print "issues"
		issues = self.repo.get_issues()
		list_issues_dates = []
		for issue in issues:
			list_issues_dates.append(issues.created_at)
		issues_over_time = self.bucketize_dates(list_issues_dates)
		return issues_over_time

	# def get_change_stats_over_time(self):
	# 	"""
	# 	return a list of 3 values [files_changed,additions,deletions]
	# 	"""
	# 	# date = datetime.datetime(2015,2,15)
	# 	print "change"
	# 	changes_over_time = defaultdict(lambda: [0,0,0])
	# 	for commit in self.repo.get_commits():
	# 		num_files_changed = len(commit.files)
	# 		timestamp = commit.commit.author.date
	# 		yearMonth,day = str(timestamp).rsplit("-",1)
	# 		additions = commit.stats.additions
	# 		deletions = commit.stats.deletions
	# 		changes_over_time[yearMonth][0]+=num_files_changed
	# 		changes_over_time[yearMonth][1]+=additions
	# 		changes_over_time[yearMonth][2]+=deletions
	# 	return changes_over_time

	def get_watchers_over_time(self):
		list_watcher_dates = []
		watchers = self.repo.get_watchers()

	def get_change_stats_over_time(self):
		"""
		return a list of 3 values [files_changed,additions,deletions]
		"""
		# date = datetime.datetime(2015,2,15)
		changes_over_time = defaultdict(lambda: [0,0,0])
		for commit in self.repo.get_commits():
			for f in commit.files:
				if self.is_documentation(f.filename):
					timestamp = commit.commit.author.date
					yearMonth,day = str(timestamp).rsplit("-",1)

					changes_over_time[yearMonth][0]+=1
					changes_over_time[yearMonth][1]+=f.additions
					changes_over_time[yearMonth][2]+=f.deletions
		return changes_over_time


	
	def get_change_stats_over_time_method2(self):
		"""
		return time series and its corresponding readme lines
		the returned readme lines only reflex changes in readme, needs to be re-processed to get total size over time
		"""
		print "change-method2"
		changes_over_time_method2 = defaultdict(int)
		for commit in self.repo.get_commits():
			
			for each_file in commit.files:
				timestamp = commit.commit.author.date
				yearMonth,day = str(timestamp).rsplit("-",1)
				if each_file.filename == 'README.md':
						changes_over_time_method2[yearMonth] += each_file.additions - each_file.deletions

		
		return changes_over_time_method2


if __name__ == '__main__':
	
	ACCESS_TOKEN = conf.access_token
	client = Github(ACCESS_TOKEN, per_page=100)
	
	f = open('../../data/top10MLProjects.txt', "r")
	projects = f.readlines()
	f.close()
	projects = [x.strip() for x in projects]
	# print projects

	stats = []
	stats2 = []
	i = 0
	for project in projects:

		print "Project: {}".format(project)
		repo = client.get_repo(project)
		r = Repo(repo)
		r.get_repo_stats()
		stats = {project:[r.stars_over_time,r.forks_over_time,r.change_stats_over_time,r.pulls_over_time]}
		i += 1
		f = open('../../data/' + str(i) + '.json', "wr")
		f.write(json.dumps(stats))
		f.close()

		stats2 = {project:[r.change_stats_over_time_method2]}
		f = open('../../data/method2-on-dataset' + str(i) + '.json', "wr")
		f.write(json.dumps(stats2))
		f.close()


	
