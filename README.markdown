SVN-Rebuild
===

SVN-Rebuild is designed to repair, clean, and update SVN repositories situated as subfolders in a git project.

The Problem
---
When SVN projects are placed in a git project, empty folders inside the .svn folder disappear. 

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