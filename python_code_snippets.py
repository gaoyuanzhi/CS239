#to get started
from github import Github

# XXX: Specify your own access token here

ACCESS_TOKEN = '10d7a57708edb441ed0a7237e0e8415dca4f6674' #github revokes token if we commit in public repo 
#replace above token with af5543ad0d765f74cc0b01609f8e756bf22cc397
# it removes even in comments zzzzzzzzzzzzz

# Specify a username and repository of interest for that user.

USER = 'ptwobrussell'
REPO = 'Mining-the-Social-Web'

client = Github(ACCESS_TOKEN, per_page=100)
user = client.get_user(USER)
repo = user.get_repo(REPO)

#get username and starred at
sg = repo.get_stargazers_with_dates()

#tr = repo.get_stargazers()

for s in sg:
    print(s.user,s.starred_at)
