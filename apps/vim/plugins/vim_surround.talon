# see `code/vim.py` for more implementation
tag: vim
-

# TODO
#  - add custom surround with markdown command for when i forget to use snip
#    first
#  - saying surround gets tiring, so maybe use wrap

# visual mode only
(surround|wrap) selected with <user.vim_surround_targets>:
    user.vim_visual_mode("S{vim_surround_targets}")

# normal mode

# selects the word under cursor
(surround|wrap) this with <user.vim_surround_targets>:
    user.vim_normal_mode("ysiw{vim_surround_targets}")

# cursor to the end of the word
(surround|wrap) with <user.vim_surround_targets>:
    user.vim_normal_mode("ysw{vim_surround_targets}")

(surround|wrap) <user.vim_text_objects> with <user.vim_surround_targets>:
    user.vim_normal_mode("ys{vim_text_objects}{vim_surround_targets}")

(surround|wrap) <user.vim_motions_all_adjust> with <user.vim_surround_targets>:
    user.vim_normal_mode("ys{vim_motions_all_adjust}{vim_surround_targets}")

(surround|wrap) <user.vim_unranged_surround_text_objects> with <user.vim_surround_targets>:
    user.vim_normal_mode("ys{vim_unranged_surround_text_objects}{vim_surround_targets}")

(surround|wrap) line with <user.vim_surround_targets>:
    user.vim_normal_mode("yss{vim_surround_targets}")

(surround|wrap) and indent line with <user.vim_surround_targets>:
    user.vim_normal_mode("ySS{vim_surround_targets}")

(delete|remove) (surrounding|those) <user.vim_surround_targets>:
    user.vim_normal_mode("ds{vim_surround_targets}")

(change|replace|swap) (surrounding|those) <user.vim_surround_targets> (to|with) <user.vim_surround_targets>:
    user.vim_normal_mode("cs{vim_surround_targets_1}{vim_surround_targets_2}")
