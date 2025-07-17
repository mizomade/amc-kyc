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
from .tree_view import router as tree_view
from .user import router as user_router

from .religion import router as religion_router
from .denomination import router as denomination_router
from .role import router as role_router

from .reports import router as reports_router
from api.education import router as education_router
from api.occupationlist import router as occuaptionlist_router
from api.documenttypelist import router as documenttypelist_router
from api.forentry import router as forentry_router
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
api.add_router("/tree-view/", tree_view)
api.add_router("/reports/", reports_router)

api.add_router("/user/", user_router)
api.add_router("/religion/", religion_router)
api.add_router("/denomination/", denomination_router)
api.add_router("/role/", role_router)
api.add_router("/education/", education_router)
api.add_router("/occupationlist/",occuaptionlist_router)
api.add_router("/documentypelist/",documenttypelist_router)
api.add_router("/forentry/",forentry_router)
urlpatterns = api._get_urls()