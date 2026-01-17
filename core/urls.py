from django.urls import path 
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # path('proyectos/', views.lista_proyectos, name='lista_proyectos'),
    path('proyectos/nuevo/', views.crear_proyecto, name='crear_proyecto'),

    path('activos/<int:proyecto_id>/', views.lista_activos, name='lista_activos'),
    path('activos/<int:proyecto_id>/nuevo/', views.crear_activo, name='crear_activo'),
    path('activos/editar/<int:activo_id>/', views.editar_activo, name='editar_activo'),
    path('activos/eliminar/<int:activo_id>/', views.eliminar_activo, name='eliminar_activo'),
    path('activos/<int:proyecto_id>/importar-shodan/', views.importar_activos_shodan, name='importar_activos_shodan'),


    path('riesgos/<int:proyecto_id>/', views.lista_riesgos, name='lista_riesgos'),
    path('riesgos/<int:proyecto_id>/nuevo/', views.crear_riesgo, name='crear_riesgo'),
    path('riesgos/<int:riesgo_id>/tratamiento/', views.tratamiento_riesgo, name='tratamiento_riesgo'),
    path('riesgos/<int:riesgo_id>/tratamiento/detalle/', views.detalle_tratamiento, name='detalle_tratamiento'),
    path('riesgos/<int:riesgo_id>/editar/', views.editar_riesgo, name='editar_riesgo'),
    path('proyectos/<int:proyecto_id>/reporte/', views.reporte_proyecto, name='reporte_proyecto'),
]
