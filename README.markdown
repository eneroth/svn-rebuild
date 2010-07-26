SVN-Rebuild
===

SVN-Rebuild is designed to repair, clean, and update SVN repositories situated as subfolders in a git project.

The Problem
---
As I migrated the main repository of a fairly large project to git recently, I realized how spoiled I'd been with SVN. I was used to being able to update my entire project, with dependencies, externals and all, with a single command: svn update. The project depends on other projects, with other repositories, which in turn depend on still more projects and so on. This is a hiearchy I could largely ignore, as SVN would integrate them seemlessly for me. Unfortunately, git didn't turn out to be as forgiving.
At first, I tried to migrate the sub-projects to git repositories, but that turned out to be a logistics nightmare. I would have to keep numerous SVN repositories turned git up to date locally, and what would happen if they suddenly changed their internal structure? Then I'd have to move the submodules around and whatnot.
Yet I wanted to use git, so I thought the solution would be easy: just check out the SVN repos I need straight into the project and then commit them along with everything else to the git repo.
Unfortunately, it turns out that git doesn't actually take a *snapshot* of the project in the same sense that SVN does. It'll modify the project slightly to fit its own structure. I'm specifically thinking of the inability to store empty folders. SVN needs those empty folders.

The solution
---
A script that automatically finds all SVN directiories under the current directory, rebuilds all empty folders that git has stripped, and then updates them.

Usage
---
Example:
	$ python3 svn-rebuild.py
  
As part of other script:
	#!/bin/bash
	git pull
	
	python3 svn-rebuild.py
  
	./symfony cc
	./symfony project:optimize frontend