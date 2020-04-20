# Decision Support System

Basic structure implemented. There're three API methods:
1. /GetRecommendation: gets problem description in log or stdout text format
and returns recommendations sorted by relevance (rating).  
2. /RateRecommendation: gets problem, recommendation and "did helped" flag
and tunes problem->recommendation rating (compliance rate).  
3. /AddRecommendation: gets recommendation and saves it to knowledge base.  

API documentation is powered by OpenAPI Swagger.  
![](demo/swagger.png)

## Flask app

Database connectors: `sqlite3` and
[mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html) 

[click](https://click.palletsprojects.com/en/7.x/) for command line interface
 
## docker-compose
 
Start 4 container
1. `nginx`
2. `elastic`
3. `mysql`
4. `app` - Flask app start with uwsgi and 30 sec delay for completely start elasticsearch.
Without delay elasticsearch not started properly and flask app crash with multiple errors.

`mysql` and `app` used common environment file `mysql.env` for define
container variables.

## scripts

`app_flask_cmd.sh` - для выплнения flask команд в контейнене app

```bash
# shell in app
docker-compose exec app bash
# list available flask command
docker-compose exec app flask --help
./app_flask_cmd.sh --help
# migrate to last migration
./app_flask_cmd.sh db migrate
# current database migration version
./app_flask_cmd.sh db version
# update elastic cache from database
./app_flask_cmd.sh elastic-refresh
```

```bash
# access to mysql shell
docker-compose exec mysql mysql -pmysqlroot
```

## cold start

```bash
docker-compose up
# wait 30 sec
./app_flask_cmd.sh db migrate
./app_flask_cmd.sh elastic-refresh
```