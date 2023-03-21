#!/bin/bash

git branch

git remote -v

git remote add origin https://github.com/cod3stealer/ASO_python-dhcp-server

cat /home/saitama/tok.txt

git config  --global user.email "sromerodiaz@dnaielcastelao.org"
git config  --global user.name "cod3stealer"

git add *
read -p "Introduce el commit: " msg
git commit -m "$msg"
git push -u origin main
