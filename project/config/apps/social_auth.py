class SocialAuthSettings(object):
    AUTHENTICATION_BACKENDS = (
        'social.backends.facebook.FacebookOAuth2',
        'social.backends.twitter.TwitterOAuth',
        'social.backends.vk.VKOAuth2',
        'social.backends.github.GithubOAuth2',

        'django.contrib.auth.backends.ModelBackend'
    )

    SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        'social.pipeline.social_auth.associate_by_email',
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details',
        'social.pipeline.mail.mail_validation',
    )

    SOCIAL_AUTH_LOGIN_REDIRECT_URL = u'/'
