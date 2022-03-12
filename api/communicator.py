import requests

def predict_post_for_userid(is_authenticated:bool, user_id: int, catagory :str, **kwargs) -> dict:

    # is_authenticated : BOOL


    data = {"user_id": user_id}
    if kwargs:
        for key, val in kwargs.items():
            data[key] = val


    res = requests.post("http://127.0.0.1:4000/predict_post/"+catagory, json=data)
    # print(res.json())

    try:
        res = res.json()["post_ids"]
        return res
    except Exception as e:
        print("[POST_PREDICTION_FETCHING_FAILED]: %s" % (e))
        return False

    # return res.json()
    # return []
