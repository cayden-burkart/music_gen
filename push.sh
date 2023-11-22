#!/bin/bash

# Configuration
PERCENTAGE=4  # Percentage of files to add in each iteration
REPO_DIR="./"  # Your repository directory
REMOTE="origin"  # Remote name
BRANCH="main"  # Branch name

# Navigate to the repository directory
cd "$REPO_DIR" || exit

# Find all files and store them in an array
FILES=($(find . -type f -not -path '*/\.git/*' | sort -R))

# Calculate the batch size
TOTAL_FILES=${#FILES[@]}
BATCH_SIZE=$((TOTAL_FILES * PERCENTAGE / 100))
[ $BATCH_SIZE -eq 0 ] && BATCH_SIZE=1  # Ensure at least one file per batch

# Process files in batches
for ((i=0; i < TOTAL_FILES; i+=BATCH_SIZE)); do
    echo "Adding files from index $i to $(($i + BATCH_SIZE - 1))"

    # Add files in the current batch
    for ((j=i; j < i + BATCH_SIZE && j < TOTAL_FILES; j++)); do
        git add "${FILES[$j]}"
    done

    # Commit and push the batch
    git commit -m "Adding files batch from $i to $j"
    git push $REMOTE $BRANCH

    # Optional: a small delay between pushes
    sleep 1
done

echo "All files have been added and pushed!"
