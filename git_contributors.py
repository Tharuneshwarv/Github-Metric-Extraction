import requests
import json
import itertools
import csv
from datetime import datetime
from termcolor import colored

git_url = [
"https://api.github.com/repos/{owner}/{repo}/stats/contributors",
"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
]

token = "add_your_token"
username = "add_your_username"

for url in git_url:
	res = requests.get(url, auth=(username, token))
	if res.status_code == 200:
		print('Querying: ', url)
		res = json.loads(res.text)
		for cont in res:
			name = cont['author']['login']
			res_mail = requests.get('https://api.github.com/users/'+name, auth=(username, token))
			if res_mail.status_code == 200:
				res_mail = json.loads(res_mail.text)
				res_email = res_mail['email']
				res_name = res_mail['name']
				# print(colored((res_name+'   YES'), 'green'))
				cont_by_user = [];
				if name != username:
					total_commit = cont['total']
					for each_week in cont['weeks']:
						w_ts = each_week["w"]
						w_ts = datetime.utcfromtimestamp(w_ts).strftime('%Y-%m-%d')
						a = each_week["a"]
						d = each_week["d"]
						c = each_week["c"]
						data = [name, res_name, res_email, total_commit, w_ts, a, d, c]
						cont_by_user.append(data)
					file = open('contributors.csv', 'a', newline ='')
					with file:
						write = csv.writer(file)
						write.writerows(cont_by_user)
					file.close()
			else:
				print(colored('NO', 'red'))
	else:
		print("Unable to reach: ", url)
