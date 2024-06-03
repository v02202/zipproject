from starlette.responses import JSONResponse, Response
from starlette.status import (
    HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST
)
from settings.response import STATUS

def responseWithXML(media):
    return Response(media, status_code = HTTP_200_OK, media_type="application/xml")

def responseWithAudio(media):
    return Response(media, status_code = HTTP_200_OK, media_type="audio/basic")

def responseWithBytes(bytes):
    return Response(bytes, status_code = HTTP_200_OK, media_type="application/x-binary")

def responseWithMedia(media, ETag, http_code = HTTP_200_OK):
    # headers = {"Cache-Control": "public, max-age=600", "Last-Modified": "Tue, 27 Sep 2022 14:25:00 GMT", "ETag": "gergWer2rqe2ryegRETWRQ"}
    headers = {"Cache-Control": "public, max-age=3600"}
    return Response(media, status_code = http_code, media_type="image/png", headers=headers)

def responseWithPDF(media):
    return Response(media, status_code = HTTP_200_OK, media_type="application/pdf")

def successWithData(data):
    res = {
        'metadata': {
            'status': '0000',
            'desc': 'success'
        },
        'data': data
    }
    return JSONResponse(res, status_code = HTTP_200_OK)

def success():
    res = {
        'metadata': {
            'status': '0000',
            'desc': 'success'
        },
        'data': None
    }
    return JSONResponse(res, status_code = HTTP_200_OK)

def error406():
    res = {
        'metadata': {
            'status': '1000',
            'desc': STATUS['1000']
        },
        'data': {'error_message':'no_permission'}
    }
    return JSONResponse(res, status_code = HTTP_406_NOT_ACCEPTABLE)

def error4061(data):
    res = {
        'metadata': {
            'status': '4061',
            'desc': STATUS['4061']
        },
        'data': data
    }
    return JSONResponse(res, status_code = HTTP_406_NOT_ACCEPTABLE)

def error4062(error_message):
    res = {
        'metadata': {
            'status': '4061',
            'desc': STATUS['4061']
        },
        'data': error_message
    }
    return JSONResponse(res, status_code = HTTP_406_NOT_ACCEPTABLE)

def error4063(error_message):
    res = {
        'metadata': {
            'status': '4063',
            'desc': error_message
        },
        'data': error_message
    }
    return JSONResponse(res, status_code = HTTP_406_NOT_ACCEPTABLE)

def error4064(error_message):
    res = {
        'metadata': {
            'status': '4064',
            'desc': STATUS['4064']
        },
        'data': error_message
    }
    return JSONResponse(res, status_code = HTTP_406_NOT_ACCEPTABLE)

def error4031():
    res = {
        'metadata': {
            'status': '4031',
            'desc': STATUS['4031']
        },
        'data': None
    }
    return JSONResponse(res, status_code = HTTP_403_FORBIDDEN)

def error4032():
    res = {
        'metadata': {
            'status': '4032',
            'desc': STATUS['4032']
        },
        'data': None
    }
    return JSONResponse(res, status_code = HTTP_403_FORBIDDEN)

def error4033(error_message):
    res = {
        'metadata': {
            'status': '4033',
            'desc': STATUS['4033']
        },
        'data': error_message
    }
    return JSONResponse(res, status_code = HTTP_403_FORBIDDEN)

def error4000():
    res = {
        'metadata': {
            'status': '4000',
            'desc': STATUS['4000']
        },
        'data': None
    }
    return JSONResponse(res, status_code = HTTP_400_BAD_REQUEST)

def error4001(error_message):
    res = {
        'metadata': {
            'status': '4000',
            'desc': STATUS['4000']
        },
        'data': error_message
    }
    return JSONResponse(res, status_code = HTTP_400_BAD_REQUEST)

def error4221(error_message):
    res = {
        'metadata': {
            'status': '4221',
            'desc': STATUS['4221']
        },
        'data': error_message
    }
    return JSONResponse(res, status_code = HTTP_422_UNPROCESSABLE_ENTITY)
