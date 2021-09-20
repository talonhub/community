ph tag:
  "<?php"
  key(enter:2)
  "?>"
  key(up)
  key(tab)

word press loop template:
  "<?php"
  key(enter)
  "get_header();"
  key(enter)
  "if (have_posts()):"
  key(enter)
  key(tab)
    "while (have_posts()) :"
    key(enter)
    key(tab)
      "the_post(); "
      key(enter)
      "the_content();"
      key(enter)
      key(shift-tab)
    "endwhile;"
    key(enter)
    key(shift-tab)
  "endif;"
  key(enter)
  "get_footer();"
  key(enter)
  "?>"

