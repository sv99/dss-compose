import logging

from . import MigrationsDir, MySQL

"""
The sgbd class should implement the following methods
- change(self, migration, up=True)
  executes the migration (up or down) and records the change on version table
- get_all_schema_migrations(self)
  return all migrations saved on version table
- get_all_schema_versions(self)
  return all versions saved on version table
- get_current_schema_version(self)
  return the current schema version
- get_version_id_from_version_number(self, version)
  return the id from an specific version
"""

# consts for color log output
PINK = "\033[35m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
END = "\033[0m"


class Migrate(object):
    def __init__(self, config, sgdb=None):
        Migrate._check_configuration(config)

        self.config = config
        self.log = logging.getLogger()
        self.log_level = 1

        self.migrations_dir = MigrationsDir(self.config.get("database_migrations_dir"))

        self.sgdb = MySQL(config)
        if config.get("drop_db_first", False):
            self.sgdb.drop_database()

        # self.sgdb.create_database_if_not_exists()
        # self.sgdb.create_version_table_if_not_exists()

    @staticmethod
    def msg(msg, color):
        print("{}{}{}".format(color, msg, END))

    def execution_log(self, msg, color=None, log_level_limit=2):
        if color is None:
            color = CYAN
        if self.log_level >= log_level_limit:
            # CLI.msg(msg, color)
            self.log.debug(msg, color)

    @staticmethod
    def _check_configuration(config):

        required_configs = ['database_host', 'database_name', 'database_user', 'database_password',
                            'database_migrations_dir', 'database_engine']

        for key in required_configs:
            # check if config has the key, if do not have will raise exception
            config.get(key)

    def migrate(self, version="last"):
        # check if a version was passed to the program
        # didn't pass a version -> do migrations up until the last available version
        if version == "last":
            version = self.migrations_dir.get_last().version
        current_version = self.sgdb.get_version()

        # do it!
        if current_version != version:
            self.execution_log('\nStarting DB migration on host/database "%s/%s" with user "%s"...' %
                               (self.config.get('database_host'), self.config.get('database_name'),
                                self.config.get('database_user')), PINK, log_level_limit=1)
            self.execute_migrations(current_version, version)
            self.execution_log("\nDone.\n", PINK, log_level_limit=1)
        else:
            self.execution_log("- Destination version is: %s" % current_version, GREEN, log_level_limit=1)
            self.execution_log("\nNothing to do.\n", PINK, log_level_limit=1)

    def get_current(self):
        return self.sgdb.get_version()

    def get_all(self):
        return self.sgdb.get_all()

    def get_all_from_dir(self):
        return self.migrations_dir.get_all()

    def execute_migrations(self, current_version, destination_version):

        is_migration_up = current_version < destination_version
        up_down_label = is_migration_up and "up" or "down"

        migrations = self.migrations_dir.get_interval(current_version, destination_version)
        if len(migrations) == 0:
            raise Exception(
                "Not found migrations for migrate from (%s) to (%s)" % (current_version, destination_version))

        self.execution_log("- Current version is: %s" % current_version, GREEN, log_level_limit=1)
        self.execution_log("- Destination version is: %s" % destination_version, GREEN, log_level_limit=1)

        if self.config.get("show_sql_only", False):
            self.execution_log("\nWARNING: database migrations are not being executed ('--showsqlonly' activated)",
                               YELLOW, log_level_limit=1)
        else:
            self.execution_log("\nStarting migration %s!" % up_down_label, log_level_limit=1)

        self.execution_log("*** versions: %s\n" % ([m.version for m in migrations]),
                           CYAN, log_level_limit=1)

        for m in migrations:
            if not self.config.get("show_sql_only", False):
                self.execution_log("===== executing %s (%s) =====" % (m.file_name, up_down_label),
                                   log_level_limit=1)
                try:
                    self.sgdb.change(m, is_migration_up)
                except Exception as e:
                    self.execution_log("===== ERROR executing %s (%s) =====" % (m.path, up_down_label),
                                       log_level_limit=1)
                    raise e

            if self.config.get("show_sql", False) or self.config.get("show_sql_only", False):
                self.execution_log("__________ SQL statements executed __________",
                                   YELLOW, log_level_limit=1)
                sql = is_migration_up and m.sql_up or m.sql_down
                for line in sql:
                    self.execution_log(line, YELLOW, log_level_limit=1)
                self.execution_log("_____________________________________________",
                                   YELLOW, log_level_limit=1)
