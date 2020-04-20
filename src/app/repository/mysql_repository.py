import mysql.connector as db
from contextlib import closing
from .repository import Repository


# noinspection SqlNoDataSourceInspection,SqlResolve
class MySQLRepository(Repository):
    def __init__(self, config):
        self.db_name = config.db_name
        # mysql connection params
        self.host = config.database_host
        self.database = config.database_name
        self.user = config.database_user
        self.password = config.database_password

    @staticmethod
    def create_db(connection):
        pass

    def is_db_empty(self):
        pass

    def fill_storage_from_file(self, path):
        pass

    def connect(self):
        try:
            conn = db.connection.MySQLConnection(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                ssl_disabled=True)
            return conn
        except Exception as e:
            raise Exception("could not connect: %s" % e)

    def get_problem_id(self, problem):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = 'SELECT problem_id FROM problem WHERE description = %s'
                cursor.execute(query, problem)
                problem = cursor.fetchone()
        return problem[0] if problem else None

    def add_problem(self, problem):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute('INSERT INTO problem (description) VALUES (?)', [problem])
            conn.commit()
        return cursor.lastrowid

    def get_recommendation_id(self, recommendation):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = 'SELECT recommendation_id FROM recommendation WHERE recommendation = ?'
                recommendation = cursor.execute(query, [recommendation]).fetchone()

        return recommendation[0] if recommendation else None

    def add_recommendation(self, recommendation):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = "SELECT recommendation from recommendation WHERE recommendation = '{}'"

                print("add_recommendation: ", query.format(recommendation))
                cursor.execute(query.format(recommendation))
                existing_recommendation = cursor.fetchall()

                if len(existing_recommendation) != 0:
                    return 1
                query = "INSERT INTO recommendation (recommendation) VALUES ('{}')"
                cursor.execute(query.format(recommendation))

            conn.commit()
        return 0

    def get_all_problems(self):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = 'SELECT problem_id, description FROM problem'
                problems = cursor.execute(query).fetchall()

        return problems

    def get_recommendations_for_problem(self, problem_id):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = f'SELECT recommendation.recommendation_id, recommendation, rating FROM problem' \
                        f'  INNER JOIN problem_recommendation' \
                        f'      ON problem.problem_id = problem_recommendation.problem_id' \
                        f'  INNER JOIN recommendation' \
                        f'      ON problem_recommendation.recommendation_id = recommendation.recommendation_id' \
                        f' WHERE problem.problem_id = {problem_id}'
                cursor.execute(query)
                recommendations = cursor.fetchall()

        # Sort by rating descending
        recommendations.sort(key=lambda item: item[2], reverse=True)

        return [item[1] for item in recommendations]

    def get_n_random_recommendations(self, n, recommendations_to_ignore):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                # Ignore already selected recommendations to avoid duplicates
                if len(recommendations_to_ignore) > 0:
                    ignore = ', '.join([f'\'{str(item)}\'' for item in recommendations_to_ignore])
                    # query = f'SELECT * FROM recommendation WHERE recommendation_id IN' \
                    #         f'   (SELECT recommendation_id FROM recommendation' \
                    #         f'      WHERE recommendation NOT IN ({ignore})' \
                    #         f'      ORDER BY RANDOM() LIMIT {n});'
                    query = """SELECT * FROM recommendation as r1
                                INNER JOIN
                                    (SELECT recommendation_id
                                     FROM recommendation
                                     WHERE recomendation NOT IN ({}})
                                     ORDER BY RAND() LIMIT {}) as r2
                                ON r1.recommendation_id = r2.recommendation_id;""".format(
                                    ignore, n)
                else:
                    # query = """SELECT * FROM recommendation WHERE recommendation_id IN
                    #              (SELECT recommendation_id FROM recommendation
                    #                 ORDER BY RANDOM() LIMIT {n});"""
                    query = """SELECT * FROM recommendation as r1
                                INNER JOIN
                                    (SELECT recommendation_id
                                    FROM recommendation
                                        ORDER BY RAND() LIMIT {}) as r2
                                ON r1.recommendation_id = r2.recommendation_id""".format(n)
                print(query)
                cursor.execute(query)
                recommendations = cursor.fetchall()

        return [item[1] for item in recommendations]

    def get_problem_recommendation_rating(self, problem, recommendation):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = """SELECT rating FROM problem
                           INNER JOIN problem_recommendation
                             ON problem.problem_id = problem_recommendation.problem_id
                           INNER JOIN recommendation
                             ON recommendation.recommendation_id = problem_recommendation.recommendation_id
                           WHERE description = '%s' AND recommendation = '%s'"""
                params = (problem, recommendation)
                cursor.execute(query, params)
                rating = cursor.fetchone()

        return rating[0] if rating else None

    def update_problem_recommendation_rating(self, problem_id, recommendation_id, rating):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = f'UPDATE problem_recommendation SET rating = {rating}' \
                        f'  WHERE problem_id = {problem_id} AND recommendation_id = {recommendation_id}'
                cursor.execute(query)
        conn.commit()

    def add_problem_recommendation_rating(self, problem_id, recommendation_id, rating):
        with closing(self.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                query = f'INSERT INTO problem_recommendation VALUES' \
                        f'  ({problem_id}, {recommendation_id}, {rating})'
                cursor.execute(query)
            conn.commit()
