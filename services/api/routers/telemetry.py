import os

from fastapi import APIRouter, Depends
from influxdb_client import InfluxDBClient

from ..deps import oidc_guard

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.get("/series")
async def series(signal: str, start: str = "-1h", stop: str = "now()", user=Depends(oidc_guard)):
    client = InfluxDBClient(
        url=os.getenv("INFLUX_URL"),
        token=os.getenv("INFLUX_TOKEN"),
        org=os.getenv("INFLUX_ORG"),
    )
    query = (
        f'from(bucket:"{os.getenv("INFLUX_BUCKET")}") '
        f"|> range(start: {start}, stop: {stop}) "
        f"|> filter(fn: (r) => r[\"_measurement\"] == \"opcua\" and r[\"_field\"] == \"{signal}\")"
    )
    tables = client.query_api().query(query)
    points = []
    for table in tables:
        for record in table.records:
            points.append({"ts": record.get_time().isoformat(), "value": record.get_value()})
    return {"signal": signal, "points": points}

