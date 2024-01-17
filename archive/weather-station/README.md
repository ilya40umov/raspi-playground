# Summary 

Prerequisites:
* Raspberry Pi
* Sense HAT

Steps:
1. Install prometheus (`sudo apt install prometheus`)
1. Install [grafana](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)
1. Add the weather script to `/opt/weather` and create a systemd service to run it on boot
1. Open grafana, add prometheus as a datasource, create a dashboard based on the metrics reported by the script 

Useful commands:
```
sudo apt update && sudo apt upgrade

sudo apt install sense-hat
sudo reboot

sudo apt install prometheus
sudo systemctl enable prometheus

wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

sudo apt install nginx
sudo systemctl enable nginx

sudo apt install python3-prometheus-client
sudo mkdir /opt/weather
sudo mv weather_statition.py /opt/weather/
sudo adduser --disabled-login weather
sudo addgroup weather input
sudo addgroup weather gpio
sudo addgroup weather i2c
ssudo chown -R weather:weather /opt/weather/

sudo mv weather.service /etc/systemd/system/weather.service
sudo systemctl daemon-reload
sudo systemctl start weather
sudo systemctl enable weather
```

Edit prometheus config: `sudo vim /etc/prometheus/prometheus.yml`

```
  - job_name: weather
    static_configs:
      - targets: ['localhost:8000']
```

Edit grafana config: `sudo vim /etc/grafana/grafana.ini`

```
publicDashboards = true
```

Edit nginx config: `sudo vim /etc/nginx/sites-available/default`

```
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        location = / {
                return 301 http://weather.home/public-dashboards/5387da648e2e45b2a0b6cfb2e5f6ff53;
        }

        location / {
                proxy_pass http://localhost:3000;
                proxy_set_header Host $http_host;
        }
}
```
