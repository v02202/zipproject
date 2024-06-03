from starlette.routing import Route, Mount
from source.controllers import (
    upload
)

routes=[
    Route('/zip', endpoint=upload.uploadZip,
        methods=['POST'], name='uploadZip'),
    Route('/history', endpoint=upload.uploadHistory,
        methods=['GET'], name='uploadHistory'),
]