
import time
from datetime import datetime, timezone

import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision

TB_URL = "https://thingsboard.cloud"

TB_USERNAME = "usernameCuaBan"
TB_PASSWORD = "matKhauCuaBan"
DEVICE_ID = "idThietBi"

KEYS = [
    "temperature",
    "humidity",
    "distance_cm",
    "rssi",
    "sequence",
    "uptime_s",
]

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "tokenCuaBan"
INFLUX_ORG = "PTIT"
INFLUX_BUCKET = "iot_data"

POLL_INTERVAL = 5


def login_thingsboard():
    """Dang nhap va lay JWT token."""
    response = requests.post(
        f"{TB_URL}/api/auth/login",
        json={
            "username": TB_USERNAME,
            "password": TB_PASSWORD,
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["token"]


def fetch_telemetry(jwt, start_ts, end_ts):
    """Truy van telemetry trong khoang thoi gian."""
    response = requests.get(
        f"{TB_URL}/api/plugins/telemetry/DEVICE/"
        f"{DEVICE_ID}/values/timeseries",
        headers={"X-Authorization": f"Bearer {jwt}"},
        params={
            "keys": ",".join(KEYS),
            "startTs": start_ts,
            "endTs": end_ts,
            "limit": 1000,
            "agg": "NONE",
            "orderBy": "ASC",
        },
        timeout=20,
    )

    response.raise_for_status()
    return response.json()


def convert_value(key, value):
    """Chuyen chuoi JSON sang kieu so phu hop."""
    if key in ("sequence", "uptime_s", "rssi"):
        return int(float(value))
    return float(value)


def main():
    print("Dang dang nhap ThingsBoard...")
    jwt = login_thingsboard()
    print("Dang nhap thanh cong.")

    last_ts = int(time.time() * 1000) - 60_000

    with InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG,
    ) as influx:
        write_api = influx.write_api()

        print("Bat dau thu thap. Nhan Ctrl+C de dung.")

        while True:
            try:
                end_ts = int(time.time() * 1000)

                try:
                    data = fetch_telemetry(jwt, last_ts + 1, end_ts)
                except requests.HTTPError as exc:
                    if exc.response is not None and exc.response.status_code == 401:
                        jwt = login_thingsboard()
                        data = fetch_telemetry(jwt, last_ts + 1, end_ts)
                    else:
                        raise

                rows = {}
                for key, values in data.items():
                    for item in values:
                        ts = int(item["ts"])
                        if ts <= last_ts:
                            continue

                        rows.setdefault(ts, {})[key] = item["value"]

                count = 0
                for ts in sorted(rows):
                    fields = {}
                    for key, value in rows[ts].items():
                        try:
                            fields[key] = convert_value(key, value)
                        except (TypeError, ValueError):
                            print(f"Bo qua gia tri khong hop le: {key}={value}")

                    if not fields:
                        continue

                    point = Point("sensor_data").tag(
                        "device_id", DEVICE_ID
                    ).time(ts, WritePrecision.MS)

                    for key, value in fields.items():
                        point = point.field(key, value)

                    write_api.write(
                        bucket=INFLUX_BUCKET,
                        org=INFLUX_ORG,
                        record=point,
                    )
                    count += 1

                if rows:
                    last_ts = max(rows)

                print(
                    f"{datetime.now().strftime('%H:%M:%S')} | "
                    f"Da luu {count} diem du lieu"
                )

            except requests.RequestException as exc:
                print("Loi ket noi ThingsBoard:", exc)
            except Exception as exc:
                print("Loi thu thap/ghi du lieu:", repr(exc))

            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDa dung collector.")
