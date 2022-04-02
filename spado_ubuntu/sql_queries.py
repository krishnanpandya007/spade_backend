TRENDING_POST_QUERY = 'select post_id, ((case when (sum((case when a.action then 1 else -1 end))-1)>0 then (sum((case when a.action then 1 else -1 end))-1) else 0 end)^0.8)*(1*10000)/((select extract(epoch from (created_on-now()::timestamp)) from spado_ubuntu_post where id=a.post_id limit 1)::int+2)^2 as hn_score from spado_ubuntu_user_post_action a group by post_id order by hn_score desc;'

# # (Args: post_id1, user_id1) (SUSPECIOUS)
# SIMILAR_POST_QUERY_I2I = 'select distinct post_id, get_score_of_post_i2i(%d, post_id::int) as score from spado_user_post_action where user_id!=%d and post_id not in (select b.post_id from spado_user_post_action b where b.user_id=%d) order by score desc;'

#Args: (user_id_1, post_id_1)
SIMILAR_POST_QUERY_I2I = 'select distinct post_id, get_score_of_post_i2i(post_id::int, %d) as score from spado_ubuntu_user_post_action where post_id!=%d and user_id not in (select b.user_id from spado_ubuntu_user_post_action b where b.post_id=%d) order by score desc;'

SIMILAR_POST_QUERY_U2U = 'select distinct post_id, get_score_of_post(%d, post_id::int) as score from spado_user_post_action where user_id!=%d and post_id not in (select b.post_id from spado_user_post_action b where b.user_id=%d) order by score desc;'

RECENT_POST_QUERY = "select b.post_id as id, round((case when sum((case when b.action then 1 else -1 end)) > 0 then 1 else -1 end)*log10((case when sum((case when b.action then 1 else -1 end))>1 then sum((case when b.action then 1 else -1 end)) else 1 end))::int + (select extract(epoch from (a.created_on-now()::timestamp)) as reddit_score from spado_post a where a.id=b.post_id limit 1)/45000, 5) from spado_user_post_action b group by b.post_id having (select DATE_PART('%s', now()-a.created_on) from spado_post a limit 1)<=%d order by round desc limit 5;"