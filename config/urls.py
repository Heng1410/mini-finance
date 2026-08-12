from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("company.urls")),
    path("api/v1/", include("department.urls")),
    path("api/v1/", include("employee.urls")),
    path("api/v1/", include("role.urls")),
    path("api/v1/", include("user.urls")),
    path("api/v1/", include("authentication.urls")),
    path("api/v1/", include("account.urls")),
    path("api/v1/", include("journal.urls")),
    path("api/v1/", include("ledger.urls")),
    path("api/v1/", include("accounts_receivable.urls")),
    path("api/v1/", include("sequence.urls")),
    path("api/v1/", include("inventory.urls")),
    path("api/v1/", include("sales_order.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
