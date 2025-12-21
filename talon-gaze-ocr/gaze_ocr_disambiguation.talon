mode: command
mode: user.dictation_command
tag: user.gaze_ocr_disambiguation
-
<number_small>: user.choose_gaze_ocr_option(number_small)
# Handle frequent misrecognition.
choose to: user.choose_gaze_ocr_option(2)
numbers hide | scrape: user.hide_gaze_ocr_options()
