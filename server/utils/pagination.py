from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """分页"""
    page_size = 20  # 每页大小
    max_page_size = 50  # 每页最大大小
    # page_query_param = 'page'   # 前端 url 定义的分页，默认为 page
    page_size_query_param = 'page_size'  # 前端 url 定义的每页大小
