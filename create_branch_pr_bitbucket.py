import requests
from requests.auth import HTTPBasicAuth
import os

password = 'zefkyv-cohvi7-suwgoV'
url = 'http://10.128.93.47:7990/rest/api/1.0/projects/TEAM/repos/multiplepr/'
headers = {
    "Content-Type": "application/json"
}


def create_branch_commit_pr(index):
    file_name = str(index) + '_file.txt'
    branch_name = 'feature_' + str(index)

    with open(file_name, 'w') as f:
        f.write(str(index))
    files = {'content': open(file_name, 'rb')}
    form_data = {"branch": branch_name, "sourceBranch": "master"}

    r = requests.put(url + 'browse/src/' + file_name, data=form_data, files=files,
                     auth=HTTPBasicAuth(username='tc-qa', password=password))

    if os.path.exists(file_name):
        os.remove(file_name)
    if r.status_code == 200:
        pr_data = {"title": "Pull Request " + str(index), "fromRef": {"id": "refs/heads/" + branch_name},
                   "toRef": {"id": "refs/heads/master"}}
        r = requests.post(url + 'pull-requests', headers=headers, json=pr_data, auth=HTTPBasicAuth(username='tc-qa',
                                                                                                   password=password))


if __name__ == '__main__':
    start = 4
    count = 150
    for i in range(start, count):
        create_branch_commit_pr(i)
