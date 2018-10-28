from flask_injector import inject
from services.provider import ItemsProvider

# items = {
#     0: {"name": "First item"}
# }

@inject(data_provider=ItemsProvider)
def search(data_provider):
    return data_provider.get()
