class PollDataMixin:
    """
    Mixin to share logic for Poll Data (percents, likes, etc)
    It should be inherited by View with queryset and votes attributes
    """

    def get_answer_json(self):
        answers_dict = {}
        for answer in self.queryset:
            votes = self.votes.filter(answer=answer)
            answers_dict[str(answer)] = (len(votes), (len(votes) * 100) / (len(self.votes) or 1))
        return answers_dict
