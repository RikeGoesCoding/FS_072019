import time
import pandas as pd
import numpy as np
import calendar as cl
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = '0'
    month = ' '
    day = ' '
    city_selection = ['c', 'n', 'w']
    month_selection = ['all', '1', '2', '3', '4', '5', '6']
    day_selection = ['all', '1', '2', '3', '4', '5', '6', '7']

    # while loop for city_selection
    while city not in city_selection:
        city = input('Please first select the city you want to analyze by entering the matching letter of the city!\n C - Chicago\n N - New York City\n W - Washington\n\nEnter value: ').lower()
        if city not in city_selection:
            print('That\'s not a valid input, please try again!\n')
    for key in CITY_DATA.keys():
        if key[0] == city:
            city = key
            break

    # get user input for month (all, january, february, ... , june) (while loop month_selection)
    while month not in month_selection:
        try:
            month = input('\nPlease select a month between January and June (Januray=1 to June=6).\nTo select all, press enter.\nEnter value:')
        except ValueError:
            print('That\'s not a valid input, please try again!\n')
        finally:
            if not month:
                month = 'all'
            if month not in month_selection:
                print('That\'s not a valid input, please try again!\n')

    # get user input for day of week (all, monday, tuesday, ... sunday) (while loop day_selection)
    while day not in day_selection:
        try:
            day = input('Please select a weekday (Monday=1 to Sunday=7).\nTo select all, press enter.\nEnter value:')
        except ValueError:
            print('That\'s not a valid input, please try again!\n')
        finally:
            if not day:
                day = 'all'
            if day not in day_selection:
                print('That\'s not a valid input, please try again!\n')

    # use calender to convert number to names for filter
    if month != 'all':
        month = cl.month_name[int(month)]
    if day != 'all':
        day = cl.day_name[int(day)-1]

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week'] == day.title()]
    return df

def time_stats(df):
    # Displays statistics on the most frequent times of travel.

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['Month'].nunique() > 1:
        most_common_month = int(df['Month'].mode()[0])
        print('The most common month where people have traveld was {}.'.format(cl.month_name[most_common_month]))

    #  the most common day of week
    if df['Day_of_week'].nunique() > 1:
        most_common_day = df['Day_of_week'].mode()[0]
        print('The most common weekday where people have traveld were {}s.'.format(most_common_day))

    # display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common start time was {} o\'clock.2'.format(most_common_hour))


    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('The most common station to start the trip was {}.'.format(most_common_start))

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('The most common station to end the trip was {}.'.format(most_common_end))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trip = df['Trip'].mode()[0]
    print('Most common trip is from {}.'.format(most_common_trip))


    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    total_trip_duration = str(dt.timedelta(seconds=int(total_trip_duration)))
    print('The total travel time where bikes were used amounts to {} of travel.'.format(total_trip_duration))

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    mean_trip_duration = str(dt.timedelta(seconds=int(mean_trip_duration)))
    print('The average rental duration per trip was {}.'.format(mean_trip_duration))


    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Only those statistics are evaluated where data is available.
    E.g. gender assessment is not possible for all data sets."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts().to_dict() #create dict to show user type split
    for user_type in user_types:
        print('The user type \'{}\' rented bikes a total of {} times.'.format(user_type, user_types[user_type]))

    #Display counts of gender
    try:
        gender_info = df['Gender'].value_counts().to_dict() #create dict to show gender type split
        for gender in gender_info:
            print('{}\'s rented bikes a total of {} times.'.format(gender, gender_info[gender]))

    #Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('Oldest bikers are born in {}.\nYoungest bikers are born in {}.\nMost bikers are born in {}.'.format(earliest_birth_year, recent_birth_year, common_birth_year))
    except:
        print('No gender data available')
    finally:

        print('-'*40)


def check_loop(city, month, day):
    """Serves to confirm that user selection of data was correct.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        n as True/Fales to define if data selection will be repeated or not"""
    if month == 'all':
        month = 'all available months'
    if day == 'all':
        day = 'all day'
    n = input('You will be investigating on {} usage data for {}s in {}.\nIf this is correct, please press enter to continue or enter any value to repeat your data selection.' .format(city.title(), day, month))
    if n:
        n = True
    else:
        n = False
    return n

def analysis_type(df):
    """To to limit output lines - user needs to select the wanted type of analysis."""

    while True:
        try:
            analysis = int(input('To select the type of analysis please enter one of of the following numbers:\n1 - t analysis\n2 - locations analysis\n3 - durations analysis\n4 - user analysis\n5 - Show raw data \n6 - Stop analysis \nEnter value:'))
        except:
            print('No valid data entry, please try again!\n')
        else:
            if analysis == 1:
                time_stats(df)
            elif analysis == 2:
                station_stats(df)
            elif analysis == 3:
                trip_duration_stats(df)
            elif analysis == 4:
                user_stats(df)
            elif analysis == 5:
                print(df.head(20))# show first 20 lines of raw data of selected df
            elif analysis == 6:
                break
            else:
                print('No valid data entry, please try again!\n')


def main():
    n = True
    while True:
        while n:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            n = check_loop(city, month, day)
        analysis_type(df)

        restart = input('\Would you like to quit your analysis? Enter yes or no.\n')
        if restart.lower() == 'yes':
            n = True
        else:
            break


if __name__ == "__main__":
	main()
