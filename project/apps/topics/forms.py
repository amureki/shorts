from django import forms

from topics.models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = (u'title', u'url')

    def clean_url(self):
        url = self.cleaned_data.get(u'url')
        if url and u'http://' not in url and u'https://' not in url:
            url = u'http://%s' % url

        return url
