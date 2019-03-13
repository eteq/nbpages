#!/bin/bash

# vars for this script:
# GH_EMAIL - github email
# GH_NAME - github name
# REPO_URL - repo url to clone from (https or ssh)
# DEPLOY_BRANCH - branch to deploy to (normally gh-pages)
# WORKSPACE - where to copy files from to add to deploy commit (build location)
# BUILD_TAG - tag for deploy commit
# These can be set by using "export var=value" for manual deploy
# Or they are set in environment vars when used on CI

git config --global user.email $GH_EMAIL
git config --global user.name $GH_NAME

git clone -b ${DEPLOY_BRANCH} --single-branch ${REPO_URL} /out
cd /out

cp -aR ${WORKSPACE}/* .

git add .
git commit -m "Automated deployment to GitHub Pages: ${BUILD_TAG}" --allow-empty
git push origin $DEPLOY_BRANCH
git clean -dfx
