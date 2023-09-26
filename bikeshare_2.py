import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington). 
    while True:
        city = input('Please enter the name of the city (Chicago, New york city, Washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Incorrect city name. Please choose from the provided options.')

    while True:
        month = input('Please enter the month you want to check in for (all, january, february, ..., june): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Incorrect month. Please choose from the provided options.')

    while True:
        day = input('Please enter the day of the week you want to inquire (all, monday, tuesday, ..., sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Incorrect day. Please choose from the provided options.')

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

    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)
    print(df.columns)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        _month = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Month'] == _month]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    _month = ['january', 'february', 'march', 'april', 'may', 'june']

    # Display the most common month
    common_month = df['Month'].mode()[0] # returns integer so i put it to check the _month list
    print(f"The most common month people travel from  our calculation is: {str(_month[common_month - 1]).capitalize()}")

    # Display the most common day of the week
    common_day = df['Day of Week'].mode()[0]
    print(f"The day of the week people prefer to travel is: {common_day}")

    # Extract and display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print(f"The common time for travel is: {common_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # Display the most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    # Calculate and display the most frequent combination of start station and end station for trips
    frequent = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start station and end station for trips is: {frequent[0]} to {frequent[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time for all trips is: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The average travel time for trips is: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    for user_type, count in user_types.items():
        print(f"{user_type}: {count}")

    # Display counts of gender (if available in the data)
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print("\nTotal counts of gender:")
        for gender, count in genders.items():
            print(f"{gender}: {count}")
    else:
        print("\nGender information is not available check back later.")

    # Display earliest, most recent, and most common year of birth (if available in the data)
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print(f"\nEarliest year of birth: {int(earliest_birth_year)}")
        print(f"Most recent year of birth: {int(most_recent_birth_year)}")
        print(f"Most common year of birth: {int(common_birth_year)}")
    else:
        print("\nBirth date information is not available check back later.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_age_groups(df):
    """
    Categorizes users into age groups and analyzes their preferences and usage patterns.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing bikeshare data with 'Birth Year' column.

    Returns:
        None (prints statistics for each age group individually).
    """

    current_year = pd.Timestamp.now().year

    ages = [0, 18, 30, 45, 60, 120]
    age_labels = ['<18', '18-30', '31-45', '46-60', '60+']  

    if 'Birth Year' in df.columns:
        df['Age Group'] = pd.cut(current_year - df['Birth Year'], bins=ages, labels=age_labels)

        age_groups = df['Age Group'].unique()

        for age_group in age_groups:
            age_group_df = df[df['Age Group'] == age_group]

            if not age_group_df.empty:
                total_trips = age_group_df['Trip Duration'].count()
                average_trip_duration = age_group_df['Trip Duration'].mean()
                most_common_start_station = age_group_df['Start Station'].mode().iat[0]
                most_common_end_station = age_group_df['End Station'].mode().iat[0]

                print(f"Age Group: {age_group}")
                print(f"Total Trips: {total_trips}")
                print(f"Average Trip Duration: {average_trip_duration}")
                print(f"Most Common Start Station: {most_common_start_station}")
                print(f"Most Common End Station: {most_common_end_station}")
                print('-' * 40)
            else:
                print(f"No data available for Age Group: {age_group}")


def subscription_duration_stats(df):
    """
    Calculates the average subscription duration for subscribers and customers.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing bikeshare data with 'User Type', 'Start Time', and 'End Time' columns.

    Returns:
        None (prints data in the dictionary containing the average subscription duration for subscribers and customers).

    """

    _df = df[df['User Type'].isin(['Subscriber', 'Customer'])].copy()

    _df['Start Time'] = pd.to_datetime(_df['Start Time'])
    _df['End Time'] = pd.to_datetime(_df['End Time'])

    # calculating subscription duration in minutes
    _df['Subscription Duration'] = (_df['End Time'] - _df['Start Time']).dt.total_seconds() / 60

    # calculating the average subscription duration for subscribers and customers
    avg_duration = {
        'Subscriber': _df[_df['User Type'] == 'Subscriber']['Subscription Duration'].mean(),
        'Customer': _df[_df['User Type'] == 'Customer']['Subscription Duration'].mean()
    }

    print("Average Subscription Duration:")
    print(f"Subscriber: {avg_duration['Subscriber']} minutes")
    print(f"Customer: {avg_duration['Customer']} minutes")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        user_age_groups(df)
        subscription_duration_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
