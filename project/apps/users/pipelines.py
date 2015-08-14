import json
import uuid
from django.shortcuts import redirect
from requests import request, HTTPError

from django.core.files.base import ContentFile

USER_FIELDS = ['username', 'email']

'''
if not email given:
ask for email
if email not exists:
    all good, go create user, send verification
else:
    get existed user, make inactive, send him notification
'''


def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    test = 123

    if not user:
        return
    if not user.email:
        return redirect('users:acquire_email', user_id=user.id)


def create_user(strategy, backend, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name) or details.get(name))
                        for name in strategy.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return

    if backend.name == 'facebook':
        fields[u'username'] = u'fb__%s__%s' % (fields[u'username'], uuid.uuid1().hex[:8])
    elif backend.name == 'vk-oauth2':
        fields[u'username'] = u'vk__%s__%s' % (fields[u'username'], uuid.uuid1().hex[:8])
    elif backend.name == 'odnoklassniki-oauth2':
        fields[u'username'] = u'ok__%s__%s' % (fields[u'username'], uuid.uuid1().hex[:8])
    elif backend.name == 'twitter':
        fields[u'username'] = u'tw__%s__%s' % (fields[u'username'], uuid.uuid1().hex[:8])

    fields[u'display_name'] = details.get(u'fullname') or details.get(u'username')

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }


def save_user_image(backend, details, user, response, is_new=False, *args, **kwargs):
    # if not is_new: return
    if backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture?type=large'.format(response['id'])
    elif backend.name == 'vk-oauth2':
        try:
            user_id = response.get(u'user_id')
            user_data_url = u'https://api.vk.com/method/users.get?user_id=%s&v=5.23&fields=photo_big' % user_id
            response = json.loads(request('GET', user_data_url).content)
            url = response.get(u'response')[0][u'photo_big']
            if url == u'http://vk.com/images/camera_200.png':
                return 
        except:
            return
        # url = response.get(u'user_photo')
    elif backend.name == 'odnoklassniki-oauth2':
        url = response.get(u'pic_2')
        if not url: url = response.get(u'pic_1')
    elif backend.name == 'twitter':
        url = response.get(u'profile_image_url')
        if url and u'_normal' in url:
            url = url.replace(u'_normal', u'')
    else: return

    try:
        response = request('GET', url)
        response.raise_for_status()
    except HTTPError:
        pass
    else:
        url_ext = url.rsplit(u'.', 1)[1]
        ext = u'jpg'
        if url_ext in [u'jpg', u'png', u'jpeg', u'gif']:
            ext = url_ext
        user.image.save(u'{0}_social.{1}'.format(user.id, ext), ContentFile(response.content))
        user.save()
