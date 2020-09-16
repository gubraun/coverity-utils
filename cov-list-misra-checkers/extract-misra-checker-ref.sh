#!/bin/bash

tidy -w 0 $1 2>/dev/null \
| sed -n '/table summary=\"MISRA C 2012/,/\/table/p' \
| sed -n '/<tr>/,/<\/tr>/p' \
| sed -e 's/<a.*<\/a>//' \
    -e 's/<th align=\"center\">\(.*\)<\/th>/\"\1\",/' \
    -e 's/<td>\(.*\)<\/td>/\"\1\",/' \
    -e 's/<span class=\"checker_th\">//' \
    -e 's/<\/span>//' \
| sed -e 's/&nbsp;//' \
| sed '/<tr>/{n;:l N;/<\/tr>/b; s/\n//; bl}' \
| sed -e '/^<\/\?tr>/d'

