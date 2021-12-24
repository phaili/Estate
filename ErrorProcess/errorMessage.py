#   400 错误请求
def errorCode400(msg):
    info = {'status': 400, 'msg': msg}
    return info

# 404 没有对应的资源
def errorCode404(msg):
    info = {'status': 404, 'msg': msg}
    return info

#   403 请求被禁止
def errorCode403(msg):
    info = {'status': 403, 'msg': msg}
    return info

#   500 服务器错误
def errorCode500():
    info = {'status': 500, 'msg': '内部服务器错误'}
    return info

def successCode(msg):
    info = {'status': 200, 'msg': msg}
    return info
