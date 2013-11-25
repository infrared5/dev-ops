Introduction
---
> General utility scripts for dev-ops.

## continuous-integration
Contains Python scripts for maintaining CI servers and projects.

### development
```
cd continuout-integration
mkvirtualenv ir5-ci
pip install -r requirements.txt
```

### tests
```
nosetests tests/jenkins/ tests/teamcity/
```

TeamCity
---
Included in the _/continuous-integration_ scripts is an archive for teamcity projects.
```
usage: teamcity.py [-h] [-n NAME] {archive,unarchive,ls}
```

## Getting Setup

* Requires [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)

```
cd ./continuos-integration
mkvirtualenv dev-ops -r requirements.txt --system-site-packages
workon dev-ops
python teamcity.py
```

### archive
The script will assume that projects to archive are created/installed in the default directory for TeamCity found in _~/.BuildServer/config/projects_

```
python teamcity.py archive -n MyProject
```

Upon successful archival, MyProject will become a _.zip_ file that can be unarchived at a later date.

*Note* TeamCity will need to be restarted in order for the project to be removed from the registry. You can always unarchive and restart TeamCity at a later date to get the project back.

### unarchive
The script will assume that a previous archived and zipped files resides in _~/.BuildServer/config/projects_.

```
python teamcity.py unarchive -n MyProject
```

Upon successful unarchival, the _.zip_ will be trashed and the project folder restored.

*Note* TeamCity will need to be restarted in order for the project to be removed from the registry

### ls
Allows you to list the previously archive projects using the teamcity python script.
