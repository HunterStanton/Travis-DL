import requests
import sys
import time

def usage():
    print(r'''  _____             _        ___  _    
 |_   _| _ __ ___ _(_)______|   \| |   
   | || '_/ _` \ V / (_-<___| |) | |__ 
   |_||_| \__,_|\_/|_/__/   |___/|____|
                                       ''')
    print('Travis-DL - 2019 Hunter Stanton')
    print('\n')
    print('This script searches for repos belonging to a specific owner using the Travis-CI.org using the Travis-CI API and downloads all job logs for local archiving or analysis.')
    print('\n')
    print('Usage: '+ sys.argv[0] +' <travis-ci.org API token> <github username> <output dir>')
    print('Providing your Travis-CI.org auth token is optional.')
    print('\n')
    print('Please be mindful when using this script. Depending on the owner you\'re targeting, lots of requests could be made which could negatively impact Travis-CI.org. This script throttles requests by default to help alleviate this.')

# Make sure the user has entered an owner name
if len(sys.argv) is not 4:
    usage()
    quit()

headers = {
    'User-Agent': 'Travis-DL/0.1',
    'Authorizaion': 'token '+sys.argv[1],
    'Travis-API-Version': '3'
}

owner_url = 'https://api.travis-ci.org/owner/' + sys.argv[2] + '/repos?limit=100&offset=0&include=repository.current_build'

# Get the list of repositories belonging to the owner
owner_response = requests.get(owner_url, headers=headers)
time.sleep(1)


# Check the response codes
if owner_response.status_code == requests.codes['not_found']:
    print('The owner ' + sys.argv[2] + ' was not found! Please check that you provided the correct owner.')
    quit()

repos_data = owner_response.json()

print('Found ' + str(len(repos_data['repositories'])) + ' repositories from owner ' + sys.argv[2])

if len(repos_data['repositories']) is 0:
    print('No repositories found!')
    quit()

repo_ids = []
builds = 0
job_ids = []

# Grab the repo ID for every repo that includes a current build
for repo in repos_data['repositories']:
    if repo['current_build'] is not None:
        repo_ids.append(repo['id'])
    

print('Grabbing job IDs from repositories...')

# Parse repos and grab all job IDs from every build
for repo in repo_ids:
    repo_url = 'https://api.travis-ci.org/repo/' + str(repo) + '/builds?limit=25&offset=0'
    repo_response = requests.get(repo_url, headers=headers)
    time.sleep(1)
    repo_json = repo_response.json()
    builds = builds + len(repo_json['builds'])
    for build in repo_json['builds']:
        for job in build['jobs']:
            job_ids.append(job['id'])


# Check the number of builds
if builds is 0:
    print('No builds found. It\'s likely the owner you provided is not using Travis-CI.')
    exit()
elif builds is 1:
    print(str(builds) + ' build found in ' + str(len(repos_data['repositories'])) + ' repositories!')
elif builds > 1:
    print(str(builds) + ' builds found in ' + str(len(repos_data['repositories'])) + ' repositories!')

print('Downloading job logs...')

# Grab all job logs and write them to file
for job_id in job_ids:
    log_url = 'https://api.travis-ci.org/job/' + str(job_id) + '/log.txt'
    log_response = requests.get(log_url, headers=headers)
    time.sleep(1)
    logfile = open(sys.argv[3]+'/'+str(job_id)+'.txt', 'w+')
    logfile.write(log_response.text)
    logfile.close()

print('Download complete! All build logs have been downloaded and saved.')
    

