# cov-check-deviations
Checks Coverity defects with classification `Intentional` for triage comments and sets `Deviation Status` attribute accordingly. 

## Purpose
The script searches the defect's triage history for user triage comments on `Intentional` defect. If a comment is found, it sets the `Deviation Status` attribute to `Ready for Review`. If no comment is found, it sets it to `Comment Needed`. This will help quality engineers to find and audit deviation records.

## Install
```
python -m venv venv
. ./venv/Scripts/activate
pip install requests
```

## Run
```
gunnar@gunnar-7410 MINGW64 ~/Projects/coverity-utils/cov-check-deviations (master)
$ ./main.py
Checking for 'Deviation Status' attribute...
... ok.
Reading issues with classification 'Intentional'...
... found 3 issues.
375685 -> Comment Missing
375686 -> Ready for Review
376358 -> Ready for Review
```
