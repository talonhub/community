default:
  just --list

log:
  tail -n 300 -f ~/.talon/talon.log

repl: shell
shell:
  ~/.talon/bin/repl
