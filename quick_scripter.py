'''PRE REQ.'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spade_ubuntu.settings")

import django
django.setup()

from django.core.management import call_command
'''PRE REQ. OVER'''

from django.contrib.auth.models import User
from spado_ubuntu.models import Post, Account, user_post_action

users = ['avsar_savaliya', 'author_1', 'author_2', 'author_3', 'jevik_pandya', 'jay_pandya', 'ved_pandya', 'kartavya_dave', 'sujan_rokad', 'vivek_gohil', 'rutvik_pandya', 'shivam_pandya', 'omkar_madhak']


'''Updating User'''

def generate_users(users:list):
    for user_name in users:
        try:
            u = User.objects.create(username=user_name, password=user_name+'123', first_name=user_name.split('_')[0], last_name=user_name.split('_')[-1], email=''.join(user_name.split('_'))+'@gmail.com')
            u.save()
        except Exception as e:
            print(e)

# generate_users(users)

'''Updating Account'''
def link_account_to_user():
    for user in list(User.objects.all()):
        try:
            a = Account.objects.create(user_name=user, is_valid=True)
            a.save()
        except Exception as e:
            print('ERROR: ', e)

# link_account_to_user()

'''Updating Posts'''

dl = {

    1:[5,11,9,7],
    2:[8,7],
    3:[9,7,6,12],
    4:[11,14,5,12,7],
    5:[12,7,9,10,14],
    6:[5,6,8],
    7:[7,6,12,9]

}

dd = {
    # post_id:[user_ids]
    1:[14, 8],
    3:[11],
    2:[5]
}

titles = ["Bug in pubg (beneficial)", "Release date of pubg new level","top 10 headshots ", "Tips, how to rush", "Get m416 skin by doing…", "Avoid these mistakes", "How to improve rank and K/D"]

dummy_descr = "<p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ipsam aut commodi nisi suscipit eveniet quisquam? Totam, veritatis magni! Ducimus, incidunt in quod cumque iste perspiciatis cupiditate delectus qui assumenda architecto! Error voluptatem nisi accusantium unde, necessitatibus animi architecto, sequi praesentium recusandae dolorem culpa laboriosam, deserunt soluta eos repellendus. Inventore quam esse quas modi, dolorem cupiditate ut a accusamus quos ipsa recusandae deserunt, corporis aspernatur aut dolorum blanditiis fuga quis iusto quaerat atque tenetur quae commodi? Consectetur vitae voluptatum repudiandae dolor ratione veniam vel labore aut maiores! Quis autem, commodi itaque eveniet, harum provident voluptate nemo perferendis ea maiores cupiditate voluptates nostrum iusto eligendi esse fugit voluptatibus. Consectetur, et voluptate qui accusamus a suscipit debitis, explicabo ea vero minus fuga quod.</p>"

def generate_dummy_posts(titles):
    import random as r
    for i in titles:
        a = Account.objects.get(user_name=User.objects.get(username=r.choices(['author_1', 'author_2', 'author_3'])[0]))
        print('Debugging: a--> ', a)
        ne = Post.objects.create(title=i, descr=dummy_descr, author=a)
        ne.save()

# generate_dummy_posts(titles)


def update_post_likes_table(d:dict, table='main'):
    if table == "main":
        for post_id, user_ids in d.items():
            p = Post.objects.get(pk=post_id)
            for i in user_ids:

                u = User.objects.get(pk=i)
                p.likes.add(u)
                p.save()
    else:
        for post_id, user_ids in d.items():
            for i in user_ids:
                u = User.objects.get(pk=i)
                p = Post.objects.get(pk=post_id)
                if not (user_post_action.objects.filter(user=u, post=p, action=True).exists()):
                    new_enrty = user_post_action.objects.create(user=u, post=p, action=True)
                    new_enrty.save()
                    
                else:
                    pass



update_post_likes_table(dl)
update_post_likes_table(dl, table='secondary')
        
def update_post_dislikes_table_old(d:dict):
    for post_id, user_ids in d.items():
        p = Post.objects.get(pk=post_id)
        for i in user_ids:

            u = User.objects.get(pk=i)
            p.dislikes.add(u)
            p.save()


def update_post_dislikes_table(d:dict, table='main'):
    if table == "main":
        for post_id, user_ids in d.items():
            p = Post.objects.get(pk=post_id)
            for i in user_ids:

                u = User.objects.get(pk=i)
                p.dislikes.add(u)
                p.save()
    else:
        for post_id, user_ids in d.items():
            for i in user_ids:
                u = User.objects.get(pk=i)
                p = Post.objects.get(pk=post_id)
                if not (user_post_action.objects.filter(user=u, post=p, action=False).exists()):
                    new_enrty = user_post_action.objects.create(user=u, post=p, action=False)
                    new_enrty.save()
                    
                else:
                    pass

update_post_dislikes_table(dd)
update_post_dislikes_table(dd, table='secondary')


# update_post_dislikes_table(dd)
