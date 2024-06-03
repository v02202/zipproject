from starlette.routing import Route, Mount
from source.controllers import (
    files
)

routes=[
    Route('/{upload_id:int}', endpoint=files.getFiles,
        methods=['GET'], name='getFiles'),
    Route('/read/{files_id:int}', endpoint=files.readFiles,
        methods=['GET'], name='readFiles')
]