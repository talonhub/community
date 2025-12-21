# NOTE: this script currently does not work due to https://jira.atlassian.com/browse/SRCTREEWIN-3198
git push origin main
git subtree push --prefix=.subtrees\screen-ocr screen-ocr master
git subtree push --prefix=.subtrees\gaze-ocr gaze-ocr master
