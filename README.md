Python From Zero To Hero
=========================

This is an example of Python application which allows to search twits in Twitter and display a tweets as long as a link to the Google Maps in case if tweet contains geodata.


Steps
-----
- [x] step_0 Project structure and base requirements.
- [x] step_1 Simple Hello World! application on Flask.
- [x] step_2 Configuration.
- [x] step_3 Tests.
- [x] step_4 Static files and Jinja2 templates (+some Twitter Bootstrap).
- [x] step_5 DB (MySQL + SQLAlchemy).
- [x] step_6 Login and sessions.
- [x] step_7 Backend (tweepy module to search for tweets by some criteria).
- [ ] step_8 More backend (Show a list of tweets as long as a link to Google Maps for tweets which has Geo data.
- [ ] step_9 More backend (do NLP stuff with tweets).

Each sep is tegged wiht ``step_n`` tag where `n` is a number of step.

How to start
------------
1. Create and activate python wirtual environment.
2. Clone this repository.
3. Switch to the required step (``git checkout <tag_name>``)
4. Insall dependencies (``pip install -U -r requirements.txt``)
5. Do something.

MySQL Setup
-----------
1. Create user:
   ```
   CREATE USER 'twitter_explorer'@'localhost' IDENTIFIED BY '123456';
   ```

2. Grant privileges:
   ```
   GRANT ALL PRIVILEGES on twitter_explorer.* to 'twitter_explorer'@'localhost';
   GRANT ALL PRIVILEGES on twitter_explorer_test.* to 'twitter_explorer'@'localhost'
   ```

3. Create DBs:
   ```
   CREATE DATABASE twitter_explorer;
   CREATE DATABASE twitter_explorer_test;
   ```

Known Issues
------------
1. Typo in env var name TWITER_EXPLORER_CONF -> TWITTER_EXPLORER_CONF. Fixed in `step_7`.
2. ``manage.py`` scripts prints weired docstring when shows help for subcommands.
3. Logging used across modules need to be updated to use the same logger to simplify logging logic.

FAQ
---
https://docs.google.com/document/d/1r0y6JMtTcgHIqTq0JpWY1gv3hFqlR3qroLa42Ok9n2E/edit
