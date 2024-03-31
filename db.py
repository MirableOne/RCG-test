import psycopg2 as pg


class DBClient:
    def __init__(
            self,
            host: str,
            user: str,
            password: str,
            db_name: str,
            port: str = '5432'
    ):
        self.engine = pg.connect(
            f"dbname='{db_name}' user='{user}' host='{host}' port='{port}' password='{password}'"
        )

    def insert_timezone(self, params):
        cur = self.engine.cursor()

        sql = """
        INSERT INTO tzdb_timezones(country_code, country_name, zone_name, gmt_offset) 
        VALUES(%s, %s, %s, %s);
        """

        cur.execute(
            sql,
            (params['countryCode'], params['countryName'], params['zoneName'], int(params['gmtOffset']),)
        )

        self.engine.commit()
        cur.close()

    def upsert_timezone_details(self, params):
        cur = self.engine.cursor()

        sql = """
                INSERT INTO tzdb_zone_details(
                    country_code, country_name, zone_name, gmt_offset, dst, zone_start, zone_end
                ) 
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """

        cur.execute(
            sql,
            (
                params['countryCode'],
                params['countryName'],
                params['zoneName'],
                int(params['gmtOffset']),
                int(params['dst']),
                int(params['zoneStart'] or 0),
                int(params['zoneEnd'] or 0),
            )
        )

        self.engine.commit()
        cur.close()

    def truncate_timezones(self):
        cur = self.engine.cursor()

        cur.execute("TRUNCATE TABLE tzdb_timezones")

        self.engine.commit()
        cur.close()

    def log_error(self, message: str):
        cur = self.engine.cursor()

        cur.execute("INSERT INTO tzdb_error_log(error_message) VALUES(%s);", (message,))

        self.engine.commit()
        cur.close()
