# Summary 

Prerequisites:
* Raspberry Pi
* Sense HAT

Steps:
1. Install prometheus (`sudo apt install prometheus`)
1. Install [grafana](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)
1. Add the weather script to `/opt/weather` and create a systemd service to run it on boot
1. Open grafana, add prometheus as a datasource, create a dashboard based on the metrics reported by the script 
