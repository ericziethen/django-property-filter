
#!/bin/bash

echo '##### Calling: '`basename "$0"` '('$0')'

echo "Travis Tag '$TRAVIS_TAG'"

# Ensure we can identify our own version
SETUP_CFG_VERSION="$(sed -nr 's/^version\s*=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$/\1/p' setup.cfg)"

if [ -z "$SETUP_CFG_VERSION" ]
then
    echo "Failed to identify our own Version"
    exit 1
else
    echo "Repository Version identified: '$SETUP_CFG_VERSION'"
fi

# Check the Travis Tag matches our Version number
if [ "$SETUP_CFG_VERSION" != "$TRAVIS_TAG" ]
then
    echo "Failed to match Repository Version '$SETUP_CFG_VERSION' to Travis Tag '$TRAVIS_TAG'"
    exit 1
else
    echo "Repository Version matches Travis Tag"
fi

exit 0
