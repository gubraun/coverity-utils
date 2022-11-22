# cov-check-deviations
Checks Coverity defects with classification `Intentional` for triage comments and sets `Deviation Status` attribute accordingly. 

## Install
`pip install requests`

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
