not mode: user.gaze_ocr_disambiguation
tag: browser
and not tag: user.rango_disabled
and tag: user.rango_direct_clicking
and not tag: user.rango_explicit_clicking
and not tag: user.rango_explicit_clicking_forced
tag: browser
and not tag: user.rango_disabled
and tag: user.rango_direct_clicking_forced
-

^go <user.rango_target>$: user.rango_command_with_target("directClickElement", rango_target)
