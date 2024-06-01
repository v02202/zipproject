from starlette.authentication import (
    AuthenticationError, SimpleUser,
    AuthCredentials
)
from starlette_auth_toolkit.base.backends import BaseTokenAuth, BaseBasicAuth
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json, uuid, hashlib, urllib
from Crypto.Random import get_random_bytes
from datetime import datetime, timedelta
# from twilio.request_validator import RequestValidator
# from source.models import user
import jwt
from urllib.parse import urlparse
from starlette.config import Config
from ..responses.responses import error4033
config = Config(".env")
tz_offset = config("TIMEZONE", cast=int, default=8)
secret_key = config("JWT_SECRET_KEY", cast=str, default='')
aes_key = config("AES_KEY", cast=str, default='')
url_root_domain = config("URL_ROOT_DOMAIN", cast=str, default='')
md5_key=config("MD5_KEY", cast=str, default="")
app_phone_user_uuid=config("APP_PHONE_USER_UUID", cast=str, default="")
auth_token = config("TL_AUTH_TOKEN", cast=str, default="")

# def getKKdayTokenKey(user_uuid = ''):
#     device_id = str(uuid.uuid4())
#     user_uuid_str = user_uuid if user_uuid else app_phone_user_uuid
#     md5_string = f'{user_uuid_str}{device_id}{md5_key}'
#     m = hashlib.md5()
#     m.update(md5_string.encode("utf-8"))
#     return m.hexdigest(), device_id

class BasicAuth(BaseBasicAuth):

    def __init__(self):
        self.aes_key = aes_key.encode('utf-8')
        self.aes_iv = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def do_encrypt(self, data):
        if data == None:
            return None
        else:
            data = data.encode('utf-8')
            cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_iv)
            ct_bytes = cipher.encrypt(pad(data, AES.block_size))
            iv = base64.b64encode(cipher.iv).decode('utf-8')
            ct = base64.b64encode(ct_bytes).decode('utf-8')
            base_all_str = ct + ':'+ iv
            final_res = b'KK' + base64.b64encode(bytes(base_all_str, encoding='utf-8'))
            return final_res.decode('utf-8')

    def do_decrypt(self, data):
        if data == None:
            return None
        else:
            bytes_data = data[2:].encode('utf-8')
            aes_data = base64.b64decode(bytes_data).decode('utf-8')
            ct, iv = aes_data.split(':')
            ct_base = base64.b64decode(ct.encode('utf-8'))
            iv_base = base64.b64decode(iv.encode('utf-8'))
            cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_iv)
            pad_data = cipher.decrypt(ct_base)
            utf8_data = unpad(pad_data, AES.block_size)
            return utf8_data.decode('utf-8')

    async def authenticate(self, request):
        if "x-api-key" in request.headers:
            api_token = request.headers["x-api-key"]
            try:
                content = jwt.decode(api_token, secret_key, algorithms=["HS256"])
                print('content', content)
            except:
                raise AuthenticationError('x-api-key JWT secret is invalid')
            expire_time = datetime.strptime(content['expired_time'], "%Y-%m-%d %H:%M:%S")
            now_time = datetime.utcnow() + timedelta(hours=tz_offset)
            if now_time > expire_time:
                raise AuthenticationError('API token is expired')
            if "authorization" not in request.headers :
                return
            else:
                auth = request.headers["authorization"]
                try:
                    scheme, credentials = auth.split()
                except:
                    raise AuthenticationError('No bearer')
                try:
                    json = jwt.decode(credentials, secret_key, algorithms=["HS256"])
                except:
                    raise AuthenticationError('Access token JWT secret is invalid')
                print('app', json)
                # check token
                access_list = ['/api/users/access', '/api/oauth/access']
                path = request.url.path
                if 'token' not in json:
                    print('Invalid access token')
                    raise AuthenticationError('Forbidden')
                else:
                    if json['token'] == 'access-token':
                        pass
                    else:
                        if json['token'] == 'refresh-token' and path in access_list:
                            pass
                        else:
                            print('Invalid access token')
                            raise AuthenticationError('Forbidden')
                # check expired_time
                expire_time = datetime.strptime(json['expired_time'], "%Y-%m-%d %H:%M:%S")
                now_time = datetime.utcnow() + timedelta(hours=tz_offset)
                if now_time > expire_time:
                    raise AuthenticationError('Access token is expired')
                else:
                    return AuthCredentials(["authenticated"]), SimpleUser(json)
        elif "x-twilio-signature" in request.headers:
            pass
        else:
            request_path = str(request.url)
            domain = urlparse(request_path).netloc
            path = request.url.path
            domain_list = [url_root_domain, 'localhost:8000']
            path_list = [
                '/api/image/read',
                '/api/webhook',
            ]
            if domain in domain_list:
                if "authorization" not in request.headers :
                    return
                elif path in path_list:
                    return
                else:
                    auth = request.headers["authorization"]
                    try:
                        scheme, credentials = auth.split()
                    except:
                        raise AuthenticationError('No bearer')
                    try:
                        json = jwt.decode(credentials, secret_key, algorithms=["HS256"])
                        print('web', json)
                    except:
                        raise AuthenticationError('Access token JWT secret is invalid')
                    # check token
                    access_list = ['/api/users/refresh/token']
                    if 'token' not in json:
                        print('Invalid access token')
                        raise AuthenticationError('Forbidden')
                    else:
                        if json['token'] == 'access-token':
                            pass
                        else:
                            if json['token'] == 'refresh-token' and path in access_list:
                                pass
                            else:
                                print('Invalid access token')
                                raise AuthenticationError('Forbidden')
                    # check expired_time
                    expire_time = datetime.strptime(json['expired_time'], "%Y-%m-%d %H:%M:%S")
                    now_time = datetime.utcnow() + timedelta(hours=tz_offset)
                    if now_time > expire_time:
                        raise AuthenticationError('Access token is expired')
                    else:
                        return AuthCredentials(["authenticated"]), SimpleUser(json)
            else:
                if path == '/api/webhook' or path == '/api/webhook/tgbot' or '/api/twilio/voice':
                    return
                else:
                    raise AuthenticationError('Invalid api credentials')

def on_auth_error(request, exc: Exception):
    return error4033(str(exc))
                

# validator = RequestValidator(auth_token)


# def twilio_signature_url(url, params, twilio_signature):
#     response = validator.validate(url, params, twilio_signature)
#     return response