import os
import copy
import instaloader
import pandas as pd
from datetime import datetime, date
from pathlib import Path


def get_data(target_name, login_name):
    df_followees = pd.DataFrame(columns=['userid', 'username', 'full_name'])
    df_followers = pd.DataFrame(columns=['userid', 'username', 'full_name'])
    today = date.today()

    L = instaloader.Instaloader()
    L.interactive_login(login_name)

    profile = instaloader.Profile.from_username(L.context, target_name)

    if (profile.is_private == True) & (profile.followed_by_viewer == False):
        raise Exception('The target profile "' + target_name + '" is private! Account "' +
                        login_name + '" has not followed them!')

    for followee in profile.get_followees():
        temp_data = {'userid': [followee.userid], 'username': [followee.username], 'full_name': [followee.full_name]}
        temp_df = pd.DataFrame(data=temp_data)
        df_followees = df_followees.append(temp_df, ignore_index=True)

    for follower in profile.get_followers():
        temp_data = {'userid': [follower.userid], 'username': [follower.username], 'full_name': [follower.full_name]}
        temp_df = pd.DataFrame(data=temp_data)
        df_followers = df_followees.append(temp_df, ignore_index=True)

    Path('../data').mkdir(exist_ok=True)

    df_followees.to_csv(path_or_buf=('../data/' + str(today) + '_followees_' + target_name + '.csv'),
                        index=False)

    df_followers.to_csv(path_or_buf=('../data/' + str(today) + '_followers_' + target_name + '.csv'),
                        index=False)

    return


def analyze_data(target_name, from_date='', to_date=''):
    my_files_all = os.listdir('../data/')
    my_files = copy.deepcopy(my_files_all)

    for file in my_files_all:
        if file[-(len(target_name) + 4): -4] != target_name:
            my_files.remove(file)

    if (to_date == '') or (from_date == ''):
        default_to_date = datetime(1970, 1, 2)
        default_from_date = datetime(1970, 1, 2)
        for file in my_files:
            file_date = datetime.strptime(file[0:10], '%Y-%m-%d')
            if file_date.timestamp() > default_to_date.timestamp():
                default_from_date = default_to_date
                default_to_date = file_date
                # Feels so redundant lol
                to_date_followee = str(default_to_date.date()) + '_followees_' + target_name
                to_date_follower = str(default_to_date.date()) + '_followers_' + target_name
                from_date_followee = str(default_from_date.date()) + '_followees_' + target_name
                from_date_follower = str(default_from_date.date()) + '_followers_' + target_name

            elif (file_date.timestamp() > default_from_date.timestamp()) & \
                    (file_date.timestamp() != default_to_date.timestamp()):
                default_from_date = file_date

                from_date_followee = str(default_from_date.date()) + '_followees_' + target_name
                from_date_follower = str(default_from_date.date()) + '_followers_' + target_name

        if default_to_date == datetime(1970, 1, 2):
            raise Exception('No files found in "data" directory! Make sure file names follows proper formating!')
        if default_from_date == datetime(1970, 1, 2):
            raise Exception('Only one day in "data" directory. Nothing to compare with!')

    if to_date != '':
        assert len(to_date) == 10, '"to_date" argument only accepts "YYYY-MM-DD" as input!'
        assert type(to_date) == str, '"to_date" argument only accepts string inputs!'
        to_date_followee = to_date + '_followees_' + target_name
        to_date_follower = to_date + '_followers_' + target_name
    else:
        to_date = default_to_date.date()

    if from_date != '':
        assert len(from_date) == 10, '"from_date" argument only accepts "YYYY-MM-DD" as input!'
        assert type(from_date) == str, '"from_date" argument only accepts string inputs!'
        from_date_followee = from_date + '_followees_' + target_name
        from_date_follower = from_date + '_followers_' + target_name
    else:
        from_date = default_from_date.date()

    # Actually reading the files
    to_date_followee_data = pd.read_csv('../data/' + to_date_followee + '.csv')
    to_date_follower_data = pd.read_csv('../data/' + to_date_follower + '.csv')

    from_date_followee_data = pd.read_csv('../data/' + from_date_followee + '.csv')
    from_date_follower_data = pd.read_csv('../data/' + from_date_follower + '.csv')

    new_followers = list(set(to_date_follower_data['userid']) - set(from_date_follower_data['userid']))
    past_followers = list(set(from_date_follower_data['userid']) - set(to_date_follower_data['userid']))

    new_followees = list(set(to_date_followee_data['userid']) - set(from_date_followee_data['userid']))
    past_followees = list(set(from_date_followee_data['userid']) - set(to_date_followee_data['userid']))

    report_data = {
        'New Followers': to_date_follower_data[to_date_follower_data['userid'].isin(new_followers)]['username'],
        'Accounts Who Unfollowed You': from_date_follower_data[from_date_follower_data['userid'].isin(past_followers)]['username'],
        'New Accounts You Follow': to_date_followee_data[to_date_followee_data['userid'].isin(new_followees)]['username'],
        'Accounts You Unfollowed': from_date_followee_data[from_date_followee_data['userid'].isin(past_followees)]['username']}

    report_df = pd.DataFrame(data=report_data)

    Path('../reports').mkdir(exist_ok=True)

    report_df.to_csv(path_or_buf = ('../reports/' + str(from_date) + '_to_' + str(to_date) + '_' + target_name + '.csv'),
                     index = False)

    return
