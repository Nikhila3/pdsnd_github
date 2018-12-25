import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Which city would you like to see data for? (Enter Chicago, New York City, or Washington) ")
    while True:
        city = input().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city name, please enter Chicago, New York City, or Washington. ")

    # get user input for month (all, january, february, ... , june)
    print("Which month would you like to see data for? (Enter a month name from January to June or all)")
    while True:
        month = input().lower()
        if month == 'all' or month in months:
            break
        else:
            print("Invalid month, please enter month name from January to June or all ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Which day of the week would you like to see data for? (Enter a day or all) ")
    while True:
        day = input().lower()
        if day == 'all' or day in days:
            break
        else:
            print("Invalid day, please enter day or all ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    most_common_month_name = months[most_common_month - 1]
    print("Most common month: {}".format(most_common_month_name))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("Most common day: {}".format(most_common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("Most common hour: {}".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most common start station: {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most common end station: {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print("Most common trip: {}".format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the mean and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time: {} seconds".format(total_time))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean travel time: {} seconds".format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("Number of each user type:")
    print(user_counts)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("\nNumber of each gender:")
        print(gender_counts)
    except KeyError:
        print("\nGender was not present in selected data")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df["Birth Year"].min()
        print("\nEarliest birth year: {}".format(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print("Most recent birth year: {}".format(most_recent_birth_year))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("Most common birth year: {}".format(most_common_birth_year))
    except KeyError:
        print("\nBirth year was not present in selected data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        raw_df = pd.read_csv(CITY_DATA[city])
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        num_rows = df.shape[0]
        i = 0;
        while i < num_rows:
            raw_data_request = input("\nWould you like to see 5 lines of raw data? Enter yes or no.\n")
            if raw_data_request.lower() != 'yes':
                break
            print(raw_df[i:i+5])
            i += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
