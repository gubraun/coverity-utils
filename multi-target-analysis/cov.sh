#!/bin/bash

CONNECT_OPTS="--host gunnar-vbox --user admin --password sigpass"

rm -rf idir

cov-build --dir idir make clean all

cov-analyze --dir idir --tu-pattern "arg('-m32')" --output-tag="-x86" 
cov-analyze --dir idir --tu-pattern "arg('-m64')" --output-tag="-x86_64"
cov-analyze --dir idir --tu-pattern "arg('-march=armv7-r')" --output-tag="-armv7-r"
cov-analyze --dir idir --tu-pattern "arg('-march=armv8-a')" --output-tag="-armv8-a"

# create streams and project

proj="Multi-Target Build"
streams="hello-x86 hello-x86_64 hello-armv7-r hello-armv8-a"

# delete projects/streams from previous runs
for stream in $streams; do
	os=$(cov-manage-im $CONNECT_OPTS --mode streams --delete --name $stream)
done
os=$(cov-manage-im $CONNECT_OPTS --mode projects --delete --name "$proj")

# create projects/streams
cov-manage-im $CONNECT_OPTS --mode projects --add --set name:"$proj"
for stream in $streams; do
	cov-manage-im $CONNECT_OPTS --mode streams --add --set name:"$stream"
	cov-manage-im $CONNECT_OPTS --mode projects --update --name "$proj" --insert stream:"$stream"
done

cov-commit-defects --dir idir --output-tag="-x86"     --stream hello-x86     $CONNECT_OPTS
cov-commit-defects --dir idir --output-tag="-x86_64"  --stream hello-x86_64  $CONNECT_OPTS
cov-commit-defects --dir idir --output-tag="-armv7-r" --stream hello-armv7-r $CONNECT_OPTS
cov-commit-defects --dir idir --output-tag="-armv8-a" --stream hello-armv8-a $CONNECT_OPTS
