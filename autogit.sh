#!/bin/bash

git config  --global user.email "sromerodiaz@dnaielcastelao.org"
git config  --global user.name "cod3stealer"

git add $PWD
read -p "Introduce el commit: " msg
git commit -m "$msg"
git push -u origin main
