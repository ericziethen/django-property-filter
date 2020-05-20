@echo off

rem Setup the githooks directory
echo Setting git hooks directory to ".githooks"
git config core.hooksPath .githooks

rem Ensure we use non Fast Forward Merges
echo Disable Non Fast Forward Merges
git config merge.commit no
git config merge.ff no
git config pull.ff only

rem Alwaysh Push Annotated Tags
git config push.followTags true

rem set diff3 as default diff view
git config merge.conflictstyle diff3

