#!/bin/bash

sudo rm -r .git
git init
git add .
git commit -m "first commit"
git branch -M master
git remote add origin https://github.com/Rhixe-company/rhixe_scans.git
git push -u origin master -f
pre-commit install
pre-commit clean
pre-commit gc
pre-commit autoupdate
git add --all
git commit -m 'Development Updates'
git push

# # # # # prod
# git add --all
# git commit -m 'Development Updates'
# git push
# pre-commit install
# pre-commit clean
# pre-commit gc
# pre-commit autoupdate
# git add --all
# git commit -m 'Development Updates'
# git push

# # git remote add origin  https://github.com/Rhixe-company/rhixe_scans.git
# # # git branch -M master
# # git push -u origin master -f

# # # dev
# sudo rm -r .git
# git init
# git add .
# git commit -m "first commit"
# git branch -M development
# git remote add origin https://github.com/Rhixe-company/rhixe_scans.git
# git push -u origin development -f
