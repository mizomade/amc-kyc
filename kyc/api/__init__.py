from ninja import NinjaAPI
from .person import router as person_router
from .house import router as house_router
from .search import router as search_router  
from .veng import router as veng_router





api = NinjaAPI()

api.add_router("/person/", person_router)
api.add_router("/house/", house_router)
api.add_router("/search/", search_router) 
api.add_router("/veng/", veng_router)