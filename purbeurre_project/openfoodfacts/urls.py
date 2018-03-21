urlpatterns = [
    url(r'^openfoodfacts/', include('openfoodfacts.urls')),
    url(r'^admin/', admin.site.urls)
]
