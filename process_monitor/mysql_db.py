import mysql.connector


class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.db_config["host"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                database=self.db_config["database"]
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            raise

    def execute(self, sql, values=None):
        try:
            self.cursor.execute(sql, values)
        except mysql.connector.Error as err:
            raise

    def commit(self):
        if self.connection:
            self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def query(self, sql, values=None):
        try:
            self.cursor.execute(sql, values)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            raise

    def insert_summary_data(self, data):
        sql = """
            INSERT INTO processes_summary
            (`PID`, `PROCESS_NAME`, `Average_CPU`, `Average_Memory`, `start_monitoring`, `end_monitoring`)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        for index, row in data.iterrows():
            values = (
                str(row['process_id']),
                row['process_name'],
                row['Average CPU %'],
                row['Average Memory (MB)'],
                row['start_time'],
                row['end_time'],
            )
            self.execute(sql, values)

    def get_all_tables(self):
        results = self.query("SHOW TABLES")
        return [row[0] for row in results]
