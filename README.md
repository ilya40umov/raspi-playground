# raspi-howtos
A list of HOWTOs around setting up a Raspberry Pi

Note, that a lot of things mentioned here can be also done via `sudo raspi-config` (an interactive shell tool for configuring a raspberry pi):

### How to prepare an SD-card?

1. Download and unzip the latest OS image (can be found [here](https://www.raspberrypi.org/software/operating-systems/))
1. Insert the SD-card and unmount the auto-mounted partition (e.g. `umount /dev/sdb1`)
1. Write the image to an SD-card `sudo dd bs=4M if=2020-08-20-raspios-buster-armhf-lite.img of=/dev/sdb conv=fsync`
1. Run `sync` and then unplug and plug the SD-card again
1. Cd into the boot partition and execut `touch ssh`
1. Create `wpa_supplicant.conf` in the boot partition with the following content:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

### How to create a new user (and delete `pi` user)?

First, connect to the raspberry pi with `ssh pi@raspberrypi`.

Then add a new user with the same groups as `pi` user:
```
sudo adduser <newusername>
groups | sed 's/pi //g' | sed -e "s/ /,/g" | xargs -I{} sudo usermod -a -G {} <newusername>
```

Then reconnect to the pi as the new user and delete the `pi` user:
```
ssh <newusername>@raspberrypi
sudo deluser --remove-home pi
```

### What to install on a fresh Raspbian?

I have simply cherry-picked all applicable packages from 
[the list](https://github.com/ilya40umov/linux-mint-software-checklist) that I'm using for LM.

### How to monitor the temperature?

`watch 'head -n 1 /sys/class/thermal/thermal_zone0/temp | xargs -I{} awk "BEGIN {printf \"%.2f\n\", {}/1000}"'`

### How to change hostname?

Edit `/etc/hostname`

### How to change SSH port?

Edit `/etc/ssh/sshd_config` (uncomment the line with `# Port 22` and change 22 to the desired port number).
Then run `sudo service ssh restart`.

### How to deal with `cannot change locale` warnings?

In my case the issue was due to SSH agent picking up `LC_*` evnrionment variables from my PC 
and transferring them to the Rasberry Pi. 
A lot of commands would then complain about not being able to change locale 
and would default to whatever the default local for the Raspberry Pi was.

##### Solution #1: Generate files for the missing locale

```
perl -pi -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/g' /etc/locale.gen
locale-gen en_US.UTF-8
update-locale en_US.UTF-8
```

##### Solution #2: Prevent your SSH agent or Pi's SSH server from handling `LC_*` variables

Either comment out `SendEnv LANG LC_*` in `/etc/ssh/ssh_config` on your PC,
or comment out `AcceptEnv LANG LC_*` in the same file on Raspberry Pi. 

### How to install certain Software?

See [software.md](software.md) for instructions on how to install Grafana, Prometheus, Airflow etc.

### Useful Links

* https://www.raspberrypi.org/software/operating-systems/
* https://www.pragmaticlinux.com/2020/06/setup-your-raspberry-pi-4-as-a-headless-server/
* http://kamilslab.com/2016/12/10/how-to-change-your-ssh-port-on-the-raspberry-pi/
* https://www.cyberciti.biz/tips/linux-display-open-ports-owner.html
* https://www.jaredwolff.com/raspberry-pi-setting-your-locale/
* https://stackoverflow.com/questions/29609371/how-do-not-pass-locale-through-ssh
* https://www.pragmaticlinux.com/2020/06/check-the-raspberry-pi-cpu-temperature/
