"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from metrics.views import RadarChartEndpoint, get_radar_metrics
from teams.views import get_player_by_id, get_players

urlpatterns = [
    path("metrics/player", get_players, name="get_players"),
    path("metrics/radar", get_radar_metrics, name="get_radar_metrics"),
    path("radar", RadarChartEndpoint.as_view(), name="get_radar_chart"),
    path("teams/players/<int:player_id>", get_player_by_id, name="get_player_by_id"),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]