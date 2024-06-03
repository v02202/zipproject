from starlette.routing import Route, Mount
from source.controllers import (
    upload
)

routes=[
    Route('/zip', endpoint=upload.uploadZip,
        methods=['POST'], name='uploadZip'),
    Route('/download/{upload_id:int}', endpoint=upload.downloadZip,
        methods=['GET'], name='downloadZip')
]