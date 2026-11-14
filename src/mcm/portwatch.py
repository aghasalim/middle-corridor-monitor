"""Download IMF PortWatch daily port data (ArcGIS feature service) to data/portwatch/.

Sources: Kpler; UN Global Platform; IMF PortWatch (portwatch.imf.org).
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

URL = ("https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/"
       "Daily_Ports_Data/FeatureServer/0/query")
PORTS = {"port100": "Baku", "port16": "Aktau", "port1330": "Turkmenbashi",
         "port1016": "Poti", "port127": "Batumi"}
SUFFIXES = ["container", "dry_bulk", "general_cargo", "roro", "tanker", "cargo"]
FIELDS = (["date", "portid", "portname", "portcalls"]
          + [f"portcalls_{s}" for s in SUFFIXES]
          + [f"{d}_{s}" for d in ("import", "export") for s in SUFFIXES])
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "portwatch"
PAGE = 1000


def fetch_port(portid):
    """All daily rows for one port, as a DataFrame with a UTC `date` column."""
    rows, offset = [], 0
    while True:
        r = requests.get(URL, timeout=60, params={
            "where": f"portid='{portid}'", "outFields": ",".join(FIELDS),
            "orderByFields": "date", "resultOffset": offset,
            "resultRecordCount": PAGE, "f": "json"})
        r.raise_for_status()
        js = r.json()
        if "error" in js:
            raise RuntimeError(f"{portid}: ArcGIS error {js['error']}")
        feats = js.get("features", [])
        rows += [f["attributes"] for f in feats]
        if len(feats) < PAGE and not js.get("exceededTransferLimit"):
            break
        offset += len(feats)
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"{portid}: no rows returned")
    # the service returns DateOnly as "YYYY-MM-DD"; older layers used epoch ms UTC
    numeric = pd.api.types.is_numeric_dtype(df["date"])
    df["date"] = pd.to_datetime(df["date"], unit="ms" if numeric else None, utc=True).dt.tz_localize(None).dt.normalize()
    return df[FIELDS].sort_values("date").reset_index(drop=True)


def check_daily(df, portid):
    """Fail loudly unless there is exactly one row per day with no gaps."""
    dup = df["date"].duplicated()
    if dup.any():
        raise ValueError(f"{portid}: {dup.sum()} duplicated dates, e.g. {df.loc[dup, 'date'].iloc[0].date()}")
    full = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    missing = full.difference(df["date"])
    if len(missing):
        raise ValueError(f"{portid}: {len(missing)} missing days, first {missing[0].date()}")
    if df["date"].min() > pd.Timestamp("2019-01-01"):
        raise ValueError(f"{portid}: short download, starts {df['date'].min().date()}")


def download(data_dir=DATA_DIR):
    data_dir.mkdir(parents=True, exist_ok=True)
    snap = {"downloaded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": URL, "citation": "Sources: Kpler; UN Global Platform; IMF PortWatch (portwatch.imf.org).",
            "ports": {}}
    for pid, name in PORTS.items():
        df = fetch_port(pid)
        check_daily(df, pid)
        df.to_csv(data_dir / f"daily_{pid}.csv", index=False)
        snap["ports"][pid] = {"name": name, "rows": len(df),
                              "first": str(df["date"].min().date()), "last": str(df["date"].max().date())}
        print(f"{pid} {name}: {len(df)} rows {snap['ports'][pid]['first']}..{snap['ports'][pid]['last']}")
    (data_dir / "snapshot.json").write_text(json.dumps(snap, indent=2))
    return snap


def load(data_dir=DATA_DIR):
    """Saved daily files -> {portid: DataFrame}, re-checked."""
    out = {}
    for pid in PORTS:
        df = pd.read_csv(data_dir / f"daily_{pid}.csv", parse_dates=["date"])
        check_daily(df, pid)
        out[pid] = df
    return out


if __name__ == "__main__":
    download()
