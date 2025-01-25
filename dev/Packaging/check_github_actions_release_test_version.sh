
#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

echo "Github Actions Tag '$GITHUB_REF'"

# Ensure we can identify our own version
REPO_VERSION="$(sed -nr 's/^version\s*=\s*\"([0-9]+\.[0-9]+\.[0-9]+)\"\s*$/\1/p' pyproject.toml)"

if [ -z "$REPO_VERSION" ]
then
    echo "Failed to identify the pyproject.toml Version"
    exit 1
else
    echo "Repository Version identified: '$REPO_VERSION'"
fi

# # Check the Github Actions Tag matches our Version number
# echo "Trying to Match '$REPO_VERSION' to '$GITHUB_REF'"
# if [ "refs/tags/$REPO_VERSION" != "$GITHUB_REF" ]
# then
#     echo "Failed to match Repository Version '$REPO_VERSION' to Github Actions Tag '$GITHUB_REF'"
#     exit 1
# else
#     echo "Repository Version matches Github Actions Tag"
# fi

exit 0
