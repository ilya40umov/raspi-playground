pyfiles     := $(wildcard *.py)

.PHONY:

.rsync:
	rsync --exclude '*.swp' -r . breadboard:~/rpi-gpio

$(pyfiles): .rsync .PHONY
	ssh -t breadboard 'python3 ~/rpi-gpio/$@'
