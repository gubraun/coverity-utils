#!/bin/sh

cov-make-library -of cov-model.xml --security cov-model.c
cov-build --dir idir gcc -c taintme.c
cov-analyze --dir idir --all --model-file cov-model.xml


