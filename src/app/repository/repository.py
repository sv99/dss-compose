from abc import ABC, abstractmethod


class Repository(ABC):
    db_name: str

    @staticmethod
    @abstractmethod
    def create_db(connection):
        pass

    @abstractmethod
    def is_db_empty(self):
        pass

    @abstractmethod
    def fill_storage_from_file(self, path):
        pass

    @abstractmethod
    def get_problem_id(self, problem):
        pass

    @abstractmethod
    def add_problem(self, problem):
        pass

    @abstractmethod
    def get_recommendation_id(self, recommendation):
        pass

    @abstractmethod
    def add_recommendation(self, recommendation):
        pass

    @abstractmethod
    def get_all_problems(self):
        pass

    @abstractmethod
    def get_recommendations_for_problem(self, problem_id):
        pass

    @abstractmethod
    def get_n_random_recommendations(self, n, recommendations_to_ignore):
        pass

    @abstractmethod
    def get_problem_recommendation_rating(self, problem, recommendation):
        pass

    @abstractmethod
    def update_problem_recommendation_rating(self, problem_id, recommendation_id, rating):
        pass

    @abstractmethod
    def add_problem_recommendation_rating(self, problem_id, recommendation_id, rating):
        pass
