from instagrapi import Client
from datetime import datetime
from dateutil import parser
import pandas
import pytz

utc=pytz.UTC


ACCOUNT_USERNAME = 'dima_pivovar_fans_account'
ACCOUNT_PASSWORD = '!dimaPivovar'

channel = 'leonidvolkov' # название аккаунта

medias_list = []
with open('medias_list.txt', 'r') as medias_list_file:
    for line in medias_list_file.readlines():
        medias_list.append(line.strip())
        
start_date_1 = '2022-03-01' # начало 1
end_date_1 = '2022-03-13' # конец 1

start_date_2 = '2022-08-01' # начало 2
end_date_2 = '2022-08-31' # конец 2


start_date_1 = utc.localize(datetime.strptime(start_date_1, "%Y-%m-%d"))
end_date_1 = utc.localize(datetime.strptime(end_date_1, "%Y-%m-%d"))

start_date_2 = utc.localize(datetime.strptime(start_date_2, "%Y-%m-%d"))
end_date_2 = utc.localize(datetime.strptime(end_date_2, "%Y-%m-%d"))

cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = int(cl.user_id_from_username(channel))
user_info = cl.user_info(str(user_id))
print('Got user info')

data = {'comment': [], 'caption': [], 'link': [], 'username': []}

for i, media_link in enumerate(medias_list):
    print(f'processing {i+1}/{len(medias_list)}')
    media_pk = cl.media_pk_from_url(media_link)
    media = cl.media_info(media_pk)

    comments = cl.media_comments_chunk(media.id, (media.comment_count or 0))[0]
    for j, comment in enumerate(comments):
        # print(f'processing comment {j}/{len(comments)}')
        if (start_date_1 <= comment.created_at_utc <= end_date_1) or (start_date_2 <= comment.created_at_utc <= end_date_2):
            data['comment'].append(comment.text)
            data['caption'].append(media.caption_text)
            data['link'].append(media_link)
            data['username'].append(comment.user.username)


data_df = pandas.DataFrame.from_dict(data)
data_df.to_excel('volkov_mar.xlsx', index=False)
print('done')