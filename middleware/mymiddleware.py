import logging

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404, JsonResponse
from ErrorProcess import errorMessage as eM


class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        a = 1
        # print("")
        # 执行路由之前被调用，在每个请求上调用，返回None或HttpResponse对象。

    #
    #     def process_view(self, request, callback, callback_args, callback_kwargs):
    #         # 调用视图之前被调用，在每个请求上调用，返回None或HttpResponse对象
    #         # Callback：当前请求对应的视图函数
    #
    #     def process_response(self, request,response):
    #         # 所有响应返回浏览器之前被调用，在每个请求上调用，返回HttpResponse对象
    #
    def process_exception(self, request, exception):
        # 只要在调用视图时一出现异常，就可以捕捉，返回HttpResponse对象
        error_msg = '\nRequest Body:{},\nRequest Url:{},\nRequest Method:{},\n{}'.format(request.body,
                                                                                         request.get_raw_uri(),
                                                                                         request.method, exception)
        print(error_msg)
        return JsonResponse(eM.errorCode500(), safe=False, json_dumps_params={"ensure_ascii": False})
