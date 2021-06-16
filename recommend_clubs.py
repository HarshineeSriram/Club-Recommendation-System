import json
import collections
from collections import Counter, OrderedDict
import numpy as np
import pandas as pd
from ast import literal_eval


class recommendations:
    def __init__(self) -> None:
        # Loading initial files and variables
        print("\n 1) Loading initial data. . .")
        initial_parameters = open(r'initial_parameters.json')
        initial_parameters = json.load(initial_parameters)
        self.all_clubs_similarity = pd.read_csv(
            './generated_csv_files/2_clubs_similarity.csv')
        self.complete_details = pd.read_csv(
            './generated_csv_files/1_student_all_interests.csv')
        f_clubs = open(initial_parameters['paths']['path_to_all_clubs'],)
        data_clubs = json.load(f_clubs)
        self.number_of_clubs = len(data_clubs)
        self.club_titles = [data_clubs[i]['title'] for i in range(
            self.number_of_clubs)]
        self.number_of_students = initial_parameters['number_of_students']
        self.hash_keys = self.complete_details['hash_key']

    def generate_similarity_index(self) -> None:
        print("\n 2) Generating similarity indices. . .")
        self.all_club_lengths = []
        for student in range(self.number_of_students):
            this_club_length = []
            for clubs in self.all_clubs_similarity.iloc[student, 1:]:
                this_club_length.append(len(literal_eval(clubs)))
            self.all_club_lengths.append(this_club_length)

        pd.DataFrame(
            self.all_club_lengths, columns=self.hash_keys).set_index(
                i for i in self.hash_keys).to_csv(
                    './generated_csv_files/3_clubs_similarity_index.csv')
        print("\n\n Process completed!")

    def most_similar_users(self):
        # Storing club recommendations from most recommended
        # to least recommended
        self.similarity_index_dataset = pd.read_csv(
            './generated_csv_files/3_clubs_similarity_index.csv')
        print("\n 1) Finding most similar users. . .")
        self.similar_students = []
        for student in range(self.number_of_students):
            self.similar_students.append(
                list(
                    self.similarity_index_dataset.iloc[student, 1:].sort_values(ascending=False).keys()))

        similar_students = pd.DataFrame(self.similar_students, index=self.hash_keys)
        similar_students.to_csv('./generated_csv_files/4_similar_students.csv', header=False)

    def get_clubs(self, student_hash_key: str) -> None:
        # Get all clubs associated with one hash_key
        get_student_index = self.complete_details.hash_key[self.complete_details.hash_key == student_hash_key].index.tolist()
        for idx in get_student_index:
            return(self.complete_details["clubs"][idx])

    def find_other_clubs(self, this_student_clubs:list, another_student_clubs:list) -> list:
        # Find unique clubs between two club lists
        #return list(set(literal_eval(this_student_clubs)) ^ set(literal_eval(another_student_clubs)))
        
        return literal_eval(list(np.setdiff1d(another_student_clubs, this_student_clubs))[0])

    def get_importance(self, this_student_pos:int, other_student_hash_key:str) -> None:
        # Calculate the weight of each suggestion
        self.similarity_index_dataset = pd.read_csv('./generated_csv_files/3_clubs_similarity_index.csv')
        return (self.similarity_index_dataset[other_student_hash_key][this_student_pos])

    def sort_dictionary(self, dictionary:dict) -> list:
        new_dictionary = {k:v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}
        return new_dictionary.keys()

    def generate_recommendations(self) -> None:
        print("\n 2) Computing recommendations. . .")
        self.similarity_students = pd.read_csv('./generated_csv_files/4_similar_students.csv', header=None)
        self.student_club_recommendations = []

        for this_student in range(self.number_of_students):
            this_hash_key = self.similarity_students.iloc[this_student, 0]

            self.this_clubs = self.get_clubs(this_hash_key)
            self.this_clubs_scores = {}
            keys = self.club_titles.copy()
            values = [0 for i in range(self.number_of_clubs)]
            for i in range(self.number_of_clubs):
                self.this_clubs_scores[keys[i]] = values[i]

            for other_student in range(1, self.number_of_students+1):
                other_hash_key = self.similarity_students.iloc[this_student, other_student]
                if(other_hash_key != this_hash_key):
                    self.other_clubs = self.get_clubs(other_hash_key)
                    this_unique_clubs = self.find_other_clubs(self.this_clubs, self.other_clubs)
                    for club in this_unique_clubs:
                        self.this_clubs_scores[club] += self.get_importance(this_student, other_hash_key)

            #for key in list(self.this_clubs_scores.keys()):
            #    if key in self.this_clubs:
            #        del self.this_clubs_scores[key]

            self.this_clubs_scores = self.sort_dictionary(self.this_clubs_scores)
            print("\n Process ", this_student+1, "/", self.number_of_students, " completed.")
            self.student_club_recommendations.append(self.this_clubs_scores)

        pd.DataFrame(self.student_club_recommendations).set_index(i for i in self.hash_keys).to_csv('./generated_csv_files/5_club_recommendations.csv')
        print("\nAll pipeline processes have successfully completed!")
