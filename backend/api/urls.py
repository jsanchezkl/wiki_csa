from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'menu', views.MenuItemViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'departments', views.DepartmentViewSet, basename='departments')  # Alias para compatibilidad
router.register(r'pages', views.WikiPageViewSet)
router.register(r'sections', views.WikiSectionViewSet)
router.register(r'media', views.MediaFileViewSet)
router.register(r'updates', views.RecentUpdateViewSet)
router.register(r'settings', views.SiteSettingsViewSet)

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('dashboard/', views.dashboard_data, name='dashboard'),
    path('sidebar/', views.sidebar_menu, name='sidebar-menu'),
    path('search/', views.search_view, name='search'),
    path('categories/tree/', views.categories_tree, name='categories-tree'),
    path('admin/stats/', views.admin_stats, name='admin-stats'),
    
    # Chat endpoints
    path('chat/', views.chat_message, name='chat-message'),
    path('chat/history/', views.chat_history, name='chat-history'),
    path('chat/index/', views.chat_index, name='chat-index'),
    path('chat/stats/', views.chat_stats, name='chat-stats'),
    
    # Auth endpoints
    path('auth/login/', views.login_view, name='auth-login'),
    path('auth/refresh/', views.refresh_token_view, name='auth-refresh'),
    path('auth/logout/', views.logout_view, name='auth-logout'),
    path('auth/me/', views.me_view, name='auth-me'),
    path('auth/check-admin/', views.check_admin, name='auth-check-admin'),
    
    path('', include(router.urls)),
]
