# Software installation

### Grafana

```
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update 
sudo apt-get install -y grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

### Prometheus

```
cd /tmp
wget https://github.com/prometheus/prometheus/releases/download/v2.23.0/prometheus-2.23.0.linux-armv7.tar.gz
tar xfz prometheus-2.23.0.linux-armv7.tar.gz

sudo mkdir /opt/prometheus/
sudo mv prometheus-2.23.0.linux-armv7/* /opt/prometheus/

sudo useradd -rs /bin/false prometheus
sudo chown -R prometheus:prometheus /opt/prometheus/
```

`sudo vim /etc/systemd/system/prometheus.service`

```
[Unit]
Description=Prometheus Server
Documentation=https://prometheus.io/docs/introduction/overview/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
Restart=on-failure
ExecStart=/opt/prometheus/prometheus \
  --config.file=/opt/prometheus/prometheus.yml \
  --storage.tsdb.path=/opt/prometheus/data \
  --web.console.templates=/opt/prometheus/consoles \
  --web.console.libraries=/opt/prometheus/console_libraries \
  --web.listen-address=0.0.0.0:9090

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl start prometheus 
sudo systemctl enable prometheus
```

`sudo vim /opt/prometheus/prometheus.yml`

Add the following:
```
 - job_name: 'grafana'
    static_configs:
    - targets: ['localhost:3000']
```

### node_exporter

```
cd /tmp
wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-armv7.tar.gz
tar xfz node_exporter-1.0.1.linux-armv7.tar.gz

sudo mkdir /opt/node_exporter/
sudo mv node_exporter-1.0.1.linux-armv7/* /opt/node_exporter/
sudo chown -R prometheus:prometheus /opt/node_exporter/
```

`sudo vim /etc/systemd/system/node-exporter.service`

```
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Restart=on-failure
ExecStart=/opt/node_exporter/node_exporter

[Install]
WantedBy=default.target
```

```
sudo systemctl daemon-reload
sudo systemctl start node-exporter 
sudo systemctl enable node-exporter
```

`sudo vim /opt/prometheus/prometheus.yml`

Add the following:
```
 - job_name: 'node_exporter'
    static_configs:
    - targets: ['localhost:9100']
```

### fritzbox_exporter

```
sudo apt install golang
go get github.com/mxschmitt/fritzbox_exporter
cd go/src/github.com/mxschmitt/fritzbox_exporter/cmd/exporter
go get ./...
go build
cd ~

sudo mkdir /opt/fritzbox_exporter
sudo cp go/src/github.com/mxschmitt/fritzbox_exporter/cmd/exporter/exporter /opt/fritzbox_exporter/fritzbox_exporter

sudo useradd -rs /bin/false fritzboxexporter
sudo chown -R fritzboxexporter:fritzboxexporter /opt/fritzbox_exporter/
```

`sudo vim /etc/systemd/system/fritzbox-exporter.service`

```
[Unit]
Description=Fritzbox Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=fritzboxexporter
Group=fritzboxexporter
Restart=on-failure
ExecStart=/opt/fritzbox_exporter/fritzbox_exporter -username=fritzbox_exporter -password=xyz
StandardOutput=null

[Install]
WantedBy=default.target
```

```
sudo systemctl daemon-reload
sudo systemctl start fritzbox-exporter 
sudo systemctl enable fritzbox-exporter
```

`sudo vim /opt/prometheus/prometheus.yml`

```
 - job_name: 'fritzbox_exporter'
    static_configs:
    - targets: ['localhost:9133']
```

Grafana dashboard: https://grafana.com/grafana/dashboards/11593

### Synology NAS

Use the following docker-compose file on NAS itself to start the exporter there:
```
version: '2.0'

services:
  node-exporter:
    privileged: true
    network_mode: host
    image: prom/node-exporter:v1.0.1
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/host/root:ro
    ports:
      - 9100:9100
    restart: always
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/host/root'
      - --collector.filesystem.ignored-mount-points
      - "^/(sys|proc|dev|host|etc|volume1/@docker/.+)($$|/)"
      - --collector.filesystem.ignored-fs-types
      - "^(tmpfs|autofs|binfmt_misc|cgroup|configfs|debugfs|devpts|devtmpfs|fusectl|hugetlbfs|mqueue|overlay|proc|procfs|pstore|rpc_pipefs|securityfs|sysfs|tracefs)$$"
```

Then add NAS endpoint to `node_exporter` job.

### Airflow

TODO: try next time to install Airflow somewhere under `/opt/`

```
sudo apt install postgresql-11

sudo apt-get install build-essential
sudo apt-get install -y --no-install-recommends \
        freetds-bin \
        krb5-user \
        ldap-utils \
        libffi6 \
        libsasl2-2 \
        libsasl2-modules \
        libssl1.1 \
        locales  \
        lsb-release \
        sasl2-bin \
        sqlite3 \
        unixodbc

sudo apt-get install libmariadb-dev-compat libmariadb-dev

sudo useradd -m -d /home/airflow airflow

AIRFLOW_VERSION=1.10.13
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip3 install "apache-airflow[devel,postgres,celery,password,docker,amazon,redis,ssh]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

Then run `pip3 uninstall numpy` (needed due to [this](https://github.com/numpy/numpy/issues/14553)).

Edit `airflow.cfg` (e.g. update LocalExecutor, connection URL etc.)

Add `airflow` user in Postgres using the following SQL:
```
CREATE USER airflow PASSWORD 'airflow';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;
```

And then run:
```
airflow initdb
airflow checkdb
```

After which you can set up authentication by editing `vim ~/airflow/airflow.cfg`.

```
[webserver]
authenticate = True
auth_backend = airflow.contrib.auth.backends.password_auth
```

`sudo vim /etc/systemd/system/airflow-webserver.service`

```
[Unit]
Description=Airflow webserver
After=network.target postgresql.service
Wants=postgresql.service

[Service]
User=airflow
Group=airflow
ExecStart=/home/airflow/.local/bin/airflow webserver
Environment=PATH=/home/airflow/.local/bin:$PATH
Restart=on-failure

[Install]
WantedBy=default.target
```

`sudo vim /etc/systemd/system/airflow-scheduler.service`

```
[Unit]
Description=Airflow scheduler
After=network.target postgresql.service
Wants=postgresql.service

[Service]
User=airflow
Group=airflow
ExecStart=/home/airflow/.local/bin/airflow scheduler
Environment=PATH=/home/airflow/.local/bin:$PATH
Restart=on-failure

[Install]
WantedBy=default.target
```

```
sudo systemctl daemon-reload
sudo systemctl start airflow-webserver
sudo systemctl enable airflow-webserver
sudo systemctl start airflow-scheduler
sudo systemctl enable airflow-scheduler
```

### Useful Links

* http://www.d3noob.org/2020/02/installing-prometheus-and-grafana-on.html
* https://www.howtoforge.com/tutorial/how-to-install-prometheus-and-node-exporter-on-centos-8/
* https://towardsdatascience.com/how-to-run-apache-airflow-as-daemon-using-linux-systemd-63a1d85f9702
* https://airflow.apache.org/docs/apache-airflow/stable/security.html#password
