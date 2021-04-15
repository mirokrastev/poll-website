from django.contrib import admin
from poll.models import Poll, Answer, Vote

admin.site.register(Poll)
admin.site.register(Answer)
admin.site.register(Vote)
