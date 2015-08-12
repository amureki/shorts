from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View, CreateView

from braces.views import LoginRequiredMixin

from comments.forms import CommentForm
from comments.models import Comment
from topics.forms import TopicForm
from topics.models import Topic


class TopicListView(ListView):
    model = Topic
    template_name = u'topics/list.html'
    context_object_name = u'topics'


class TopicDetailView(DetailView):
    model = Topic
    template_name = u'topics/detail.html'
    context_object_name = u'topic'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context[u'comment_form'] = CommentForm
        return context


class TopicSubmitView(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = u'topics/submit.html'
    form_class = TopicForm

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.user = self.request.user
        topic.save()
        return HttpResponseRedirect(topic.get_absolute_url())


class TopicVoteView(LoginRequiredMixin, View):
    def get_topic(self, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise Http404
        return topic

    def post(self, request, *args, **kwargs):
        topic_id = kwargs.get(u'pk', 0)
        topic = self.get_topic(topic_id)
        vote = request.POST.get(u'vote', u'up')

        if vote == u'up':
            topic.vote(request.user, 1)
        elif vote == u'down':
            topic.vote(request.user, -1)
        next_page = request.GET.get(u'next', topic.get_absolute_url())
        return HttpResponseRedirect(next_page)


class TopicCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.save()
        return HttpResponseRedirect(comment.topic.get_absolute_url())
