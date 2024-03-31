import os
import time

import requests
from client import Client
from db import DBClient


def grabber(client: Client, db: DBClient):
    timezones = []
    try:
        timezones = client.get_timezones()
    except Exception as ex:
        db.log_error(str(ex))
        print(str(ex))

    time.sleep(1)
    db.truncate_timezones()

    for timezone in timezones:
        try:
            timezone_details = client.get_timezone_details(timezone['zoneName'])

            db.insert_timezone(timezone)
            db.upsert_timezone_details(timezone_details)
        except Exception as ex:
            db.log_error(str(ex))
            print(str(ex))

        time.sleep(1)


def main():
    client = Client(
        os.environ.get("API_ENDPOINT", ""),
        os.environ.get("API_KEY", ""),
    )

    db = DBClient(
        os.environ.get("DB_HOST", ""),
        os.environ.get("DB_USER", ""),
        os.environ.get("DB_PASS", ""),
        os.environ.get("DB_NAME", ""),
    )

    grabber(client, db)


if __name__ == '__main__':
    main()
