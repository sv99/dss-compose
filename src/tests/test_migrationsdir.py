import unittest

from src.db_migrate import Migration, MigrationsDir
from src.config import Config


class TestMigrationDir(unittest.TestCase):

    def setUp(self):
        self.migrations_dir = "./migrations"
        self.md = MigrationsDir(self.migrations_dir)
        self.added_migrations = []

    def tearDown(self):
        if len(self.added_migrations) > 0:
            for m in self.added_migrations:
                self.md.remove(m)

    def test_get_all_migrations(self):
        self.assertNotEqual(0, len(self.md.migrations))

    def test_create(self):
        before_create = self.md.count()
        self.added_migrations.append(self.md.create("test-1"))
        self.added_migrations.append(self.md.create("test-2"))
        self.added_migrations.append(self.md.create("test-3"))
        self.assertEqual(before_create + 3, self.md.count())

    def test_interval(self):
        self.added_migrations.append(self.md.create("test-1"))
        self.added_migrations.append(self.md.create("test-2"))
        self.added_migrations.append(self.md.create("test-3"))
        # self.md.get_versions() = ['01', '02', '03', '04', '05']
        ms = self.md.get_from_version("03")
        self.assertEqual(2, len(ms))
        self.assertEqual("[04_test-2, 05_test-3]", repr(ms))
        ms = self.md.get_from_version("05")
        self.assertEqual(0, len(ms))
        ms = self.md.get_from_version("0")
        self.assertEqual(5, len(ms))
        self.assertEqual("[01_user, 02_table1, 03_test-1, 04_test-2, 05_test-3]", repr(ms))
        # check interval
        ms = self.md.get_interval("0", "03")
        self.assertEqual("[01_user, 02_table1, 03_test-1]", repr(ms))
        ms = self.md.get_interval("03", "0")
        self.assertEqual("[03_test-1, 02_table1, 01_user]", repr(ms))
        self.added_migrations.append(self.md.create("test-4"))
        ms = self.md.get_interval("03", "04")
        self.assertEqual("[04_test-2]", repr(ms))
        ms = self.md.get_interval("04", "05")
        self.assertEqual("[05_test-3]", repr(ms))
        # print(ms)


class TestMigration(unittest.TestCase):

    def test_is_file_name_valid(self):
        # check extension
        self.assertTrue(Migration.is_file_name_valid("20200419120801_init.sql"))
        self.assertTrue(Migration.is_file_name_valid("20200419120802_init.Sql"))
        self.assertTrue(Migration.is_file_name_valid("20200419120803_init.SQL"))
        # check version
        self.assertTrue(Migration.is_file_name_valid("01_init.sql"))
        self.assertFalse(Migration.is_file_name_valid("ss_init.sql"))


if __name__ == '__main__':
    unittest.main()
