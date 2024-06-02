from starlette.routing import Route, Mount
from source.controllers import (
    supplier
)

routes=[
    Route('/create', endpoint=supplier.createSupplier,
        methods=['POST'], name='createSupplier'),
    Route('/{supplier_id:int}', endpoint=supplier.getSupplier,
        methods=['GET'], name='getSupplier'),
]