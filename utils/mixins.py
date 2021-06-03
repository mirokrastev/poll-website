from django.core.paginator import Paginator


class PaginateObjectMixin:
    paginate_by = 10
    orphans = 0

    def paginate(self, queryset, page, *, paginate_by=None, orphans=None):
        kwargs = {
            'per_page': paginate_by or self.paginate_by,
            'orphans': orphans or self.orphans
        }

        paginator_object = Paginator(queryset, **kwargs)
        result_object = paginator_object.page(page)

        return (paginator_object, result_object)
