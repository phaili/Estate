# Create your views here.
import json

from django.http import JsonResponse
from django.core.mail import send_mail
from ErrorProcess import errorMessage as eM
from Estate1 import settings

# 发送邮件
def check_mail(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            email = req.get('email', '')
            if email == '':
                return JsonResponse(eM.errorCode404('请输入邮箱'), safe=False)
            else:
                msg = req.get('msg', '')
                send_mail(
                    subject='模型报告',
                    message=msg,
                    from_email=settings.EMAIL_HOST_USER,
                    # 目的邮箱
                    recipient_list=[]
                )
            return JsonResponse(eM.successCode('发送成功'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(eM.errorCode404('发送失败'), safe=False)
    return JsonResponse(eM.errorCode400('错误请求'), safe=False)