
def register_elastic_command(app, kb):
    @app.cli.command(short_help='refresh elastic cash')
    def elastic_refresh():
        """Refresh elasticsearch cache from database"""
        print(f'elastic_refresh command executed')
        kb.init_storage()