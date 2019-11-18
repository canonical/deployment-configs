#! /usr/bin/env bash

# The only purpose of this script is to verify that the template system
# used in this branch will not change to the current projects.

# Bash strict mode
set -euo pipefail

# Remove older log file
if [[ -f ./diff.log ]]; then
  rm ./diff.log
fi

printf "\nLooking for kubernetes changes against previous manifest files\n"

# Get current git branch name
branch_name="$(git symbolic-ref HEAD 2>/dev/null)"
branch_name=${branch_name##refs/heads/}

# Apply all old configurations
printf "\n- Importing all previous configurations\n"
git checkout master &> /dev/null
TAG_TO_DEPLOY="latest"

# Import previous service and deployment objects
for file in ./services/*.yaml; do
  cat $file | sed "s|[:][$][{]TAG_TO_DEPLOY[_aa-zA-Z]*[}]|:latest|" | sed 's|replicas: [0-9][0-9]*|replicas: 1|' | microk8s.kubectl apply --filename - --namespace default 1> /dev/null
done

# Import ingress for production
for file in ./ingresses/production//*.yaml; do
  cat $file | sed '/namespace:/d' | microk8s.kubectl apply --filename - --namespace default 1> /dev/null
done

# Import ingress for staging
for file in ./ingresses/staging/*.yaml; do
  cat $file | sed '/namespace:/d' | microk8s.kubectl apply --filename - --namespace default 1> /dev/null
done

printf "\n- Diff old configs with new ones\n"

# Checkout to the new branch
git checkout $branch_name &> /dev/null

# Diff old configs with new ones
for file in ./sites/*.yaml; do
    filename=$(basename $file .yaml)

    # Print current project file
    printf "\n$filename\n"

    # User kubectl diff to detect changes
    if ./konf.py --local-qa production $file | microk8s.kubectl diff -f - 1>> ./diff.log; then
        printf "\tProduction: Okay\n";
    else
        printf "\tProduction: Changes detected!!!!\n";
    fi

    if ./konf.py --local-qa staging $file | microk8s.kubectl diff -f - 1>> ./diff.log; then
        printf "\tStaging: Okay\n";
    else
        printf "\tStaging: Changes detected!!!!\n";
    fi
done
