from populate_dataset import *
from club_similarity import *
from recommend_clubs import *


def pipeline(x) -> None:

    if x == '1':
        print("\n--------------------------------")
        print("\n Stage 1: Developing the dataset")
        print("\n--------------------------------")
        dataset = populate_dataset()
        dataset.generate_random_emails()
        dataset.generate_fake_interests()
        dataset.generate_dataset()

        print("\n--------------------------------")
        print("\n Stage 2: Calculating similarity")
        print("\n--------------------------------")
        similarity_dataset = club_similarity()
        similarity_dataset.find_club_similarity()

        print("\n--------------------------------")
        print("\n Stage 3: Calculating similarity indices")
        print("\n--------------------------------")
        similarity_index = recommendations()
        similarity_index.generate_similarity_index()

        print("\n--------------------------------")
        print("\n Stage 4: Generating club recommendations")
        print("\n--------------------------------")
        similarity_index.most_similar_users()
        similarity_index.generate_recommendations()

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
