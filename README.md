# Travis-DL
A Travis-CI.org build log bulk downloader. It can download all public build logs from a specific owner and save them to file as *job-id.txt*.

## Usage
travis-dl.py <travis-ci.org API token> <github username> <output dir>

Right now the script only supports Python 2.7.x. It does not work on Python 3, but I am going to add support for it soon.

While the script can work without providing an API token, it is best to provide one to ensure that your requests always succeed. You can grab your API token from [here](https://travis-ci.org/account/preferences).

## To-Do
There is a list of things I'd like to do to the script as right now it is in a very basic state. Here is a short list of a few things.

* Allow build log downloading for only a specific repository
* Add the option to output build logs into folders with the name of their repository
* Add a progress bar to show how long the process has until completion

## Known Issues
* If you attempt to set your output directory to a folder that does not exist, the script will fail.
