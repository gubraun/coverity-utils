# start clean
rm -rf idir
# make model for mythreads
cov-build --dir idir g++ -c mythreads.cpp
cov-analyze --dir idir --disable-default --concurrency 
cov-collect-models --dir idir -of mythreads.xmldb
# build and analyze testcase #1
rm -rf idir
cov-build --dir idir g++ -c main_nested.cpp 
cov-analyze --dir idir --disable-default --concurrency --model-file mythreads.xmldb
# build and analyze testcase #1
rm -rf idir_fromsource
cov-build --dir idir_fromsource g++ -c main_nested.cpp mythreads.cpp
cov-analyze --dir idir_fromsource --disable-default --concurrency
