# see `code/vim.py` for more implementation
tag: vim
-

# visual mode only
surround selected with <user.vim_surround_targets>:
    user.vim_visual_mode("S{vim_surround_targets}")

# normal mode
surround <user.vim_text_objects> with <user.vim_surround_targets>:
    user.vim_normal_mode("ys{vim_text_objects}{vim_surround_targets}")

surround <user.vim_motions_all_adjust> with <user.vim_surround_targets>:
    user.vim_normal_mode("ys{vim_motions_all_adjust}{vim_surround_targets}")

surround <user.vim_unranged_surround_text_objects> with <user.vim_surround_targets>:
    user.vim_normal_mode("ys{vim_unranged_surround_text_objects}{vim_surround_targets}")

surround line with <user.vim_surround_targets>:
    user.vim_normal_mode("yss{vim_surround_targets}")

surround and indent line with <user.vim_surround_targets>:
    user.vim_normal_mode("ySS{vim_surround_targets}")

(delete|remove) (surrounding|those) <user.vim_surround_targets>:
    user.vim_normal_mode("ds{vim_surround_targets}")

(change|replace|swap) (surrounding|those) <user.vim_surround_targets> (to|with) <user.vim_surround_targets>:
    user.vim_normal_mode("cs{vim_surround_targets_1}{vim_surround_targets_2}")
