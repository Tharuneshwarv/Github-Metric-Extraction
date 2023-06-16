import requests
import json
import itertools
import csv

git_url = [
"https://api.github.com/repos/{owner}/{repo}/commits",
"https://api.github.com/repos/{owner}/{repo}/commits"
]

def key_func(k):
    return k['name'].lower()

token = "add_your_token"
username = "add_your_username"

commit_status_by_repo = []
for url in git_url:
	lang = url.replace("/commits","/languages")
	print('Querying: ', url)
	commit_by_user_raw = []
	commit_by_user = {}
	commit_by_user_date_wise = []
	res = requests.get(url, auth=(username, token))

	if res.status_code == 200:
		lan_res = requests.get(lang, auth=(username, token))
		lang_used = []
		if lan_res.status_code == 200:
			lan_res = json.loads(lan_res.text)
			for l in lan_res:
				lang_used.append(l)
		res = json.loads(res.text)

		for res_uni in res:
			commit_by_user_raw.append(res_uni['commit']['author'])

		commit_by_user_raw = sorted(commit_by_user_raw, key=key_func)
		for key, value in itertools.groupby(commit_by_user_raw, key_func):
			commit_by_user[key] =  list(value)

		for key in commit_by_user:
			date_arr = {}
			date = commit_by_user[key]
			each_date = []
			email = date[0]['email']

			for each_commit in date:
				date1 = each_commit['date'].split('T')[0]
				if date1 in date_arr.keys():
					date_arr[date1] = date_arr.get(date1) + 1
				else:
					date_arr[date1] = 1

			for d in date_arr:
				each_date.append([key, email, d, date_arr[d], lang_used])
				# [name, email, date, no.of commits, language_used]

			file = open('commits_language.csv', 'a', newline ='')
			with file:
				write = csv.writer(file)
				write.writerows(each_date)
			file.close()

			commit_by_user_date_wise.append({key: date_arr})
		commit_status_by_repo.append({
			url: commit_by_user_date_wise
		})
	else:
		print ('Unable to fetch : ', url)