#!/bin/sh

cov-build --dir idir gcc -c annotated.cpp
cov-analyze --dir idir --all --strip-path `pwd`
