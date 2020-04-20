import click
from flask.cli import AppGroup


def add_db_command(migrate_dir):
    db_cli = AppGroup('db', short_help='working with database migration')

    @db_cli.command(short_help='migrate database')
    @click.argument('version', default="last")
    def migrate(version):
        """Migrate database"""
        print(f'migrate command executed with arg: {version}')
        migrate_dir.migrate(version)

    @db_cli.command("version", short_help='get current version')
    def get_version():
        """Get current version"""
        res = migrate_dir.get_current()
        print(f"Get current version {res}")
        return res

    return db_cli


