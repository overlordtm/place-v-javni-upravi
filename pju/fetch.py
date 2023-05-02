import urllib3
import pandas as pd
import json
import html
from . import __version__

BASE_URL = "http://www.pportal.gov.si"

# Create a pool manager to handle multiple requests
http = urllib3.PoolManager()
http.headers["User-Agent"] = f"pju/{__version__}"


def fetch_payouts() -> pd.DataFrame:
    COLS = ["date", "employees_by_hours", "employees", "employees_all", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "L", "N", "O"]

    df = pd.DataFrame()
    r = http.request("GET", f"{BASE_URL}/tipimesec.txt")
    df = pd.DataFrame(json.loads(r.data)["aaData"], columns=COLS)

    df[["employees_by_hours", "employees", "employees_all", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "L", "N", "O"]] = df[["employees_by_hours", "employees", "employees_all", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "L", "N", "O"]].apply(lambda col: col.str.replace(".", "", regex=False).astype(int))

    df["month_year"] = pd.to_datetime(df["date"], format="%m.%Y").dt.to_period("M")
    df.drop("date", axis=1, inplace=True)
    df.set_index("month_year", inplace=True)
    df.sort_index(inplace=True)

    return df

def fetch_payout_by_budget_user_group(year: int, month: int) -> pd.DataFrame:
    data = []

    for i in range(1, 24):
        r = http.request("GET",  f"{BASE_URL}/ISPAP_{year}/{month}_{year}/POD/{i}_POD_VSOTE_VRST{month}.txt")
        data.append(dict(list(map(lambda row: row.split(":"), r.data.decode("utf-8").splitlines()))))

    df = pd.DataFrame.from_records(data, index="POD")
    df.index = df.index.str.strip()
    df.index.rename
    ]=-65w("group_id", inplace=True)
    df.rename(columns={"Z360": "employees"}, inplace=True)
    df = df.apply(lambda col: col.str.replace(".", "", regex=False).astype(int), axis=1)
    df.insert(0, "month_year", pd.to_datetime(f"{year}-{month}").to_period("M"))

    return df

def fetch_payout_by_budget_user(year: int, month: int) -> pd.DataFrame:
    COLS = ["group_id", "budget_user_id", "budget_user_name", "employees", "gross_salary", "NA1", "C", "NA2", "D", "NA3", "E", "NA4", "NA5","NA6", "I", "NA7", "J", "NA8", "O", "NA9"]
    r = http.request("GET",  f"{BASE_URL}/ISPAP_{year}/{month}_{year}/PU/PU_POVPRECJE_{month}.txt")

    df = pd.DataFrame(json.loads(html.unescape(r.data.decode("iso-8859-2")))["aaData"], columns=COLS)

    df[["group_id", "group_name"]] = df["group_id"].str.split(" ", n=1, expand=True)
    df["budget_user_id"] = df["budget_user_id"].str.strip().astype(int)
    df["budget_user_name"] = df["budget_user_name"].str.strip().astype(str)
    df["employees"] = df["employees"].str.replace(".", "", regex=False).astype(int)
    df["gross_salary"] = df["gross_salary"].str.replace(".", "", regex=False).astype(int)

    df.set_index("budget_user_id", inplace=True)
    df.insert(0, "month_year", pd.to_datetime(f"{year}-{month}").to_period("M"))

    return df

def fetch_payouts_job_title(year: int, month: int) -> pd.DataFrame:
    COLS = ["group", "budget_user_id", "budget_user_name", "job_title_id", "job_title" ,"employees","gross_salary","C","D","E","F","I","J","O"]
    r = http.request("GET",  f"{BASE_URL}/ISPAP_{year}/{month}_{year}/DM/DM_VSI_BRUTOPLACA{month}.txt")

    df = pd.DataFrame(json.loads(html.unescape(r.data.decode("iso-8859-2")))["aaData"], columns=COLS)

    df[["employees", "gross_salary", "C", "D", "E", "F", "I", "J", "O"]] = df[["employees", "gross_salary", "C", "D", "E", "F", "I", "J", "O"]].apply(lambda col: col.str.replace(".", "", regex=False).astype(int))

    df.insert(0, "month_year", pd.to_datetime(f"{year}-{month}").to_period("M"))
    df.set_index("job_title_id", inplace=True)
    return df