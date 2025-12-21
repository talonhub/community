# talon-gaze-ocr

[Talon](https://talonvoice.com/) scripts to enable advanced cursor control using
eye tracking and text recognition (OCR). This is alpha functionality which uses
experimental/unsupported APIs, so it could break at any time. See
[my blog post](https://handsfreecoding.org/2022/11/27/gaze-ocr-talon-support-and-10-new-features/)
for an overview.

## Installation

Prerequisite: Requires [community](https://github.com/talonhub/community) to be
installed as a sibling in the same directory.

`git clone` this repo into your Talon user scripts folder. If you are on Talon
Beta, switch to the "beta" branch (add flag `-b beta`) to take advantage of
beta-only features. 

If you use [Talon HUD](https://github.com/chaosparrot/talon_hud), consider
setting `user.talon_hud_allows_capture = false` to make the HUD invisible to OCR
(only supported on Talon Beta).

Restart Talon to ensure that the package is fully reloaded. Unlike most Talon
scripts, this package requires Talon to be restarted when it is updated or
settings are changed.

Required permissions:

- On Mac, Talon requires the ability to read the screen. As per the
  [macOS User Guide](https://support.apple.com/guide/mac-help/control-access-to-screen-recording-on-mac-mchld6aa7d23/mac):
  1. Choose Apple menu > System Settings, then click Privacy & Security in the sidebar. (You may need to scroll down.)
  2. Click Screen Recording.
  3. Turn screen recording on for Talon.

Required Python packages:

- All Python package dependencies are present in the `.subtrees` directory so
  that no pip installations are needed. If packages are have been installed
  manually through pip, these will be preferred (e.g. so that faster binary
  packages can be used.)

Note: This installation process is for Windows and Mac. Linux is not officially
supported because Talon does not provide an OCR API. You may be able to get this
working using Tesseract, but this configuration is not tested by the author.

## Features:

- Click, select, or position caret adjacent to any text visible onscreen.
- Tracks eye position as you speak to filter matches.
- Offers disambiguation if multiple matches are present.
- Applies fuzzy matching to one or more spoken words.
- Works with or without an eye tracker (just expect slower processing and more
  disambiguation).
- Matches homophones of recognized words (based on CSV in
  [community](https://github.com/talonhub/community)). Also
  matches digits and punctuation in either their spoken form (e.g. "two" and
  "period") or their symbolic form (e.g. "2" and ".").
- Briefly displays debugging overlay if no matches are present.
- Beta-only: match on any `<user.prose>`, including numbers.
- Beta-only: match on any onscreen words, even outside of your vocabulary.
- Beta-only: [intuitive editing
  commands](https://handsfreecoding.org/2024/03/15/making-writing-and-editing-with-your-voice-feel-natural/)
  including "revise" and "insert".

## Known limitations:

- Only operates on the main screen, as defined by Talon.
- Updates (via git pull) and some settings changes require Talon restart.
- Numbers must be referred to by their individual digits (except in Beta where
  you can say `numb <number>`).
- Modifications to punctuation and digit names in
  [community](https://github.com/talonhub/community) not leveraged.
- Depends on OS-provided text recognition (OCR), which is not perfectly accurate.
- Cursor positioning often imprecise around text with underline, strikethrough,
  or squiggly.
- Text caret can interfere with text recognition.
- Command subtitles may cause disambiguation when selecting a range of text.
- Dragon recognition timestamps are slightly off, leading to lower accuracy
  especially during text selection. Works best with Conformer.
- Text selection only works in apps that support shift-click to select (vs.
  dragging), which excludes some PDF viewers. 
- See the [issue tracker](https://github.com/wolfmanstout/talon-gaze-ocr/issues)
  for bugs that have been discovered.

## Dependencies

The .subtrees directory contains dependency packages needed by talon-gaze-ocr:

- gaze-ocr was cloned from https://github.com/wolfmanstout/gaze-ocr
- screen-ocr was cloned from https://github.com/wolfmanstout/screen-ocr
- rapidfuzz was cloned from https://github.com/maxbachmann/RapidFuzz

Changes in this repository are automatically pushed out to `gaze-ocr` and
`screen-ocr` via a GitHub Action that uses `git subtree`.

## Running without `community`

As noted in the installation instructions,
[community](https://github.com/talonhub/community) is highly recommended,
but most functionality will still be available in degraded form without it (and
you will see some warning logs). Missing functionality:

- The main `user.timestamped_prose` capture is missing custom vocabulary and
  punctuation support.
- No homophones means no automatic smart handling of homophones (e.g. if "hear"
  is recognized it won't match "here" onscreen).
- "scroll" commands use `user.mouse_scroll_*()`, so they won't work.
- "replace" and "say" commands use `user.prose` to insert text, so they won't
  work.
- `actions.user.dictation_peek` not available means text
  deletion/replacement isn't as smart (i.e. extra space is left over when a word
  is deleted).
