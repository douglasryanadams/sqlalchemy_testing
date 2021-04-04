### Intro

The goal of this project is to research how SQLAlchemy handles DB connections and sessions.

### Setup


#### Run Locally

- Install Python 3.9+
- Install PostgreSQL Dev Binaries (for building `psycopg2`)
  - This may depend on installing GCC or other C compiler as well as OpenSSL or other TLS libraries
- Then:

```bash
python -m pip install --upgrade pip
python -m pip install poetry
python -m poetry install
```

### Instructions

These are instructions for using this test environment.

Run Docker Compose for Environment:

```bash
docker-compose up
```

Run Telegraf for metrics:

```bash
telegraf --config telegraf.conf
```

Connect to [Adminer](http://localhost:8080)

Log in:

| Attribute | Value       |
| --------- | ----------- |
| System    |  PostgreSQL |
| Server    |  postgres   |
| Username  |  postgres   |
| Password  |  postgres   |
| Database  |  postgres   |


Connect to [InfluxDB](http://localhost:8086)

| Attribute | Value    |
| --------- | -------- |
| Username  | influxdb |
| Password  | influxdb |

Links to Dashboards:

- [Docker Data](http://localhost:8086/orgs/7e76364335a7857e/dashboards/0753a0450417a000)
- [Postgres Data](http://localhost:8086/orgs/7e76364335a7857e/dashboards/07539ebb2cc19000)


Run Tests:

```bash
# alias poetry="python -m poetry"
poetry run pytest connection_testing.py
```

