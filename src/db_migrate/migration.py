import os
import re


class Migration(object):
    MIGRATION_FILES_EXTENSION = ".sql"
    MIGRATION_FILES_MASK = r"[0-9]+_[\w\-]+%s$" % MIGRATION_FILES_EXTENSION
    TEMPLATE = '--\n-- Up\n--\n\n\n--\n-- Down\n--\n\n\n'

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.file_name = os.path.basename(path)
        self.name = os.path.splitext(self.file_name)[0]
        self.version = self.get_file_version(self.file_name)
        if not Migration.is_file_name_valid(self.file_name):
            raise Exception('invalid migration file name (%s)' % self.file_name)
        if not os.path.isfile(self.path):
            raise Exception('migration file (%s) not exists' % self.file_name)
        with open(self.path, 'r', encoding="utf-8") as f:
            self.data = f.read()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def sql_up(self):
        sql = self.__get_command(0)
        if sql == "":
            raise Exception("migration command 'SQL_UP' is empty (%s)" % self.path)
        return sql

    @property
    def sql_down(self):
        return self.__get_command(1)

    def __get_command(self, index):
        try:
            parts = re.split(r"^--\s+?down\b", self.data, flags=re.M | re.I)

        except KeyError:
            raise Exception(
                "migration file is incorrect format; it does not define Up or Down section (%s)" % self.path)

        # remove comments
        return re.sub(r'^--.*?$', "", parts[index]).strip()

    @staticmethod
    def get_file_version(file_name):
        return file_name[0:file_name.find("_")]

    @staticmethod
    def is_file_name_valid(file_name):
        match = re.match(Migration.MIGRATION_FILES_MASK, file_name, re.IGNORECASE)
        return match is not None


# make Migration comparable
Migration.__eq__ = lambda self, other: self.name == other.name
Migration.__ne__ = lambda self, other: self.name != other.name
Migration.__lt__ = lambda self, other: self.name < other.name
Migration.__le__ = lambda self, other: self.name <= other.name
Migration.__gt__ = lambda self, other: self.name > other.name
Migration.__ge__ = lambda self, other: self.name >= other.name
