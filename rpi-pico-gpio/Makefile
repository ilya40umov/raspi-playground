.PHONY: phony_explicit

phony_explicit:

%.py: phony_explicit
	rshell cp $@ /pyboard/main.py
	$(MAKE) soft-reset

.PHONY: soft-reset
soft-reset:
	rshell "repl ~ import machine ~ machine.soft_reset() ~"
