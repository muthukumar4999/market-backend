from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_swagger.views import get_swagger_view

schema_view = get_schema_view(title="Market App", renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer],
                              urlconf='market_backend.v0.urls', description="API V0",
                              url="/api/v0/")

urlpatterns = [
    path('accounts/', include(('market_backend.v0.accounts.urls', 'market_backend.v0.accounts'), namespace='accounts')),
    path('customer/', include(('market_backend.v0.customer.urls', 'market_backend.v0.customer'), namespace='customer')),
    path('delivery/', include(('market_backend.v0.delivery.urls', 'market_backend.v0.delivery'), namespace='delivery')),
    path('docs/', schema_view, name='api-docs'),
]
