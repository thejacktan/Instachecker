import os
import copy
import instaloader
import pandas as pd
from datetime import datetime, date
from pathlib import Path
import sys


def get_data(target_name, login_name, login_pass):
    df_followees = pd.DataFrame(columns=['userid', 'username', 'full_name'])
    df_followers = pd.DataFrame(columns=['userid', 'username', 'full_name'])
    today = date.today()

    L = instaloader.Instaloader()
    L.login(user=login_name, passwd=login_pass)

    try:
        target_profile = instaloader.Profile.from_username(L.context, target_name)
    except Exception as e:
        print(e)
        print('Target profile does not exist! Please make sure ' + login_name + ' is not blocked by target profile!')
        sys.exit(1)

    # Seeing if we're able to access target profile data
    if (target_profile.is_private == True) & (target_profile.followed_by_viewer == False):
        raise Exception('The target profile "' + target_name + '" is private! Account "' +
                        login_name + '" has not followed them!')

    # Adding followers and followees
    for followee in target_profile.get_followees():
        df_followees = df_followees.append(
            pd.DataFrame(data={'userid': [followee.userid], 'username': [followee.username],
                               'full_name': [followee.full_name]}), ignore_index=True)

    for follower in target_profile.get_followers():
        df_followers = df_followers.append(
            pd.DataFrame(data={'userid': [follower.userid], 'username': [follower.username],
                               'full_name': [follower.full_name]}),
            ignore_index=True)

    Path('../data').mkdir(exist_ok=True)

    df_followees.to_csv(path_or_buf=('../data/' + str(today) + '_followees_' + target_name + '.csv'),
                        index=False)

    df_followers.to_csv(path_or_buf=('../data/' + str(today) + '_followers_' + target_name + '.csv'),
                        index=False)

    return


def analyze_data(target_name, from_date='', to_date=''):
    L = instaloader.Instaloader()
    my_files_all = os.listdir('../data/')
    my_files = copy.deepcopy(my_files_all)

    # Filtering for files associated with target profile
    for file in my_files_all:
        if file[-(len(target_name) + 4): -4] != target_name:
            my_files.remove(file)

    # Finding default "to" and "from" dates if arguments not given
    if (to_date == '') or (from_date == ''):
        default_to_date = datetime(1970, 1, 2)
        default_from_date = datetime(1970, 1, 2)
        for file in my_files:
            file_date = datetime.strptime(file[0:10], '%Y-%m-%d')

            # Shifts both the "from" and "to" dates
            if file_date.timestamp() > default_to_date.timestamp():
                default_from_date = default_to_date
                default_to_date = file_date
                to_date_followee = str(default_to_date.date()) + '_followees_' + target_name
                to_date_follower = str(default_to_date.date()) + '_followers_' + target_name
                from_date_followee = str(default_from_date.date()) + '_followees_' + target_name
                from_date_follower = str(default_from_date.date()) + '_followers_' + target_name

            # Only shifts the "from" date
            elif (file_date.timestamp() > default_from_date.timestamp()) & \
                    (file_date.timestamp() != default_to_date.timestamp()):
                default_from_date = file_date

                from_date_followee = str(default_from_date.date()) + '_followees_' + target_name
                from_date_follower = str(default_from_date.date()) + '_followers_' + target_name

        if default_to_date == datetime(1970, 1, 2):
            raise Exception('No files found in "data" directory! Make sure file names follows proper formating!')
        if default_from_date == datetime(1970, 1, 2):
            print('Only one day in "data" directory! Limited report can be generated')

    # Taking manual input if given
    if to_date != '':
        assert len(to_date) == 10, '"to_date" argument only accepts "YYYY-MM-DD" as input!'
        assert type(to_date) == str, '"to_date" argument only accepts string inputs!'
        default_to_date = datetime.strptime(to_date, '%Y-%m-%d')
        to_date_followee = to_date + '_followees_' + target_name
        to_date_follower = to_date + '_followers_' + target_name

    if from_date != '':
        assert len(from_date) == 10, '"from_date" argument only accepts "YYYY-MM-DD" as input!'
        assert type(from_date) == str, '"from_date" argument only accepts string inputs!'
        default_from_date = datetime.strptime(from_date, '%Y-%m-%d')
        from_date_followee = from_date + '_followees_' + target_name
        from_date_follower = from_date + '_followers_' + target_name

    # Attempting to read data files from the specified dates
    try:
        to_date_followee_data = pd.read_csv('../data/' + to_date_followee + '.csv')
    except:
        print('Unable to find file: ' + to_date_followee + '.csv')

    try:
        to_date_follower_data = pd.read_csv('../data/' + to_date_follower + '.csv')
    except:
        print('Unable to find file: ' + to_date_follower + '.csv')

    try:
        from_date_followee_data = pd.read_csv('../data/' + from_date_followee + '.csv')
    except:
        print('Unable to find file: ' + from_date_followee + '.csv')

    try:
        from_date_follower_data = pd.read_csv('../data/' + from_date_follower + '.csv')
    except:
        print('Unable to find file: ' + from_date_follower + '.csv')

    # Generating report as appropriate
    deactivated_id = list()
    deactivated = list()

    try:
        new_followers_id = list(set(to_date_follower_data['userid']) - set(from_date_follower_data['userid']))
        new_followers = list(to_date_follower_data[to_date_follower_data['userid'].isin(new_followers_id)]['username'])
    except:
        new_followers = list()

    try:
        past_followers_id = list(set(from_date_follower_data['userid']) - set(to_date_follower_data['userid']))
        for n in past_followers_id:
            if n in deactivated_id:
                past_followers_id.remove(n)
                continue
            else:
                try:
                    instaloader.Profile.from_id(L.context, n)
                except Exception:
                    past_followers_id.remove(n)
                    deactivated_id.append(n)
                    deactivated.append(
                        from_date_follower_data[from_date_follower_data['userid'] == n]['username'].values[0])

        past_followers = list(
            from_date_follower_data[from_date_follower_data['userid'].isin(past_followers_id)]['username'])
    except:
        past_followers = list()

    try:
        new_followees_id = list(set(to_date_followee_data['userid']) - set(from_date_followee_data['userid']))
        new_followees = list(to_date_followee_data[to_date_followee_data['userid'].isin(new_followees_id)]['username'])
    except:
        new_followees = list()

    try:
        past_followees_id = list(set(from_date_followee_data['userid']) - set(to_date_followee_data['userid']))
        for n in past_followees_id:
            if n in deactivated_id:
                past_followees_id.remove(n)
                continue
            else:
                try:
                    instaloader.Profile.from_id(L.context, n)
                except Exception:
                    past_followees_id.remove(n)
                    deactivated_id.append(n)
                    deactivated.append(
                        from_date_followee_data[from_date_followee_data['userid'] == n]['username'].values[0])

        past_followees = list(
            from_date_followee_data[from_date_followee_data['userid'].isin(past_followees_id)]['username'])
    except:
        past_followees = list()

    try:
        no_followback_id = list(set(to_date_followee_data['userid']) - set(to_date_follower_data['userid']))
        no_followback = list(to_date_followee_data[to_date_followee_data['userid'].isin(no_followback_id)]['username'])
    except:
        no_followback = list()

    try:
        no_follow_id = list(set(to_date_follower_data['userid']) - set(to_date_followee_data['userid']))
        no_follow = list(to_date_follower_data[to_date_follower_data['userid'].isin(no_follow_id)]['username'])
    except:
        no_follow = list()

    report_data = {
        ("New Followers of '" + target_name + "'"): new_followers,
        ("Accounts Who Unfollowed '" + target_name + "'"): past_followers,
        ("New Accounts Followed By '" + target_name + "'"): new_followees,
        ("Accounts Unfollowed By '" + target_name + "'"): past_followees,
        "Accounts Deactivated/Deleted": deactivated,
        ("Accounts Who Don't Follow Back '" + target_name + "' (" + str(default_to_date.date()) + ")"): no_followback,
        ("Accounts '" + target_name + "' Doesn't Follow Back (" + str(default_to_date.date()) + ")"): no_follow
    }

    report_df = pd.DataFrame.from_dict(data=report_data, orient='index').transpose()

    Path('../reports').mkdir(exist_ok=True)

    if default_from_date == datetime(1970, 1, 2):
        report_df.to_csv(path_or_buf=('../reports/' + str(default_to_date.date()) + '_' + target_name + '.csv'),
                         index=False)
    else:
        report_df.to_csv(path_or_buf=('../reports/' + str(default_from_date.date()) + '_to_' +
                                      str(default_to_date.date()) + '_' + target_name + '.csv'),
                         index=False)

    return
