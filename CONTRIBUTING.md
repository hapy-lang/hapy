# working on hapy and as a team:

## Source Control (Git)

this will be quick and short before i write a more elaborate kini:

-	First things first is to clone the repo into a suitable folder
	```git
		git clone [repo address]
	```
-	If you are working on anything new, checkout to the develop branch `develop`
	```language
		git checkout develop
	```
	Pull the latest changes from remote
	```git
		git pull
	```
	then create a new branch using the latest changes from `develop`
	```git
		git checkout -b	[branch name] (see branch names for more)
	```

-	After making changes, commit your work and give it a concise descriptive msg
	```git
		git add . // add all changes to be staged (ready to commit)
		git commit -m "your msg goes here"
	```

	Then push your new branch to the remote repo:
	```git

		git push -u origin [branch name]
	```

	For the first time tho, subsequently to update the remote branch you'll just do `git push`

	-----

	### Working on Hapy:

	The repository has 3 sections, hapy source code, scripts and tests. 

	- /hapy folder contains the source code for the programming language, this is where you can find the parser and transpiler.

	- /scripts has the necessary build scripts to bundle Hapy as a Pip package.

	- /tests is where we write our tests. We use unittest.


	We use Python 3 and pips virtualenv.

	Install all packages using `pip install -r requirements.txt` from the root folder.

	To run the tests, run `python -m unittest` from the root folder.

	To execute a file run `python -m hapy.[file name]`

	To explain the different main files such as the Parser, Input Stream and Transpiler you can consult the [Lisp Language Tutorial](https://lisperator.net/pltut/)



Some resources:

This will outline the git workflow for development based on best practices and experience.

* [Git branching conventions](https://gist.github.com/digitaljhelms/4287848)
* [Semantic Git commits (article)](https://hackwild.com/article/semantic-git-commits/)
* [Commit message style by Karma](http://karma-runner.github.io/0.10/dev/git-commit-msg.html)
* [Working with issues in Gitlab](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html)
* [Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
* [Tips to enhance **GitHub** workflow](https://hackernoon.com/15-tips-to-enhance-your-github-flow-6af7ceb0d8a3)

## Code Editors and Formatting

There's an `.editorconfig` file at the root with some defaults.

I (@LeanKhan) started with Sublime Text as the editor because it was light. But you can use anyone. I use these extensions so maybe find something similar:

- Yapf for code formatting
- PyYapf Sublime Plugin
- Factor8 plugin and Sublime extension
- Anaconda Sublime Extension though I haven't got it working properly

I followed this article for setting up Sublime Text for Python https://karansthr.gitlab.io/fosstack/setup-sublime-python/index.html

On VSCode, I use these extensions:

- ms-python.vscode-pylance
- ms-python.python
