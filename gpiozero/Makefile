pyfiles     := $(wildcard *.py)

.PHONY:

.rsync:
	rsync --exclude '*.swp' -r . breadboard:~/gpiozero

$(pyfiles): .rsync .PHONY
	ssh -t breadboard 'python3 ~/gpiozero/$@'
