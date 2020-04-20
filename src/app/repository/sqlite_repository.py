import sqlite3
from contextlib import closing
from .repository import Repository


class SQLiteRepository(Repository):
    def __init__(self, config):
        self.db_name = config.db_name

        conn = sqlite3.connect(self.db_name)
        self.create_db(conn)

    @staticmethod
    def create_db(connection):
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS problem ('
            '   problem_id INTEGER PRIMARY KEY,'
            '   description TEXT NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS recommendation ('
            '   recommendation_id INTEGER PRIMARY KEY,'
            '   recommendation TEXT NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS problem_recommendation ('
            '   problem_id INTEGER,'
            '   recommendation_id INTEGER,'
            '   rating INTEGER NOT NULL DEFAULT 0,'
            '   PRIMARY KEY (problem_id, recommendation_id),'
            '   FOREIGN KEY (problem_id)'
            '       REFERENCES problem (problem_id)'
            '           ON DELETE CASCADE ON UPDATE CASCADE,'
            '   FOREIGN KEY (recommendation_id)'
            '       REFERENCES recommendation (recommendation_id)'
            '           ON DELETE CASCADE ON UPDATE CASCADE)'
        )
        cursor.close()

    def is_db_empty(self):
        problems = self.get_all_problems()
        return len(problems) == 0

    def fill_storage_from_file(self, path):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                with open(path, 'r') as f:
                    cursor.executescript(f.read())

            conn.commit()

    def get_problem_id(self, problem):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = 'SELECT problem_id FROM problem WHERE description = ?'
                problem = cursor.execute(query, [problem]).fetchone()

        return problem[0] if problem else None

    def add_problem(self, problem):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute('INSERT INTO problem VALUES (NULL, ?)', [problem])

                conn.commit()
                return cursor.lastrowid

    def get_recommendation_id(self, recommendation):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = 'SELECT recommendation_id FROM recommendation WHERE recommendation = ?'
                recommendation = cursor.execute(query, [recommendation]).fetchone()

        return recommendation[0] if recommendation else None

    def add_recommendation(self, recommendation):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = 'SELECT * from recommendation WHERE recommendation = ?'
                existing_recommendation = cursor.execute(query, [recommendation]).fetchall()

                if len(existing_recommendation) != 0:
                    return 1

                cursor.execute('INSERT INTO recommendation VALUES (NULL, ?)', [recommendation])

            conn.commit()
        return 0

    def get_all_problems(self):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = 'SELECT * FROM problem'
                problems = cursor.execute(query).fetchall()

        return problems

    def get_recommendations_for_problem(self, problem_id):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = f'SELECT recommendation.recommendation_id, recommendation, rating FROM problem' \
                        f'  INNER JOIN problem_recommendation' \
                        f'      ON problem.problem_id = problem_recommendation.problem_id' \
                        f'  INNER JOIN recommendation' \
                        f'      ON problem_recommendation.recommendation_id = recommendation.recommendation_id' \
                        f' WHERE problem.problem_id = {problem_id}'
                recommendations = cursor.execute(query).fetchall()

        # Sort by rating descending
        recommendations.sort(key=lambda item: item[2], reverse=True)

        return [item[1] for item in recommendations]

    def get_n_random_recommendations(self, n, recommendations_to_ignore):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                # Ignore already selected recommendations to avoid duplicates
                if len(recommendations_to_ignore) > 0:
                    ignore = ', '.join([f'\'{str(item)}\'' for item in recommendations_to_ignore])
                    query = f'SELECT * FROM recommendation WHERE recommendation_id IN' \
                            f'   (SELECT recommendation_id FROM recommendation' \
                            f'      WHERE recommendation NOT IN ({ignore})' \
                            f'      ORDER BY RANDOM() LIMIT {n})'
                else:
                    query = f'SELECT * FROM recommendation WHERE recommendation_id IN' \
                            f'   (SELECT recommendation_id FROM recommendation' \
                            f'      ORDER BY RANDOM() LIMIT {n})'

                recommendations = cursor.execute(query).fetchall()

        return [item[1] for item in recommendations]

    def get_problem_recommendation_rating(self, problem, recommendation):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = f'SELECT rating FROM problem' \
                        f' INNER JOIN problem_recommendation' \
                        f'  ON problem.problem_id = problem_recommendation.problem_id ' \
                        f' INNER JOIN recommendation ' \
                        f'  ON recommendation.recommendation_id = problem_recommendation.recommendation_id' \
                        f'    WHERE description = ? AND recommendation = ?'
                params = [problem, recommendation]
                rating = cursor.execute(query, params).fetchone()

        return rating[0] if rating else None

    def update_problem_recommendation_rating(self, problem_id, recommendation_id, rating):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = f'UPDATE problem_recommendation SET rating = {rating}' \
                        f'  WHERE problem_id = {problem_id} AND recommendation_id = {recommendation_id}'
                cursor.execute(query)

            conn.commit()

    def add_problem_recommendation_rating(self, problem_id, recommendation_id, rating):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                query = f'INSERT INTO problem_recommendation VALUES' \
                        f'  ({problem_id}, {recommendation_id}, {rating})'
                cursor.execute(query)

            conn.commit()
