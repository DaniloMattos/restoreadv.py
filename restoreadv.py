#!/usr/bin/env python

#################################################################################################
# Author: Danilo Mattos                                                                         #
# Enterprise: Hostgator                                                                         #
# Created on: 17/04/2021                                                                        #
# Functions: - Restore a domain files from a full backup of cpanel                              #
#            - Restore a informed path like mail/                                               #
# Sintax: command -u user --domain domain.tld --path pathtorestore full_cpanel_backup_directory #
#                                                                                               #
#################################################################################################

import json, sys, os, shutil
import subprocess
import traceback
import logging

sintax='[!] Sintax: restore.py -u user [--domain domain.tld] [--path path/to/restore] full_cpanel_backup_directory'

try:
    argumentsLength=len(sys.argv) # Length of arguments
    argumentsList=list(sys.argv) # Create a list of arguments
    backupDirectory=str(sys.argv[int(len(sys.argv)-1)]) # Get the backup directory from the last argument
    pathToUserdataCache=backupDirectory + '/userdata/cache.json' # Creates a path to the cache.json file
    pathToHomedir=backupDirectory + '/homedir' # Defines the path for home directory on backup directory
    pathToMysql=backupDirectory + '/mysql'

    with open(pathToUserdataCache) as json_file: # Open the cache.json file to get data
        data = json.load(json_file)
except:
    print(sintax)
    sys.exit(1)

for arg in argumentsList:
    if arg == '-u':
        cwd=os.path.expanduser("~"+argumentsList[argumentsList.index(arg)+1]) + '/' # Get user path
    if arg == '--domain':
        try:
            pathToRestore=data[argumentsList[argumentsList.index(arg)+1]][4] # Get the path of domain
            pathToRestore=pathToRestore.split('/',3)[3] # Split to get only after /home/user/
            pathToSource=pathToHomedir + '/' + pathToRestore + '/' # Create the source of files inside backup directory
            pathToDestination=cwd + pathToRestore + '/' # Create the path destination with cwd informed on --cwd argument

            if os.path.exists(cwd):
                print('Restoring files on: ' + pathToDestination)
                if not os.path.exists(pathToDestination): # Check if directory exists on destination
                    print('Creating directory ' + pathToDestination)
                    os.makedirs(pathToDestination) # If doesnt exists create the directory recursively
                    subprocess.call(["rsync","-qavt",str(pathToSource),str(pathToDestination)])
                    print('Restore complete')
                else:
                    subprocess.call(["rsync","-qavt",str(pathToSource),str(pathToDestination)])
                    print('Restore complete')
            else:
                print('Path '+ cwd + ' do not exists')
                print(sintax)
        except Exception as e:
            logging.error(traceback.format_exc())
            print(sintax)
            sys.exit(1)
    if arg == '--path':
        try:
            pathToRestorePath=argumentsList[argumentsList.index(arg)+1] # Get the path of domain
            pathToSource=pathToHomedir + '/' + pathToRestorePath + '/' 
            pathToDestination=cwd + pathToRestorePath + '/' 

            if os.path.exists(cwd) and os.path.exists(pathToSource):
                print('Restoring files on: ' + pathToDestination)
                if not os.path.exists(pathToDestination): # Check if directory exists on destination
                    print('Creating directory ' + pathToDestination)
                    os.makedirs(pathToDestination) # If doesnt exists create the directory recursively
                    subprocess.call(["rsync","-qavt",str(pathToSource),str(pathToDestination)])
                    print('Restore complete')
                else:
                    subprocess.call(["rsync","-qavt",str(pathToSource),str(pathToDestination)])
                    print('Restore complete')
            else:
                print('Path(s) '+ cwd + ' or '+ pathToSource +' do not exist')
                print(sintax)
        except Exception as e:
            logging.error(traceback.format_exc())
            print(sintax)
            sys.exit(1)
    if arg == '--singledb':
        pathToRestoredb=argumentsList[argumentsList.index(arg)+1]
        pathToSourcedb=pathToMysql + '/' + pathToRestoredb + '.sql'
        print(pathToSourcedb)
