from email import header
from wsgiref import headers
import requests


def full_revalidate_author_posts(author_name:str, data:list):


    full_revalidate_url:str = "http://127.0.0.1:3001/api/full_revalidate_profile_posts/"

    response = requests.post(full_revalidate_author_posts, headers={'Secret-Key': '98h(F*H(F$&*H87fH$*&gtoL:TW$)*HF*84f'}, data={'data': data, 'target_author': author_name})

    if (response.status_code != 204):
        print("Can't able to re-validate frontend cache!")
        return 0

    return 1


def revalidate_post_likes_by_id(post_id:int, data:list):

    revalidate_url:str = "http://127.0.0.1:3001/api/revalidate/"

    response = requests.post(revalidate_url, headers={'Secret-Key': '98h(F*H(F$&*H87fH$*&gtoL:TW$)*HF*84f'}, data={'target_post_id': post_id, 'target_field': 'likes', 'data': data})

    if (response.status_code != 204):
        print("Can't able to re-validate frontend cache!")
        return 0

    return 1


def revalidate_post_dislikes_by_id(post_id:int, data:list):

    revalidate_url:str = "http://127.0.0.1:3001/api/revalidate/"

    response = requests.post(revalidate_url, headers={'Secret-Key': '98h(F*H(F$&*H87fH$*&gtoL:TW$)*HF*84f', 'Content-Type': 'application/json'}, json={'target_post_id': post_id, 'target_field': 'dislikes', 'data': data})

    if (response.status_code != 204):
        print("Can't able to re-validate frontend cache!")
        return 0

    return 1


def revalidate_post_comments_by_id(post_id:int, data:list):

    revalidate_url:str = "http://127.0.0.1:3001/api/revalidate/"

    response = requests.post(revalidate_url, headers={'Secret-Key': '98h(F*H(F$&*H87fH$*&gtoL:TW$)*HF*84f', 'Content-Type': 'application/json'}, json={'target_post_id': post_id, 'target_field': 'comments', 'data': data})

    if (response.status_code != 204):
        print("Can't able to re-validate frontend cache!")
        return 0

    return 1
