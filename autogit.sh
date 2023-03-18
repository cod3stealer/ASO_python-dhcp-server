#!/bin/bash

git branch

git remote -v

cat /home/saitama/tok.txt

git config  --global user.email "sromerodiaz@dnaielcastelao.org"
git config  --global user.name "cod3stealer"

git add *
read -p "Introduce el commit: " msg
git commit -m "$msg"
git push -u origin main
