import pandas as pd
import numpy as np
from ast import literal_eval
import json


class club_similarity:
    def __init__(self) -> None:
        # Loading initial files and variables
        print("\n 1) Loading initial data. . .")
        self.complete_details = pd.read_csv(
            './generated_csv_files/1_student_all_interests.csv')
        initial_parameters = open(r'initial_parameters.json')
        initial_parameters = json.load(initial_parameters)
        self.number_of_students = initial_parameters['number_of_students']
        self.hash_keys = self.complete_details['hash_key']

    def find_club_similarity(self) -> None:
        all_clubs_similarity = np.zeros(
            (self.number_of_students, self.number_of_students),
            dtype=object)

        print("\n 2) Finding common clubs between pairs of students. . .")
        # Finding common clubs between all pairs of existing students
        for i in range(self.number_of_students):
            this_clubs_similarity = np.zeros((
                1, self.number_of_students), dtype=object)
            for j in range(self.number_of_students):
                if(j != i):
                    this_clubs_similarity[0][j] = list(
                        set(
                            literal_eval(
                                self.complete_details["clubs"][i])).intersection(
                            literal_eval(self.complete_details["clubs"][j])))
                elif(j == i):
                    this_clubs_similarity[0][j] = []
            all_clubs_similarity[i] = this_clubs_similarity

        all_clubs_similarity = pd.DataFrame(all_clubs_similarity, columns=
                                            [i for i in self.hash_keys]).set_index((i for i in self.hash_keys), drop=True)

        print("\n 3) Saving the generated file. . .")
        all_clubs_similarity.to_csv('./generated_csv_files/2_clubs_similarity.csv')
        print("\n\n Process completed!")
