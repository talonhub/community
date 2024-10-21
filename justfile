default:
  just --list

log:
  tail -n 300 -f ~/.talon/talon.log

shell:
  ~/.talon/bin/repl
