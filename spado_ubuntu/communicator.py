import requests
from django.db import connection
from spado_ubuntu.sql_queries import TRENDING_POST_QUERY


def predict_post_by_trend() -> list:
    try:

        with connection.cursor() as c:
            c.execute(TRENDING_POST_QUERY)
            return [row[0] for row in c.fetchall()]

    except Exception as e:
        print("can't predict post [TRENDING], ", e)
        return []
