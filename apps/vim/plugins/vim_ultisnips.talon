tag: vim
-
tag(): snippets
# XXX - can likely go to a generic snippet command in talon
(reload|refresh) snippets: user.vim_normal_mode_exterm(":call UltiSnips#RefreshSnippets()\n")
add snippets: user.vim_normal_mode_exterm(":UltiSnipsAddFiletypes \n")
#show file snippets: user.vim_normal_mode_exterm(":call UltiSnips#SnippetsInCurrentScope()\n")
#show all file snippets: user.vim_normal_modE_exterm(":call UltiSnips#SnippetsInCurrentScope(1)\n")
