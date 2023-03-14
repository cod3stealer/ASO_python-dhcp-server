#!/bin/bash

git add $PWD
read -p "Introduce el commit: " msg
git commit -m "$msg"
git push -u origin main
