---
title: "A Practical Note for Git Commands"
author: qianhui
date: 2026-03-30 00:00:00 +0000
categories: [Configuration]
tags: [git]
render_with_liquid: false
---

## Commands for Starting a Working Area

#### Clone a repository
- if cloning into a new directory with the same name as the repository:
  ```shell
  user@host % git clone <repo_url>
  ```
- when inside an existing local directory `dir` and it is empty:
  ```shell
  user@host dir % git clone <repo_url> .
  ```
- when the local directory `dir` is not empty:
  ```shell
  user@host dir % git init
  user@host dir % git remote add origin <repo_url>
  user@host dir % git fetch origin # fetches all branches and tags from the remote repository
  user@host dir % git switch <remote_branch_name> # create a new local branch that tracks the remote branch
  ```  
- clone a specific branch or tag:
  ```shell
  user@host % git clone -b <branch/tag_name> <repo_url>
  ```
- clone and download history only for a specific branch:
  ```shell
  user@host % git clone --branch <branch_name> --single-branch <repo_url>
  ```
- clone with a specific depth (shallow clone):
  ```shell
  user@host % git clone --depth 1 <repo_url> # clones only the latest commit
  ```

## Commands for Working with Current Changes

#### Add file contents to the index
- Stage all changes for commit:
  ```shell
  user@host % git add .
  ```
- Stage specific files for commit:
  ```shell
  user@host % git add <file_path1> <file_path2> ...
  ```

#### Record changes in the working tree but go back to the clean state
- Stash the changes in a dirty working directory away
  ```shell
  user@host % git stash
  ```
- Stash the changes with a message:
  ```shell
  user@host % git stash push "Stash message"
  ```
- Unstash the changes and apply them to the working directory:
  ```shell
  user@host % git stash pop
  ```
- Unstash the changes and apply them to the working directory without removing them from the stash list:
  ```shell 
  user@host % git stash apply
  ```

#### Undoing changes in the working tree
- Discard changes in the working directory:
  ```shell
  user@host % git restore <file_path>
  ```
- Unstage changes from the index:
  ```shell
  user@host % git restore --staged <file_path>
  ```


#### Revert changes
- Revert changes introduced by a specific commit and create a new commit with the revert:
  ```shell
  user@host % git revert <commit_hash>
  ```
- Revert changes introduced by a specific commit without creating a new commit:
  ```shell
  user@host % git revert --no-commit <commit_hash>
  ```

#### Reset the current branch to a specific state
- Reset the current branch to a specific commit and keep changes in the working directory:
  ```shell
  user@host % git reset --soft <commit_hash>
  ```
- Reset the current branch to a specific commit and keep changes in the index:
  ```shell
  user@host % git reset --mixed <commit_hash>
  ```
- Reset the current branch to a specific commit and discard all changes in the working directory:
  ```shell  
  user@host % git reset --hard <commit_hash>
  ```




## Commands for Examining the History and State

#### View commit history
- View the commit history in a compact/full code change format:
  ```shell
  user@host % git log --oneline/-p
  ```
- View the commit history with a graph:
  ```shell
  user@host % git log --graph --oneline --all
  ```
- View the commit history for a specific file:
  ```shell
  user@host % git log -- <file_path>
  ```
- View the commit history in a file list format:
  ```shell
  user@host % git log --status/--name-only/--name-status
  ```
- View the commit history with a specific author:
  ```shell
  user@host % git log --author="<author_name>"
  ```
- View the commit history with a specific message:
  ```shell
  user@host % git log --grep="<search_term>"
  ```
- View the commit history with a specific date range:
  ```shell
  user@host % git log --since="2026-01-01" --until="2026-12-31"
  ```
- View the commit history with a specific branch/tag:
  ```shell
  user@host % git log <branch_name/tag_name>
  ```
- View the commit history with a specific number of commits:
  ```shell
  user@host % git log -n <number_of_commits>
  ```
- View the commit history with a specific format:
  ```shell
  user@host % git log --pretty=format:"%h - %an, %ar : %s"
  ``` 

#### View the current status of the repository
- View the current status of the repository:
  ```shell
  user@host % git status
  ```
- View the current branch:
  ```shell
  user@host % git branch
  ```
- View the current branch and its tracking remote branch:
  ```shell
  user@host % git branch -vv
  ```
- View the current commit hash:
  ```shell
  user@host % git rev-parse HEAD
  ```
- View the current commit with a specific format:
  ```shell
  user@host % git log -1 --pretty=format:"%h - %an, %ar : %s"
  ```

#### View the differences between commits or branches
- View the differences between the current branch and the master branch:
  ```shell
  user@host % git diff master
  ```
- View the differences between two branches:
  ```shell
  user@host % git diff <branch1> <branch2>
  ```
- View the differences between two commits:
  ```shell
  user@host % git diff <commit1> <commit2>
  ```
- View the differences for a specific file:
  ```shell
  user@host % git diff <commit1> <commit2> -- <file_path>
  ``` 
- View the differences with a specific format:
  ```shell
  user@host % git diff --stat/--name-only/--color/--word-diff/--compact-summary
  ```

#### Examine a specific state of the repository without being on a branch [DO NOT SAVE WORK HERE]
- Check out a specific commit and create a detached HEAD state:
  ```shell
  user@host % git switch --detach <commit_hash>
  ```



## Commands for Growing, Marking and Tweaking Common History
#### Create a new branch
- Create a new branch and switch to it:
  ```shell
  user@host % git switch -c <new_branch_name>
  ```
- Create a new branch from a specific commit or branch/tag:
  ```shell 
  user@host % git switch -c <new_branch_name> <commit_hash/branch_name/tag_name>
  ```
- Create an orphan branch (a branch with no history):
  ```shell
  user@host % git switch --orphan <new_branch_name>
  ```



#### Record changes to the repository
- Stage and commit all changes with a message:
  ```shell
  user@host % git commit -A "Commit message"
  ```
- Commit staged changes with a message:
  ```shell
  user@host % git commit -m "Commit message"
  ```
- Commit staged changes with a message and sign the commit:
  ```shell
  user@host % git commit -S -m "Commit message"
  ``` 
- Amend the previous commit with new changes and a new message:
  ```shell
  user@host % git commit --amend -m "New commit message"
  ```





#### Join development history together
- Merge a branch/commit into the current branch:
  ```shell
  user@host % git merge <branch_name/commit_hash>
  ```
- Merge remotely tracked branch into the current branch:
  ```shell
  user@host % git merge <remote_repo>/<branch_name>
  ```
- Apply a specific commit to the current branch:
  ```shell
  user@host % git cherry-pick <commit_hash>
  ```
- Rebase the branched-off commits of the current branch onto a new base tip:
  ```shell
  user@host % git rebase <branch_name/tag_name/commit_hash>
  ```


## Commands for Collaborating
#### Download objects and refs from remote or upstream repositories
- Unshallow clone and fetch all history:
  ```shell
  user@host % git fetch --unshallow
  ```
- Unshallow clone and fetch a specific branch:
  ```shell
  user@host % git fetch --unshallow origin <branch_name>
  ``` 
- Fetch all branches and tags from the remote repository:
  ```shell
  user@host % git fetch --all
  ```
- Fetch a specific branch/tag from the remote repository:
  ```shell
  user@host % git fetch origin <branch_name/tag_name>
  ```

#### Push commits to a remote repository
- Push the current branch to the remote repository and set the upstream tracking branch:
  ```shell
  user@host % git push -u origin <current_branch_name>
  ```
- Push a specific branch/tag to its remote tracking repository:
  ```shell
  user@host % git push origin <branch_name/tag_name>
  ```

#### Pull changes from a remote repository
- Pull changes from the remote repository and merge them into the current branch:
  ```shell
  user@host % git pull origin <current_branch_name>
  ```
- Pull changes from the remote repository and rebase them onto the current branch:
  ```shell
  user@host % git pull --rebase origin <current_branch_name>
  ```   

## Commands for Global Configuration
- Set the global username and email for commits:
  ```shell
  user@host % git config --global user.name "Your Name"
  user@host % git config --global user.email "Your Email"
  ```
- Set the global ignore file for untracked files:
  ```shell
  user@host % git config --global core.excludesfile <path_to_ignore_file>
  ```
- Set the global alias for a git command:
  ```shell
  user@host % git config --global alias.<alias_name> <git_command>
  ```
- Check the global configuration:
  ```shell  
  user@host % git config --global --list
  ```