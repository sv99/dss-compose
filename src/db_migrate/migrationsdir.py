import codecs
import os

from . import Migration


class MigrationsDir(object):
    def __init__(self, path):
        self.__migrations_dir = os.path.abspath(path)
        if not os.path.isdir(path):
            raise Exception('migration directory (%s) not exists' % path)
        self.__migrations = None

    @property
    def migrations(self):
        if self.__migrations:
            return self.__migrations

        migrations = []

        migrations_list = os.listdir(self.__migrations_dir)

        for item in migrations_list:
            if Migration.is_file_name_valid(item):
                migration = Migration(os.path.join(self.__migrations_dir, item))
                migrations.append(migration)

        if len(migrations) == 0:
            raise Exception("no found migration files")

        self.__migrations = sorted(migrations)
        return self.__migrations

    def count(self):
        return len(self.migrations)

    def get_last(self):
        return self.migrations[-1]

    def get_next_version(self):
        last = self.get_last().version
        ver_format = "{:0%dd}" % len(last)
        next_ver = ver_format.format(int(last) + 1)
        return next_ver

    def get_versions(self):
        return [migration.version for migration in self.migrations]

    def get_all(self):
        return [migration.name for migration in self.migrations]

    def get_all_migration_versions_up_to(self, limit_version):
        return [version for version in self.get_versions() if version < limit_version]

    def check_if_version_exists(self, version):
        return version in self.get_versions()

    def get_from_version(self, version):
        migrations = [migration for migration in self.migrations if migration.version > version]
        return migrations

    def get_interval(self, start, end):
        migrations = self.migrations.copy()
        if start < end:
            # Up
            return [m for m in migrations if start < m.version <= end ]
        else:
            # Down
            migrations = list(reversed(migrations))
            return [m for m in migrations if end < m.version <= start ]

    def create(self, migration_name):
        """creat empty migration from template"""
        # original version vith timestamp version format
        # timestamp = strftime("%Y%m%d%H%M%S", localtime())
        next_ver = self.get_next_version()
        file_name = "%s_%s%s" % (next_ver, migration_name, Migration.MIGRATION_FILES_EXTENSION)
        if not Migration.is_file_name_valid(file_name):
            raise Exception(
                "invalid migration name ('%s'); it should contain only letters, numbers and/or underscores"
                % file_name)

        new_file_name = os.path.join(self.__migrations_dir, file_name)

        try:
            f = codecs.open(new_file_name, "w", "utf-8")
            f.write(Migration.TEMPLATE)
            f.close()
        except IOError:
            raise Exception("could not create file ('%s')" % new_file_name)

        migration = Migration(new_file_name)
        self.__migrations.append(migration)
        return migration

    def remove(self, migration):
        """remove migration from directory"""
        if os.path.isfile(migration.path):
            self.__migrations.remove(migration)
            os.remove(migration.path)
