# NOTE: this script currently does not work due to https://jira.atlassian.com/browse/SRCTREEWIN-3198
git pull origin main
git subtree pull --prefix=.subtrees\screen-ocr --squash screen-ocr master
git subtree pull --prefix=.subtrees\gaze-ocr --squash gaze-ocr master
git subtree pull --prefix=.subtrees\rapidfuzz --squash rapidfuzz main
