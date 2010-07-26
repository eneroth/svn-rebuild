import sys
import os
from os.path import join, abspath, isdir, dirname, split, exists
from os import listdir, mkdir

# Finds SVN repositories under the given starting point
# returns as a dictionary, where the key is the base
# folder, and the values lists with all .svn folders
# under the base folder. All absolute paths.
# ---------------------------------------------------------
def findSvnRepos(folderToSearch):
  svnFolders      = {}
  foldersToSearch = [folderToSearch]
  
  while len(foldersToSearch):
    dirToCheck           = foldersToSearch[0]
    foldersToSearch[0:1] = []
    # Get subdirectories
    subDirs = [join(dirToCheck, subDir) for subDir in listdir(dirToCheck) if isdir(join(dirToCheck,subDir))]
    
    # Check if there's an .svn folder on this level. If there is, this folder is a 'parent'.
    if join(dirToCheck, ".svn") in subDirs:
      print("SVN repository found: ", split(dirToCheck)[1])
      tmpFolders = []
      
      # Find all .svn subfolders and add to temporary array
      for root, dirs, files in os.walk(dirToCheck):
        if '.svn' in dirs:
          tmpFolders.append(join(root,".svn"))
      
      # Associate all subfolders with parent
      svnFolders[dirToCheck] = tmpFolders
      
    else:
      # Add subfolders to list to be searched
      foldersToSearch.extend(subDirs)
  
  return svnFolders


# Formatting functions
# ---------------------------------------------------------
def getEscapeChars(inString):
  return '\b' * len(inString)

def getLeadingFiller(num, maxSize):
  numLength     = len(str(num))
  maxSizeLength = len(str(maxSize))
  return (' ' * (maxSizeLength - numLength))

def renderRepoCounter(num, maxSize):
  maxSizeString = str(maxSize)
  numString     = getLeadingFiller(num, maxSize) + str(num)
  return "(" + numString + "/" + maxSizeString + ")"

def renderPercentage(num, max):
  percentage = int(num/max*100)
  return getLeadingFiller(percentage, 100) + str(percentage) +  "%"


# Repair SVN directories. Print status while it's happening
# ---------------------------------------------------------
def repairSvnDirs(repos):
  svnStructure = ['prop-base', 'props', 'text-base', 'tmp', join('tmp','prop-base'), join('tmp','props'), join('tmp','text-base')]
  
  repoIndex    = 0;
  rebuildCount = 0;
  dirCount     = 0;
  for key, dirs in repos.items():
    # Set up status printing
    repoIndex += 1;
    repoString = " " + renderRepoCounter(repoIndex, len(repos)) + " Rebuilding " + split(key)[1] + "..." 
    statusString = ""
    
    # Go through all directories and rebuild them
    for dirIndex, dir in enumerate(dirs):
      for svnStruct in svnStructure:
        svnDir = join(dir, svnStruct)
        dirCount += 1;
        if not(exists(svnDir)):
          mkdir(svnDir)
          rebuildCount += 1;
    
      statusString = getEscapeChars(statusString) + renderPercentage(dirIndex+1, len(dirs)) + repoString
      sys.stdout.write(statusString)
    print('')

  print("\nRebuilt", rebuildCount, "of", dirCount, "directories.")
  
  
# Clean and update SVN directories.
# ---------------------------------------------------------
def updateSvnDirs(repos):
  for repoIndex, repo in enumerate(repos.keys()):
    repoString = renderRepoCounter(repoIndex+1, len(repos)) + " Cleaning " + split(repo)[1] + "..."
    print(repoString)
    os.system("svn cleanup " + repo)
    
  print('')
  for repoIndex, repo in enumerate(repos.keys()):
    repoString = renderRepoCounter(repoIndex+1, len(repos)) + " Updating " + split(repo)[1] + "..."
    print(repoString)
    os.system("svn update " + repo)



# Default settings
# ------------------------------------------------------
startDir     = abspath(os.getcwd())

print("Locating SVN directories...")
repos        = findSvnRepos(startDir)

print("\nRebuilding SVN directories...")
repairSvnDirs(repos)

print("\nCleaning and updating SVN directories...")
updateSvnDirs(repos)
