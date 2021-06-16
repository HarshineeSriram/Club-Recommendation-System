import os
import string
import json
import random
import hashlib
import pandas as pd


class populate_dataset:
    def __init__(self) -> None:
        print("\n 1) Loading initial parameters. . .")
        initial_parameters = open(r'initial_parameters.json')
        initial_parameters = json.load(initial_parameters)

        self.number_of_students = initial_parameters['number_of_students']
        f_clubs = open(initial_parameters['paths']['path_to_all_clubs'],)
        f_events = open(initial_parameters['paths']['path_to_all_events'],)

        data_clubs = json.load(f_clubs)
        data_events = json.load(f_events)
        self.faculties = initial_parameters['faculties']

        self.number_of_clubs = len(data_clubs)
        self.number_of_events = len(data_events)

        self.club_titles = [data_clubs[i]['title'] for i in range(
            self.number_of_clubs)]
        self.event_ids = [data_events[i]['eventId'] for i in range(
            self.number_of_events)]

    def generate_random_emails(self) -> None:
        print("\n 2) Generating random email IDs and encrypting them. . .")
        # Generating random email IDs
        self.all_chars = list(string.ascii_letters)
        self.all_special_chars = list(string.punctuation)

        self.all_domains = ["@gmail.com", "@yahoo.com",
                            "@hotmail.com", "@aol.com", "@msn.com",
                            "@live.com", "@rediffmail.com",
                            "@outlook.com", "@bigpond.com", "@cox.net"]
        self.all_email_ids = []

        for i in range(self.number_of_students):  # maximum number of students
            email = []
            length_of_email = random.randint(5, 15)
            place_of_special_char = -1

            if(random.randint(0, 1)):
                # if the e-mail will have special characters
                place_of_special_char = random.randint(1, length_of_email)

            for j in range(0, length_of_email):
                # populating email with random characters
                email.append(random.choice(self.all_chars))

            if (place_of_special_char > 0):
                # adding a random special character to a random place
                email.insert(
                    place_of_special_char, random.choice(
                        self.all_special_chars))

            email += random.choice(self.all_domains)
            self.all_email_ids.append(''.join(email))

        # One way encryption of e-mail IDs
        self.hash_keys = []
        self.salt_values = []
        for i in range(self.number_of_students):
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac(
                'sha256', self.all_email_ids[i].encode(
                    'utf-8'), salt, 100)
            self.salt_values.append(salt)
            self.hash_keys.append(key)

    def generate_fake_interests(self) -> None:
        print("\n 3) Generating fake club memberships, events participation, and originating faculty for each student. . .")
        # Generating fake clubs, events, and faculty for each student
        self.club_interests = []
        self.event_interests = []
        self.faculty = []

        for i in range(self.number_of_students):
            this_club = []
            this_event = []

            # random number of interested clubs and events
            club_number = random.randint(1, 15)
            event_number = random.randint(1, 15)

            for j in range(club_number):
                this_club.append(random.choice(self.club_titles))

            for j in range(event_number):
                this_event.append(random.choice(self.event_ids))

            self.club_interests.append(this_club)
            self.event_interests.append(this_event)

        for i in range(self.number_of_students):
            self.faculty.append(random.choice(self.faculties))

    def generate_dataset(self) -> None:
        print("\n 4) Saving the generated dataset. . .")
        complete_details = pd.DataFrame(
            list(
                zip(
                    self.all_email_ids, self.hash_keys,
                    self.salt_values, self.faculty,
                    self.club_interests, self.event_interests)),
                    columns=["email", "hash_key", "salt",
                            "faculty", "clubs", "events"])

        complete_details.to_csv(
            './generated_csv_files/1_student_all_interests.csv')
        print("\n\n Process completed!")
