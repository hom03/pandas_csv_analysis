import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


negative =  ["dirty", "uncomfortable", "noisy", "rude", "disappointing", "poor", "expensive", "unfriendly", "stale", "inadequate", "smelly", "outdated", "misleading", "unresponsive", "unhygienic", "chaotic", "horrible", "bad", "frustrating", "unsafe", "cold"]
    
positive = ["clean", "comfortable", "quiet", "friendly", "enjoyable", "excellent", "affordable", "welcoming", "good", "modern", "fresh", "helpful", "responsive", "convenient", "hygienic", "charming", "nice", "pleasant", "satisfying", "safe", "perfect"]    

noises = [".",",","?",")","(",":",";","_", "-", " ́", "*", "!", "[", "]", "{", "}", "@", "%"]

df = pd.read_csv("Hotel.csv")


def Task1():
    clean_df = df.dropna(subset=['hotel_name','nationality'])
    # A
    hotel_counts = clean_df['hotel_name'].value_counts()
    h1 = hotel_counts.idxmax()
    print(f"The hotel with the highest number of records is: {h1} with {hotel_counts.max()} records.\n")

    # B
    h1_rows = clean_df[clean_df['hotel_name'] == h1]
    h1_unique_nations = h1_rows['nationality'].unique()
    print(f"{h1} nations: ")
    for nation in h1_unique_nations:
        print(nation)
    print('\n')

    # C
    h2 = hotel_counts.index[1]
    second_highest_count = hotel_counts.iloc[1]
    print(f"The hotel with the second highest number of records is: {h2} with {second_highest_count} records.\n")

    # D
    h2_rows = clean_df[clean_df['hotel_name'] == h2]
    h2_unique_nations = h2_rows['nationality'].unique()
    print(f"{h2} nations: ")
    for nation in h2_unique_nations:
        print(nation)

Task1()


def Task2():
    # clean reviewed_at column
    clean_df = df.dropna(subset=["reviewed_at"]).copy()

    # A
    clean_df.loc[:,'month'] = clean_df['reviewed_at'].str.split('-').str[1]
    unique_months = clean_df['month'].unique()
    print("\nUnique Months: ",unique_months)

    # B
    month_mapping = {
        'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'
    }
    def replace_month(date_str):
        day, month, year = date_str.split('-')
        month_num = month_mapping.get(month,month)
        return f"{day}-{month_num}-{year}"
    clean_df['reviewed_at'] = clean_df['reviewed_at'].apply(replace_month)
    print(clean_df['reviewed_at'])

    # C
    clean_df['year']  = clean_df['reviewed_at'].str.split('-').str[2]
    least_freq_year = clean_df['year'].value_counts().idxmin()
    def fill_dates(row):
        if pd.isna(row['reviewed_at']):
            day_month = row['reviewed_at'].split('-')[:2]
            return f"{day_month[0]}-{day_month[1]}-{least_freq_year}"
        return row['reviewed_at']
    clean_df['reviewed_at'] = clean_df.apply(fill_dates,axis=1)

    # D
    year_counts = clean_df['year'].value_counts()
    #plot bar chart
    plt.figure(figsize=(10,6))
    year_counts.sort_index().plot(kind="bar",color="Blue")
    plt.title("Frequency of Each Year in reviewed_at column")
    plt.xlabel("Year")
    plt.ylabel("Count (Reviews)")
    plt.show()

Task2()


def Task3():
    # A
    if 'review_text' in df.columns:
        try:
            def clean_text(text):
                for noise in noises:
                    text= text.replace(noise,"")
                return text
            df['clean_review'] = df['review_text'].astype(str).apply(clean_text)

            # B
            def count_positive_words(text):
                return sum(1 for term in positive if term in text.split()) # count positive words in review
            df['pos_count']  = df['clean_review'].apply(count_positive_words) # positive column
            filtered_pos_df = df[df['pos_count'] >= 2] # records where pos count equals or exceeds 2

            # C
            pos_avg_rating = filtered_pos_df['rating'].mean()
            print(f"{pos_avg_rating}") # 8.832923266184837

            # D
            def count_negative_words(text):
                return sum(1 for term in negative if term in text.split())  # count positive words in review

            df['neg_count'] = df['clean_review'].apply(count_negative_words)  # negative column
            filtered_neg_df = df[df['neg_count'] >= 2]  # records where neg count equals or exceeds 2

            # E
            neg_avg_rating = filtered_neg_df['rating'].mean()
            print(f"{neg_avg_rating}") # 5.815463917525773

            # F
            '''
            Reviews with more than 2 or more positive words tend to have a higher average rating, while those with 2 
            or more negative words tends to have a lower average rating.
            '''
        except Exception as e:
            print(f"An error has occurred while cleaning text: {e}")
    else:
        print("'review_text' column is missing from dataframe")

Task3()


def Task4():
    # A
    if 'tags' in df.columns:
        try:
            clean_df = df.dropna(subset=["tags"])

            # B
            trip_categories =['Business','Leisure','Solo']
            trip_df = clean_df[clean_df['tags'].str.split().str[0].isin(trip_categories)]

            # C
            category_avg_rating = trip_df.groupby(trip_df['tags'].str.split().str[0])['rating'].mean()

            # C - Visual representation
            plt.figure(figsize=(10,5))
            category_avg_rating.plot(kind='bar',color=["blue","red","green"])
            plt.title("Average rating for different trip purposes")
            plt.xlabel("Trips")
            plt.ylabel("Ratings")
            plt.xticks(rotation=0)
            plt.ylim(7.5,9)
            plt.yticks(np.arange(8,9.1,0.1))
            plt.tight_layout()
            plt.show()

            # D
            '''
            People on trips for leisure tend to rate the highest and people who
            travel solo tend to rate the lowest
            '''
        except Exception as e:
            print(f"Exception: {e}")
    else:
        print("No 'tags' column in dataframe")


Task4()


def Task5():
    """
    Relationship between the seasons of the year (spring,summer,autumn,winter) and the amount of review traffic
    """
    # clean data that has no review date
    clean_df = df.dropna(subset=["reviewed_at"]).copy()

    # split the months up from the reviewed_at
    clean_df['month'] = clean_df['reviewed_at'].str.split('-').str[1]

    # function to map months to seasons
    def get_season(month):
        # create seasonal arrays
        spring = ['Feb', 'Mar', 'Apr']
        summer = ['May', 'Jun', 'Jul']
        autumn = ['Aug', 'Sep', 'Oct']
        winter = ['Nov', 'Dec', 'Jan']

        if month in spring:
            return 'Spring'
        elif month in summer:
            return 'Summer'
        elif month in autumn:
            return 'Autumn'
        elif month in winter:
            return 'Winter'
        else:
            return 'Season unknown'

    clean_df['season'] = clean_df['month'].apply(get_season)
    season_counts = clean_df['season'].value_counts()

    # Pie chart for number of reviews in each season
    sectionToExplode=(0.1,0,0,0)
    plt.pie(season_counts.values,explode=sectionToExplode,
    labels=season_counts.index,shadow=True,autopct='%.2f%%',startangle=90)
    plt.title("Difference in quantity of reviews in different seasons")
    plt.show()

    """
    Autumn months have more reviews than the other seasons (8593) this could be because people
    like to get away in August or mid term break
    Spring months have less reviews than other seasons (5158) this could be because it is the
    start of the year and people are very busy
    """

Task5()
