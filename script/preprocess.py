
import pandas as pd
from influxdb_client import InfluxDBClient

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "V93k4_TKJAyKVxWwFtDnz2yYjrBqB4fs6HG-QAgiG6RZMtAkm2gCDMOwZmEt3VRpo3Uug-k7LhO4N6f2_-flKQ=="
INFLUX_ORG = "PTIT"
INFLUX_BUCKET = "iot_data"

SENSOR_COLUMNS = ["temperature", "humidity", "distance_cm"]


def main():
    with InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG,
    ) as client:

        query = f'''
        from(bucket: "{INFLUX_BUCKET}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "sensor_data")
          |> filter(fn: (r) =>
              r._field == "temperature" or
              r._field == "humidity" or
              r._field == "distance_cm"
          )
        '''

        tables = client.query_api().query(query, org=INFLUX_ORG)

        rows = []
        for table in tables:
            for record in table.records:
                rows.append({
                    "time": record.get_time(),
                    "field": record.get_field(),
                    "value": record.get_value(),
                })

    if not rows:
        print("Chua co du lieu. Hay chay collector.py truoc.")
        return

    df = pd.DataFrame(rows)
    df = df.pivot_table(
        index="time",
        columns="field",
        values="value",
        aggfunc="last",
    ).sort_index()

    for col in SENSOR_COLUMNS:
        if col not in df.columns:
            df[col] = float("nan")

    df = df[SENSOR_COLUMNS].apply(pd.to_numeric, errors="coerce")

    resampled = df.resample("10s").mean()

    cleaned = resampled.copy()

    for col in SENSOR_COLUMNS:
        series = cleaned[col].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        mask = (cleaned[col] < lower) | (cleaned[col] > upper)
        cleaned.loc[mask, col] = float("nan")

    cleaned = cleaned.interpolate(
        method="time",
        limit=2,
        limit_area="inside",
    )

    for col in SENSOR_COLUMNS:
        cleaned[f"{col}_rolling_mean"] = (
            cleaned[col].rolling(window=3, min_periods=1).mean()
        )

    normalized = cleaned[SENSOR_COLUMNS].copy()

    for col in SENSOR_COLUMNS:
        min_val = normalized[col].min()
        max_val = normalized[col].max()

        if pd.isna(min_val) or pd.isna(max_val):
            normalized[f"{col}_norm"] = float("nan")
        elif max_val == min_val:
            normalized[f"{col}_norm"] = 0.0
        else:
            normalized[f"{col}_norm"] = (
                (normalized[col] - min_val) / (max_val - min_val)
            )

    result = pd.concat(
        [
            cleaned,
            normalized[[f"{c}_norm" for c in SENSOR_COLUMNS]],
        ],
        axis=1,
    )

    result.to_csv(
        "iot_processed.csv",
        index_label="time",
        encoding="utf-8-sig",
    )

    print("Da tien xu ly xong.")
    print("So dong truoc lay mau:", len(df))
    print("So dong sau lay mau:", len(resampled))
    print("File ket qua: iot_processed.csv")
    print(result.tail(10))


if __name__ == "__main__":
    main()