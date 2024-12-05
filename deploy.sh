# #!/bin/bash
# rm -rf public/*
# # Build the Hugo site
# hugo --minify

# # Navigate to the public folder
# cd public

# # Initialize Git if it doesn't exist
# if [ ! -d ".git" ]; then
#   git init
#   git remote add main https://github.com/datatweets/datatweets.github.io.git
# fi

# # Pull the latest changes to avoid conflicts and preserve the CNAME file
# # git fetch main gh-pages
# # git reset --soft main/gh-pages

# # Ensure the CNAME file exists (preserve your custom domain)
# if [ ! -f "CNAME" ]; then
#   echo "datatweets.com" > CNAME
# fi

# # Add and commit the new changes
# git add .
# git commit -m "Update site content"

# # Push to the gh-pages branch
# git branch -M gh-pages
# git push -u main gh-pages --force

# # Return to the project root
# cd ..


#!/bin/bash

# Clean the local public folder
rm -rf public/*

# Build the Hugo site
hugo --minify

# Navigate to the public folder
cd public

# Initialize Git if it doesn't exist
if [ ! -d ".git" ]; then
  git init
  git remote add main https://github.com/datatweets/datatweets.github.io.git
fi
# Ensure the CNAME file exists (preserve your custom domain)
if [ ! -f "CNAME" ]; then
  echo "datatweets.com" > CNAME
fi
# Add and commit the new changes
git add .
git commit -m "Deploy updated site content"

# Push to the gh-pages branch, overwriting old content
git branch -M gh-pages
git push -u main gh-pages --force

# Return to the project root
cd ..
