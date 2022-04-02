import requests
from django.db import connection
from spado_ubuntu.sql_queries import RECENT_POST_QUERY, SIMILAR_POST_QUERY_U2U, TRENDING_POST_QUERY, SIMILAR_POST_QUERY_I2I


def predict_post_by_trend() -> list:
    try:

        with connection.cursor() as c:
            c.execute(TRENDING_POST_QUERY)
            return [row[0] for row in c.fetchall()]

    except Exception as e:
        print("can't predict post [TRENDING], ", e)
        return []

def get_similar_posts_I2I(post_id) -> list:

    try:    

        with connection.cursor() as c:
            c.execute(SIMILAR_POST_QUERY_I2I % (post_id, post_id, post_id))
            return [row[0] for row in c.fetchall()]
        # My view is to just filter by get_weight_i2i() function on psql


    except Exception as e:
        pass


def predict_posts_by_relevant(user_id) -> list:

    try:

        with connection.cursor() as c:

            c.execute(SIMILAR_POST_QUERY_U2U % (user_id, user_id, user_id))
            return [row[0] for row in c.fetchall()]

    except Exception as e:
        # If we are unable to predict posts by relevant to a user we want to show them prending posts
        
        return predict_post_by_trend()


def predict_posts_by_recent() -> list:

    duration_in = 'month'
    max_age = '1'
    # This states that i need posts which are recent as 1 month

    try:
        with connection.cursor() as c:

            c.execute(RECENT_POST_QUERY % (duration_in, max_age))
            return [row[0] for row in c.fetchall()]

    except Exception as e:
        # If we are unable to predict posts by relevant to a user we want to show them prending posts
        
        return predict_post_by_trend()


def predict_posts_by_popular() -> list:

    # Implement it laterwards once we get formula

    return predict_post_by_trend()


