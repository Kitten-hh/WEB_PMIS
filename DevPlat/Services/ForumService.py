import json
from DataBase_MPMS.models import Task,Users
import requests
from django.conf import settings
from html import escape
import re

cateagory = settings.FORUM_POST_CATEGORY
class ForumService(object):
    def post_task(self, task:Task):
        login_url = settings.FORUM_LOGIN_URL
        post_url = settings.FORUM_POST_TOPIC
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
        
        username = task.contact
        qs = Users.objects.values('username','password').filter(username=username)
        if len(qs) == 0:
            raise Exception('沒有用戶:{0}'.format(qs[0]['username']))
        username = qs[0]['username']
        password = qs[0]['password']
        with requests.session() as s:
            resp = s.get(login_url, headers=headers, verify=False)
            csrf_token = resp.cookies['csrftoken']
            headers['X-CSRFToken'] = csrf_token
            login_headers = headers.copy()
            login_headers['X-Requested-With'] = 'XMLHttpRequest'
            resp = s.post(login_url, headers=login_headers, data={'username':username,'password':password})
            if resp.json()['state'] != 200:
                raise Exception("登錄不成功")
            else:
                resp = s.post(post_url,headers=headers, data=self.convert_task_to_topic(task))
                if resp.json()['state'] != 200:
                    raise Exception('Post不成功')
                else:
                    return resp.json()['data']
        return None

    def encrypt(self, value):
        key = 47639
        char_arr = list(value)
        for index,c in enumerate(char_arr):
            char_arr[index] = c^key
        return ''.join(char_arr)

    def convert_task_to_topic(self, task:Task):
        title = task.task
        if len(title) > 80:
            title = title[0:80]
        content = task.task
        if content:
            str_arr = escape(task.task).split("\n")
            new_str_arr = []
            for line in str_arr:
                if re.search(r'^[\t\s]+', line):
                    begin_str = ""
                    for charStr in line:
                        if charStr == " ":
                            begin_str += "&nbsp;"
                        elif charStr == "\t":
                            begin_str += "&emsp;"
                        else:
                            break;
                    new_str_arr.append(begin_str+line.strip())
                else:
                    new_str_arr.append(line.strip())
            content = "<p>"+"</p><p>".join(new_str_arr)+"</p>"
        return  {
                'category_no':None,
                'topics_title':title,
                'topics_content':content,
                'topics_content_text':task.task,
                'topics_attr': 0
                }
