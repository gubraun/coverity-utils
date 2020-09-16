#!/bin/sh

cov-build --dir idir gcc -c test.c

# run analysis without model - will give FORWARD_NULL defect
cov-analyze --dir idir --all

# create model
cov-make-library -of user_models.xmldb my_reset.c

# run analysis with model - no defect
cov-analyze --dir idir --all --model-file user_models.xmldb
