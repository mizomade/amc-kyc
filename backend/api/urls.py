from ninja import NinjaAPI
from .person import router as person_router
from .house import router as house_router
from .search import router as search_router
from .veng import router as veng_router
from .qualifications import router as qualifications_router
from .occupations import router as occupations_router
from .attachments import router as attachments_router
from .certificates import router as certificates_router
from .family_tree import router as family_tree


api = NinjaAPI()

api.add_router("/person/", person_router)
api.add_router("/house/", house_router)
api.add_router("/search/", search_router)
api.add_router("/veng/", veng_router)
api.add_router("/qualifications/", qualifications_router)
api.add_router("/occupations/", occupations_router)
api.add_router("/attachments/", attachments_router)
api.add_router("/certificates/", certificates_router)
api.add_router("/family-tree/", family_tree)



urlpatterns = api._get_urls()