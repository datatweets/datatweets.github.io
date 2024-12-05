#!/bin/bash

# Build the Hugo site
hugo --minify

# Navigate to the public folder
cd public

# Add and commit changes
git init
git add .
git commit -m "Update site content"

# Push to gh-pages
git branch -M gh-pages
git remote add main https://github.com/datatweets/datatweets.github.io.git
git push -u main gh-pages --force

# Return to the project root
cd ..
