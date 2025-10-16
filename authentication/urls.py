from django.urls import path
from allauth.account.views import LogoutView
from . import views
from .views import CustomPasswordChangeView, redirect_to_dashboard

urlpatterns = [
    path('', views.redirect_to_dashboard, name='dashboard'),

    # Token-based dashboard (legacy support)
    path('dashboard/<str:token>/<str:role>/', views.dashboard_signed_with_role, name='dashboard_signed_with_role'),
    # Session-based dashboard (new)
    path('dashboard/', views.dashboard_signed_with_role, name='dashboard_session'),

    path('unauthorized/', views.unauthorized, name='unauthorized'),

    path('logout/', LogoutView.as_view, name='account_logout'),

    path('resend-verification/', views.resend_verification, name='resend_verification'),

    path("verification-sent/", views.verification_sent, name="verification_sent"),

    path('accounts/email-verification-required/', views.email_verification_required, name='email_verification_required'),

    path('accounts/profile/', views.profile, name='profile'),

    path('accounts/settings/', views.settings, name='settings'),

    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),

    # Token optional patterns
    path('manage-user-profiles/', views.manage_user_profiles, name='manage_user_profiles_session'),
    path('manage-user-profiles/<str:token>/', views.manage_user_profiles, name='manage_user_profiles'),

    path('search-users/', views.search_users, name='search_users'),

    path('add-users/', views.add_user, name="add_user_session"),
    path('add-users/<str:token>/', views.add_user, name="add_user"),

    path("edit-user/<int:user_id>/", views.edit_user, name="edit_user_session"),
    path("edit-user/<str:token>/<int:user_id>/", views.edit_user, name="edit_user"),

    path("archive-user/<int:user_id>/", views.archive_user, name="archive_user_session"),
    path("archive-user/<str:token>/<int:user_id>/", views.archive_user, name="archive_user"),

    path('unarchive-user/<int:user_id>/', views.unarchive_user, name='unarchive_user_session'),
    path('unarchive-user/<str:token>/<int:user_id>/', views.unarchive_user, name='unarchive_user'),

    path('clear-welcome-flag/', views.clear_welcome_flag, name='clear_welcome_flag'),

    path('update-profile-name/', views.update_profile_name, name='update_profile_name'),

    path('update-avatar/', views.update_avatar, name='update_avatar'),

    path('update-profile-email/', views.update_profile_email, name='update_profile_email'),

    path('api/dashboard/', views.dashboard_api, name='dashboard_api'),
]