from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Producto(models.Model):
    idProducto = models.IntegerField(primary_key=True, verbose_name="ID de producto")
    nombreProducto = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre del producto")
    categoria = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre Categoría")
    descripcion = models.CharField(max_length=300, blank=False, null=False, verbose_name="Descripción del producto")
    precio = models.IntegerField(blank=False, null=False, verbose_name="Precio")
    porcSub = models.IntegerField(blank=False, null=False, verbose_name="Descuento Subscriptor")
    porcOferta = models.IntegerField(blank=False, null=False, verbose_name="Descuento Oferta")
    imagenProducto = models.CharField(max_length=300, blank=False, null=False, verbose_name="Imágen Producto")
    cantidad = models.IntegerField(blank=False, null=False, verbose_name="Cantidad", default=1)

    def __str__(self):
        return f"{self.nomProducto} - {self.precio}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=80, blank=True, null=True, verbose_name="Rut")
    direccion = models.CharField(max_length=80, blank=True, null=True, verbose_name="Dirección")
    imagenUs = models.CharField(max_length=300, blank=True, null=True, verbose_name="Imágen Usuario")
    esSubscriptor = models.CharField(max_length=2, blank=True, null=True, verbose_name="Es Suscriptor")

    def __str__(self):
        return f"{self.user.username} - ({self.user.email})"

class Carrito(models.Model):
    idc = models.IntegerField(primary_key=True, verbose_name="Id carro")
    cliente = models.ForeignKey(PerfilUsuario, on_delete=models.DO_NOTHING)
    idproducto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    def __str__(self):
        return f"{self.idProducto}"

class Boleta(models.Model):
    idBoleta = models.IntegerField(primary_key=True, verbose_name="Id Compra")
    cliente = models.ForeignKey(PerfilUsuario, on_delete=models.DO_NOTHING)
    monto = models.IntegerField(blank=False, null=False, verbose_name="Total pagado")    
    fecha = models.DateTimeField(auto_now=True, verbose_name="Fecha")
    estadoActual = models.CharField(max_length=100, blank=True, null=True, verbose_name="Estado actual")

class DetalleBoleta(models.Model):
    idd = models.IntegerField(primary_key=True, verbose_name="Id detalle")
    idBole = models.ForeignKey(Boleta, on_delete=models.DO_NOTHING)
    idproducto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    porcSub = models.IntegerField(blank=False, null=False, verbose_name="Descuento Subscriptor")
    porcOferta = models.IntegerField(blank=False, null=False, verbose_name="Descuento Oferta")
    subTotal = models.IntegerField(blank=False, null=False, verbose_name="subTotal")
    total = models.IntegerField(blank=False, null=False, verbose_name="Total")