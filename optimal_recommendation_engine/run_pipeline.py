from generate_tags import *
from populate_dataset import *
from club_similarity import *
from recommend_clubs import *

import json

def pipeline(x) -> None:

    if x == '1':
        print("\n--------------------------------")
        print("\n Stage 1: Generating smarter tags for current clubs")
        print("\n--------------------------------")
        this_obj = generate_club_tags()
        this_obj.generate_better_tags()
        print("\n 3) Saving the generated .json file. . .")
        jsonStr = json.dumps(this_obj.data_clubs, indent=4)
        jsonFile = open("../generated_json_files/data.json", "w")
        jsonFile.write(jsonStr)
        jsonFile.close()
        print("\n Stage 1 complete!")

        print("\n--------------------------------")
        print("\n Stage 2: Populating the extended dataset")
        print("\n--------------------------------")
        dataset = populate_dataset()
        dataset.generate_random_emails()
        dataset.generate_fake_interests()
        dataset.generate_personal_tags()
        dataset.generate_dataset()

        print("\n--------------------------------")
        print("\n Stage 3: Generating club similarity")
        print("\n--------------------------------")
        all_clubs = club_similarity()
        all_clubs.find_club_similarity()

        print("\n--------------------------------")
        print("\n Stage 4: Generating club similarity indices based on student information")
        print("\n--------------------------------")
        similarity_indices = recommendations()
        similarity_indices.generate_similarity_index()
        similarity_indices.most_similar_users()
        similarity_indices.generate_recommendations()

    elif x == '2':
        print("\n Currently under development.")

    elif x == '3':
        print("\n Currently under development.")


print("Menu: \
     \n 1. Initiate the recommendation system pipeline \
     \n 2. Returning user \
     \n 3. New user")
     
choice = input("\n Enter 1/2/3 to proceed:")

pipeline(choice)
