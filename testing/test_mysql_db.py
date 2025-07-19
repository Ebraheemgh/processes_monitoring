import unittest

from process_monitor.helper_functions import load_config
from process_monitor.mysql_db import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config("../process_monitor/config.json")['db']
        cls.db = DatabaseManager(cls.config)
        cls.table_name_to_create = "Testing_Table"

    def setUp(self):
        self.db.connect()

    def tearDown(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Failed to close connection: {e}")

    def test_connection(self):
        assert self.db.connection is not None, "Connection is Failed"

    def test_close_connection(self):
        self.db = DatabaseManager(self.config)
        self.db.close()
        assert self.db.connection is None, "Connection is not closed"

    def test_execute_and_commit(self):
        self.db.execute(f"DROP TABLE IF EXISTS {self.table_name_to_create}")

        create_table_query = """
                   CREATE TABLE IF NOT EXISTS {} (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(255)
                   )
               """.format(self.table_name_to_create)
        self.db.execute(create_table_query)
        self.db.commit()
        assert self.table_name_to_create in self.db.get_all_tables(), "Table not created , execute and commit not working"
        assert True


if __name__ == '__main__':
    unittest.main()
