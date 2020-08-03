# Instachecker


## Motivation
Ever wonder why your follower count decreased? Ever wonder who unfollowed you? Instachecker is not only able to provide real-time analysis of your profile, but it is also able to give you insight on how your social media realtionships change over time.


## Description
This package aims to track a person's followers and followees using the [Instaloader](https://instaloader.github.io/) package. This is done by taking a snapshot of a person's followers and followees and comparing them to another point in time. This package is able to detect a person's: new followers, new followees, past followers, past followees, previous followers/followees who are now deactivated/deleted, followees who don't follow back, as well as followers whom the person doesn't follow back.


## Usage
Navigate into the "src" folder and run [main_script.py](https://github.com/thejacktan/Instachecker/blob/master/src/main_script.py). Two folders called "data" and "report" will be created in the main repo directory.

## Dependencies
- Python 3.7.5
  - instaloader==4.4.4
  - pandas==0.25.3
