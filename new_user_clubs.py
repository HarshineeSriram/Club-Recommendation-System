import pandas as pd
import collections
from collections import Counter
from ast import literal_eval

def global_club_recommendations() -> None:
    all_student_memberships = pd.read_csv(r'./generated_csv_files/student_all_interests.csv')['clubs']
    c = collections.Counter()

    for clubs in all_student_memberships:
        c.update(literal_eval(clubs))

    c = Counter(c).most_common()
    global_recommendations = pd.DataFrame(c)
    global_recommendations.columns = ['club_name', 'enrolled_students']
    global_recommendations.to_csv('./generated_csv_files/global_club_recommendations.csv')