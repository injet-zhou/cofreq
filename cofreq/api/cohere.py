import cohere
from conf.config import settings

def new_cohere():
    co = cohere.Client(settings.api_key.cohere)
    return co