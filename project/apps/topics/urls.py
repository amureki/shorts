from django.conf.urls import patterns, url

from topics.views import TopicListView, TopicDetailView, TopicSubmitView, TopicVoteView, TopicCommentView

urlpatterns = patterns(
    u'topics.views',

    url(r'^$', TopicListView.as_view(), name=u'list'),
    url(r'^submit/$', TopicSubmitView.as_view(), name=u'submit'),
    url(r'^(?P<pk>\d+)/$', TopicDetailView.as_view(), name=u'detail'),
    url(r'^(?P<pk>\d+)/vote/$', TopicVoteView.as_view(), name=u'vote'),
    url(r'^(?P<pk>\d+)/comment/$', TopicCommentView.as_view(), name=u'comment'),

)
