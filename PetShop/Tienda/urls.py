from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('oferta_especial', views.oferta_especial, name="oferta_especial"),
    path('registrarse', views.registro, name="registrarse"),
    path('login', views.logearse, name="login"),
    path('producto/<idp>', views.producto_detalle, name="producto"),
    path('salir', views.salir, name="salir"),
    path('nosotros', views.nosotros, name="nosotros"),
    path('administrar', views.admin, name="administrar"),
    path('admin_productos', views.admin_productos, name="admin_productos"),
    path('editar_producto/<idp>', views.editar_producto, name="editar_producto"),
    path('eliminar_producto/<idp>', views.eliminar_producto, name="eliminar_producto"),
    path('admin_usuarios', views.admin_usuarios, name="admin_usuarios"),
    path('editar_usuario/<idu>', views.admin_usuarios_editar, name="editar_usuario"),
    path('eliminar_usuario/<idu>', views.eliminar_usuario, name="eliminar_usuario"),
    path('carro', views.carro, name="carro"),
    path('agregar_carro/<idp>', views.agregar_carro, name="agregar_carro"),
    path('borrar_carro/<id>', views.borrar_carro, name="borrar_carro"),
    path('pagar', views.pagar, name="pagar"),
    path('admin_ventas', views.admin_ventas, name="admin_ventas"),
    path('despachar/<idb>', views.despachar, name="despachar"),
    path('entregar/<idb>', views.entregar, name="entregar"),
    path('admin_venta/<idb>', views.admin_venta, name="admin_venta"),
    path('mis_compras', views.mis_compras, name="mis_compras"),
    path('mi_compra/<idb>', views.mi_compra, name="mi_compra"),
    path('mi_perfil', views.mi_perfil, name="mi_perfil"),
    path('admin_bodega', views.admin_bodega, name="admin_bodega"),
    path('api/subscriptores', views.SubscriptoresAPI.as_view(), name="subscriptores"),
    path('api/subscriptores/<int:idu>', views.SubscriptoresAPI.as_view(), name="subscriptores_listada"),
    path("poblar_db", views.poblar_db, name="poblar_db")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)