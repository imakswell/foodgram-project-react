from rest_framework.pagination import PageNumberPagination


class AddPageLimitPaginator(PageNumberPagination):
    page_size_query_param = 'limit'
