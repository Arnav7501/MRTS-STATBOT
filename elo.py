import sqlite3
import math

# self explanatory


def calculateEloRating(player_rating, opponent_rating, outcome, k_factor=32):
    expected_score = 1 / \
        (1 + math.pow(10, (opponent_rating - player_rating) / 400))
    actual_score = outcome
    new_rating = player_rating + k_factor * (actual_score - expected_score)
    return round(new_rating)


# if the user exists, return the elo value, otherwise return false
def getUserInfo(username):
    conn = sqlite3.connect('elo.db')
    select_query = conn.execute("SELECT * FROM Rankings")
    if username == "all":
        return select_query

    for row in select_query:
        if row[0] == username:
            return row[1]
    return False


# if the user doesn't exist, create the user, otherwise update the user
def eloSystem(username, value):

    try:
        conn = sqlite3.connect('elo.db')
        cursor = conn.cursor()
        cursor.execute("DELETE from Rankings WHERE name = ?", ('test',))

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Rankings'")
        table_exists = cursor.fetchone()
        if not table_exists:
            conn.execute('''
            CREATE TABLE Rankings (
            name TEXT,
            eloValue INT
            );
            ''')
        cursor = conn.cursor()
        # if user does not exist, create user, otherwise update
        if getUserInfo(username) == False:
            print("does not exist")
            # if user does not exist, create user
            cursor.execute(
                f"INSERT INTO Rankings (name, eloValue) VALUES (?, ?)", (username, value))
        else:
            cursor.execute(
                f"UPDATE Rankings set eloValue = ? where name = ?", (value, str(username)))
        print("executed")
      #
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("exception", e)
        return False
