
#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

echo "Github Actions Tag '$GITHUB_REF'"

# Ensure we can identify our own version
SETUP_CFG_VERSION="$(sed -nr 's/^version\s*=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$/\1/p' setup.cfg)"

if [ -z "$SETUP_CFG_VERSION" ]
then
    echo "Failed to identify the Setup.cfg Version"
    exit 1
else
    echo "Repository Version identified: '$SETUP_CFG_VERSION'"
fi

# Check the Github Actions Tag matches our Version number
echo "Trying to Match 'refs/tags/$SETUP_CFG_VERSION' to '$GITHUB_REF'"
if [ "refs/tags/$SETUP_CFG_VERSION" != "$GITHUB_REF" ]
then
    echo "Failed to match Repository Version '$SETUP_CFG_VERSION' to Github Actions Tag '$GITHUB_REF'"
    exit 1
else
    echo "Repository Version matches Github Actions Tag"
fi

exit 0
