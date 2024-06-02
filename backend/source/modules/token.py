from datetime import datetime, timedelta
import jwt
from starlette.config import Config
config = Config(".env")
tz_offset = config("TIMEZONE", cast=int, default=8)
secret_key = config("JWT_SECRET_KEY", cast=str, default='')

def generateToken(**kwargs):
    # generate access token
    print('kwargs: ', kwargs)
    expired_time = datetime.now() + timedelta(hours=tz_offset) + timedelta(hours=kwargs['expires'])
    formated_time = datetime.strftime(expired_time, "%Y-%m-%d %H:%M:%S")
    generate_token = jwt.encode(
        {'expired_time':formated_time, 'token':'access-token', **kwargs}, secret_key, algorithm="HS256")
    # generate refresh token
    refresh_expired_time = datetime.now() + timedelta(hours=tz_offset) + timedelta(hours=36)
    refresh_formated_time = datetime.strftime(refresh_expired_time, "%Y-%m-%d %H:%M:%S")
    generate_refresh_token = jwt.encode(
        {'expired_time':refresh_formated_time, 'token':'refresh-token', **kwargs}, secret_key, algorithm="HS256")
    return generate_token, generate_refresh_token