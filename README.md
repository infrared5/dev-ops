Introduction
---
> General utility scripts for dev-ops.

## continuous-integration
Contains scripts for maintaining CI servers and projects.

### development 
'''
cd continuout-integration
mkvirtualenv ir5-ci
pip install -r requirements.txt
'''

### tests
'''
nosetests tests/jenkins/ tests/teamcity/
'''