# combine from migrate and simple-db-migrate
# load migration.sql from ./migrations directory
from contextlib import closing
import mysql.connector as db


# noinspection SqlNoDataSourceInspection
class MySQL(object):
    def __init__(self, config):
        self.mysql_host = config.get("database_host")
        self.mysql_port = config.get("database_port", 3306)
        self.mysql_user = config.get("database_user")
        self.mysql_passwd = config.get("database_password")
        self.mysql_database = config.get("database_name")
        self.version_table = config.get("database_version_table", "db_migrate")

    def connect(self, with_database=True):
        try:
            database = with_database and self.mysql_database or None
            conn = db.connection.MySQLConnection(host=self.mysql_host,
                                                 port=self.mysql_port,
                                                 user=self.mysql_user,
                                                 passwd=self.mysql_passwd,
                                                 database=database,
                                                 ssl_disabled=True)
            return conn
        except Exception as e:
            raise Exception("could not connect: %s" % e)

    def __execute(self, sql):
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            try:
                for _ in cursor.execute(sql, multi=True):
                    pass
                cursor.close()
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise Exception("Error executing: %s" % e)

    def __change_db_version(self, migration, up=True):
        if up:
            # moving up and storing history
            sql = """INSERT INTO {} (version, name)
             VALUES ('{}', '{}');""".format(self.version_table,
                                            migration.version,
                                            migration.name)
        else:
            # moving down and deleting from history
            sql = """DELETE FROM {} WHERE name = '{}';""".format(
                self.version_table, migration.name)

        self.__execute(sql)

    def drop_database(self):
        with closing(self.connect(False)) as conn:
             with closing(conn.cursor()) as cursor:
                try:
                    for result in cursor.execute(
                            "set foreign_key_checks=0; drop database if exists `%s`;" % self.mysql_database,
                            multi=True):
                        pass
                        # print(result.statement, result.rowcount)
                except Exception as e:
                    raise Exception("can't drop database '%s'; \n%s" % (self.mysql_database, str(e)))

    def create_database_if_not_exists(self):
        with closing(self.connect(False)) as conn:
            with closing(conn.cursor()) as cursor:
                try:
                    cursor.execute(
                        "CREATE DATABASE IF NOT EXISTS `{}` DEFAULT CHARACTER SET 'utf8';".format(self.mysql_database))
                except Exception as e:
                    raise Exception("Can't create database '%s'; \n%s" % (self.mysql_database, str(e)))

    def create_version_table_if_not_exists(self):
        # create version table
        sql = """CREATE TABLE if not exists {} (
                    id int(11) NOT NULL AUTO_INCREMENT,
                    version varchar(20) NOT NULL default '0',
                    name varchar(255),
                    applied TIMESTAMP,
                    PRIMARY KEY (id));""".format(self.version_table)
        self.__execute(sql)

    def change(self, migration, up=True):
        self.create_version_table_if_not_exists()
        sql = up and migration.sql_up or migration.sql_down
        self.__execute(sql)
        self.__change_db_version(migration, up)

    def get_version(self):
        self.create_version_table_if_not_exists()
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("select version from %s order by id desc limit 1;" % self.version_table)
                version = cursor.fetchone()
        return version is None and "0" or version[0]

    def get_versions(self):
        result = []
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("select version from %s order by id;" % self.version_table)
                all_versions = cursor.fetchall()
                for version in all_versions:
                    result.append(version)
        return result

    def get_all(self):
        result = []
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("select name from %s order by id;" % self.version_table)
                all_versions = cursor.fetchall()
                for version in all_versions:
                    result.append(version)
        return result

    def is_table(self, name):
        """check is table exists, for testing perposes """
        result = True
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = '{}'
                    AND table_name = '{}';""".format(self.mysql_database, name))
                result = cursor.fetchone() is not None
        return result
