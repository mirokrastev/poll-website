from django.contrib import admin
from poll.models import Poll, Answer, Vote, Comment

admin.site.register(Poll)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Comment)
