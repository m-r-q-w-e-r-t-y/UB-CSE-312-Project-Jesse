# Git Workflow

_How to commit code to the codebase and other git tricks_

The entire workflow can be summed up as follows:

1. Switch to `master` branch (`git checkout master`) and do `git pull` to get the latest updates.
2. While in the `master` branch, create a new branch for the specific issue you are working on, `git checkout -b <branch_name>` (the `-b` means "_Create a new branch if it doesn't exist and switch to it_").
3. The branch should deal with only the issue it is meant for and nothing else. If any other work is done other than the specific issue, deny the pull request (PR for short).
4. Once you have made the changes, stage the changes to be commited `git add . ` (adds all files, if you want to add only specifc files to be committed do `git add <filename>` instead), then commit the changes `git commit -m "Commit message"`, then push up the changes to Github `git push -u origin <branch_name>` (the `-u` is short for `--set-upstream` which pretty much means "_Put the local branch I have created up on Github_" oversimplified but it'll do; the `<branch_name>` is the name you want your branch to have up on Github, keep it the same name as the local branch).
5. Go to Github and you should see the new branch you just pushed. Switch to it on Github and press "Open Pull Request" and select other members to review the PR. If it's good and the branch gets merged into master, delete the branch on Github (should see a button on the bottom of the PR page) assuming you do not need it anymore.

### Other Git commands

- Get list of all branches: `git branch`.
- See changes that need to be committed: `git status`.
- We may run into other commands such as `reset`,`rebase`,`merge` and resolving merge conflicts but if you follow the workflow correctly we should never need these.
