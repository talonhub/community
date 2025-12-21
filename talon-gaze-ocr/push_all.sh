#!/bin/sh

git push origin main
git subtree push --prefix=.subtrees/screen-ocr screen-ocr master
git subtree push --prefix=.subtrees/gaze-ocr gaze-ocr master
