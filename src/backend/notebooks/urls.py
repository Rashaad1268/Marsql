from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

from . import views
from chat.views import ChatMessageViewSet


router = DefaultRouter()
router.register("notebooks", views.NoteBookViewSet)

notebooks_router = routers.NestedSimpleRouter(router, "notebooks", lookup="notebook")
notebooks_router.register("cells", views.NoteBookCellViewSet, basename="notebook_cell_viewset")
notebooks_router.register("messages", ChatMessageViewSet, basename="notebook_chat_messages")

urlpatterns = router.urls + notebooks_router.urls
