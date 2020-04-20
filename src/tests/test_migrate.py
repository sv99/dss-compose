import unittest

from src.db_migrate import Migrate
from src.config import Config


def get_config(drop=False):
    config = Config()
    config.database_name = "DSS_TEST"
    config.database_user = "root"
    config.database_password = "mysqlroot"
    config.drop_db_first = drop
    config.database_migrations_dir = "./migrations"
    return config


class TestMigrateDropDbFirst(unittest.TestCase):

    def setUp(self):
        self.config = get_config(True)
        self.migrate = Migrate(self.config)

    def tearDown(self):
        self.migrate.sgdb.drop_database()

    def test_get_versions(self):
        versions = self.migrate.sgdb.get_versions()
        # print(versions)
        self.assertEqual("[]", repr(versions))

    def test_get_version(self):
        version = self.migrate.sgdb.get_version()
        # print("version: ", version)
        self.assertEqual("0", version)

    def test_migrate_all(self):
        self.assertTrue(self.migrate.sgdb.is_table("db_migrate"))
        self.assertFalse(self.migrate.sgdb.is_table("user"))
        self.assertFalse(self.migrate.sgdb.is_table("table1"))
        self.migrate.migrate()
        self.assertEqual("02", self.migrate.sgdb.get_version())
        self.assertTrue(self.migrate.sgdb.is_table("user"))
        self.assertTrue(self.migrate.sgdb.is_table("table1"))

    def test_migrate(self):
        self.assertFalse(self.migrate.sgdb.is_table("user"))
        self.assertFalse(self.migrate.sgdb.is_table("table1"))
        self.migrate.migrate("01")
        self.assertEqual("01", self.migrate.sgdb.get_version())
        self.assertTrue(self.migrate.sgdb.is_table("user"))
        self.assertFalse(self.migrate.sgdb.is_table("table1"))

    def test_migrate_down(self):
        self.assertFalse(self.migrate.sgdb.is_table("user"))
        self.assertFalse(self.migrate.sgdb.is_table("table1"))
        self.migrate.migrate()
        self.assertEqual("02", self.migrate.sgdb.get_version())
        self.migrate.migrate("01")
        self.assertEqual("01", self.migrate.sgdb.get_version())
        self.assertTrue(self.migrate.sgdb.is_table("user"))
        self.assertFalse(self.migrate.sgdb.is_table("table1"))
        self.migrate.migrate("0")
        self.assertEqual("0", self.migrate.sgdb.get_version())
        self.assertFalse(self.migrate.sgdb.is_table("user"))
        self.assertFalse(self.migrate.sgdb.is_table("table1"))


if __name__ == '__main__':
    unittest.main()
