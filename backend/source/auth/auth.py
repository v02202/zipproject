from starlette.authentication import (
    AuthenticationError, SimpleUser,
    AuthCredentials
)
from starlette_auth_toolkit.base.backends import BaseTokenAuth, BaseBasicAuth
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from datetime import datetime, timedelta
import jwt
from starlette.config import Config
from ..responses.responses import error4033
config = Config(".env")
tz_offset = config("TIMEZONE", cast=int, default=8)
secret_key = config("JWT_SECRET_KEY", cast=str, default='')


class BasicAuth(BaseBasicAuth):

    def __init__(self):
        self.aes_key = b'0102030405060708'
        self.aes_iv = b'0807060504030201'

    def do_encrypt(self, data):
        if data == None:
            return None
        else: 
            utf8_data = data.encode('utf-8')
            # print('length of utf8_data', len(utf8_data))
            pad_data = pad(utf8_data, AES.block_size)
            pad_key = pad(self.aes_key, AES.block_size)
            cipher = AES.new(pad_key, AES.MODE_CBC, self.aes_iv)
            aes_data = cipher.encrypt(pad_data)
            # print('length of encrypt', len(base64.b64encode(aes_data).decode('utf-8')))
            return base64.b64encode(aes_data).decode('utf-8')

    def do_decrypt(self, data):
        if data == None:
            return ''
        else:
            aes_data = base64.b64decode(data)
            pad_key = pad(self.aes_key, AES.block_size)
            cipher = AES.new(pad_key, AES.MODE_CBC, self.aes_iv)
            pad_data = cipher.decrypt(aes_data)
            utf8_data = unpad(pad_data, AES.block_size)
            return utf8_data.decode('utf-8')

    async def authenticate(self, request):
        if "x-api-key" in request.headers:
            api_token = request.headers["x-api-key"]
            content = jwt.decode(api_token, secret_key, algorithms=["HS256"])
            try:
                content = jwt.decode(api_token, secret_key, algorithms=["HS256"])
                print('content', content)
            except:
                raise AuthenticationError('x-api-key JWT secret is invalid')
            expire_time = datetime.strptime(content['expired_time'], "%Y-%m-%d %H:%M:%S")
            now_time = datetime.now() + timedelta(hours=tz_offset)
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
                # check token
                access_list = ['/api/users/refresh/token']
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
                now_time = datetime.now() + timedelta(hours=tz_offset)
                if now_time > expire_time:
                    raise AuthenticationError('Access token is expired')
                else:
                    return AuthCredentials(["authenticated"]), SimpleUser(json)
        else:
            path = request.url.path
            path_list = [
                '/api/apikey/store',
                '/api/apikey/token',
            ]
            if path in path_list:
                return
            else:
                raise AuthenticationError('Invalid api credentials')

def on_auth_error(request, exc: Exception):
    return error4033(str(exc))
                
