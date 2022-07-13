from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import PerfilUsuario, Producto, Carrito, Boleta, DetalleBoleta
from .forms import RegistrarForm, ProductoForm, PerfilForm, UsuarioForm

#API importaciones
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
# Create your views here.
def inicio(request):
    productos = Producto.objects.all()
    return render(request, 'usuarios/index.html', {'productos': productos})

def oferta_especial(request):
    return render(request, 'usuarios/promocion.html')

def producto_detalle(request, idp):
    producto = Producto.objects.get(idProducto = idp)
    return render(request, 'usuarios/producto.html', {'producto': producto})

def logearse(request):
    if request.user.is_authenticated:
        return redirect(inicio)
    if(request.method == 'POST'):
        usname = request.POST.get("usuario")
        contrasena = request.POST.get("contrasena")
        user = authenticate(username=usname, password=contrasena)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(inicio)
    return render(request, 'usuarios/logearse.html')

def registro(request):
    if request.user.is_authenticated:
        return redirect(inicio)
    if request.method == 'POST':
        form = RegistrarForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            direccion = request.POST.get("direccion")
            imagenUsuario = request.POST.get("fotoperfil")
            suscripcion = request.POST.get("consubscripcion")
            if(suscripcion == 'on'):
                sub = 'Si'
            else:
                sub = 'No'
            PerfilUsuario.objects.update_or_create(user=user, rut=rut, direccion=direccion, esSubscriptor=sub, imagenUs=imagenUsuario)
            return redirect(logearse)
    form = RegistrarForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def salir(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(inicio)

def nosotros(request):
    return render(request, 'usuarios/nosotros.html')

def admin(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    return render(request, 'administrador/index.html')

def admin_productos(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    productos = Producto.objects.all()
    form = ProductoForm(request.POST or None, request.FILES or None)
    if(request.method == 'POST'):
        try:
            Producto.objects.create(categoria=request.POST.get("Categoria"), 
            nombreProducto=request.POST.get("nombreProducto"), 
            precio=request.POST.get("precio"), 
            porcSub=request.POST.get("porcSub"), 
            porcOferta = request.POST.get("porcOferta"), 
            descripcion=request.POST.get("descripcion"), 
            imagenProducto=request.POST.get("imagenProducto"))
        except:
            return redirect(admin_productos)
    return render(request, 'administrador/adminProductos.html', {'productos': productos, 'form': form})

def editar_producto(request, idp):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    productos = Producto.objects.all()
    producto = Producto.objects.get(idProducto=idp)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if(request.method == 'POST'):
        form.save()
        Producto.objects.filter(idProducto=idp).update(categoria=request.POST.get("Categoria"))
        return redirect(admin_productos)
    return render(request, 'administrador/adminProductosEditar.html', {'productos': productos, 'form': form, 'producto': producto})

def eliminar_producto(request, idp):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    Producto.objects.get(idProducto=idp).delete()
    return redirect(admin_productos)

def admin_usuarios(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    if request.method == 'POST':
        form = RegistrarForm(request.POST)
        if form.is_valid():
            user = form.save()
            idu = user.id
            rut = request.POST.get("rut")
            direccion = request.POST.get("direccion")
            imagenUsuario = request.POST.get("fotoperfil")
            suscripcion = request.POST.get("consubscripcion")
            administrador = request.POST.get("staff")
            if(administrador == 'on'):
                staff = True
            else:
                staff = False
            if(suscripcion == 'on'):
                sub = 'Si'
            else:
                sub = 'No'
            PerfilUsuario.objects.update_or_create(user=user, rut=rut, direccion=direccion, esSubscriptor=sub, imagenUs=imagenUsuario)
            User.objects.filter(id=idu).update(is_staff = staff)
            return redirect(admin_usuarios)
    form = RegistrarForm()
    usuarios = PerfilUsuario.objects.all()
    return render(request, 'administrador/adminUsuarios.html', {'form': form , 'usuarios': usuarios})

def admin_usuarios_editar(request, idu):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    pUsuario = PerfilUsuario.objects.get(user_id=idu)
    formPerfil = PerfilForm(request.POST or None, request.FILES or None, instance=pUsuario)
    dataUsuario = User.objects.get(id=idu)
    formUser = UsuarioForm(request.POST or None, request.FILES or None, instance=dataUsuario)
    usuarios = PerfilUsuario.objects.all()
    esSub = pUsuario.esSubscriptor
    staff = dataUsuario.is_staff
    if request.method == 'POST':
        rutUsuario = request.POST.get("rut")
        direccionUsuario = request.POST.get("direccion")
        imagenUsuario = request.POST.get("fotoperfil")
        esSubUsuario = request.POST.get("consubscripcion")
        if(esSubUsuario == 'on'):
            esSub = 'Si'
        else:
            esSub = 'No'

        usuarioUsername = request.POST.get("username")
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        usuarioEmail = request.POST.get("email")
        rolUsuario = request.POST.get("staff")
        esStaff = False
        if(rolUsuario == 'on'):
            esStaff = True

        PerfilUsuario.objects.filter(id=idu).update(
            rut=rutUsuario, 
            direccion=direccionUsuario, 
            imagenUs=imagenUsuario, 
            esSubscriptor =esSub
        )

        User.objects.filter(id=idu).update(
            username=usuarioUsername,
            first_name=firstName,
            last_name=lastName,
            email=usuarioEmail,
            is_staff=esStaff
        )
        return redirect(admin_usuarios)
    return render(request, 'administrador/adminUsuariosEditar.html', 
    {'formPerfil': formPerfil, 'formUser': formUser, 'esSub': esSub, 'staff': staff, 'pUsuario': pUsuario, 'usuarios': usuarios})

def eliminar_usuario(request, idu):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    PerfilUsuario.objects.get(user=idu).delete()
    User.objects.get(id=idu).delete()
    return redirect(admin_usuarios)

def carro(request):
    if not request.user.is_authenticated:
        return redirect(inicio)
    try:
        us = PerfilUsuario.objects.get(id=request.user.id)
        carrito = Carrito.objects.filter(cliente = us)
        carro = []
        desctoSub = 0
        subtotal = 0
        total = 0
        if(carrito[0].cliente.esSubscriptor == 'Si'):
            desctoSub = 0.05
        for prod in carrito:
            montoReajustado = round(prod.idproducto.precio * (1 - ( desctoSub + ( prod.idproducto.porcOferta/100 ) )))
            subtotal += prod.idproducto.precio
            total += montoReajustado
            carro.append({
                'categoria': prod.idproducto.categoria, 
                'nombreProducto': prod.idproducto.nombreProducto, 
                'precio': prod.idproducto.precio, 
                'desSub': 5,
                'descOferta': prod.idproducto.porcOferta,
                'reajuste':montoReajustado,
                'id': prod.idc
            })
        return render(request, 'usuarios/carro.html', {'montos': carro, 'total': total, 'subtotal': subtotal})
    except:
        return render(request, 'usuarios/carro.html')

def agregar_carro(request, idp):
    if not request.user.is_authenticated:
        return redirect(inicio)
    try:
        us = PerfilUsuario.objects.get(id=request.user.id)
        pro = Producto.objects.get(idProducto=idp)
        Carrito.objects.create(cliente=us, idproducto=pro)
    except:
        return redirect(inicio)
    return redirect(inicio)

def borrar_carro(request, id):
    if not request.user.is_authenticated:
        return redirect(inicio)
    Carrito.objects.filter(idc=id).delete()
    return redirect(carro)

def pagar(request):
    if not request.user.is_authenticated:
        return redirect(inicio)
    us = PerfilUsuario.objects.get(id=request.user.id)
    carrito = Carrito.objects.filter(cliente = us)
    d = {}
    for c in carrito:
        if(c.idproducto.idProducto not in d):
            d[c.idproducto.idProducto] = 1
        else:
            d[c.idproducto.idProducto] = d[c.idproducto.idProducto] + 1
    for cr in d:
        if(d[cr] > Producto.objects.get(idProducto = cr).cantidad):
            return redirect(carro)
    for cr in d:
        Producto.objects.filter(idProducto = cr).update(cantidad = (Producto.objects.get(idProducto = cr).cantidad - d[cr]))

    subTotal = 0
    total = 0
    desctoSub = 0
    dsub = 0
    if(carrito[0].cliente.esSubscriptor == 'Si'):
        desctoSub = 0.05
        dsub = 5
    for prod in carrito:
        montoReajustado = round(prod.idproducto.precio * (1 - ( desctoSub + ( prod.idproducto.porcOferta/100 ) )))
        total += montoReajustado
        subTotal += prod.idproducto.precio
    Boleta.objects.create(cliente=us, monto=total, estadoActual='En Bodega')

    boletas = Boleta.objects.filter(cliente=us)
    menor = -1
    for b in boletas:
        if(b.idBoleta > menor):
            menor = b.idBoleta
    
    boleta = Boleta.objects.get(idBoleta=menor)
    for detb in carrito:
        stotal = detb.idproducto.precio
        total = round(detb.idproducto.precio * (1 - ( desctoSub + ( detb.idproducto.porcOferta/100 ) )))
        DetalleBoleta.objects.create(idBole=boleta, idproducto=detb.idproducto, porcSub=dsub, porcOferta=detb.idproducto.porcOferta, subTotal=stotal, total=total)
    
    Carrito.objects.filter(cliente = us).delete()
    return redirect(carro)

def admin_ventas(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    boletas = Boleta.objects.all()
    return render(request, 'administrador/adminVentas.html', {'boletas': boletas})

def despachar(request, idb):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    Boleta.objects.filter(idBoleta=idb).update(estadoActual = 'Despachado')
    return redirect(admin_ventas)

def entregar(request, idb):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    Boleta.objects.filter(idBoleta=idb).update(estadoActual = 'Entregado')
    return redirect(admin_ventas)

def admin_venta(request, idb):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    deboleta = DetalleBoleta.objects.filter(idBole=Boleta.objects.get(idBoleta=idb))
    infoBoleta = Boleta.objects.get(idBoleta=idb)
    return render(request, 'administrador/adminVenta.html', {'boleta': deboleta, 'infoBoleta': infoBoleta})

def mis_compras(request):
    if not request.user.is_authenticated:
        return redirect(inicio)
    boletas = Boleta.objects.filter(cliente=PerfilUsuario.objects.get(id=request.user.id))
    return render(request, 'usuarios/misCompras.html', {'boletas': boletas})

def mi_compra(request, idb):
    if not request.user.is_authenticated:
        return redirect(inicio)
    deboleta = DetalleBoleta.objects.filter(idBole=Boleta.objects.get(idBoleta=idb))
    infoBoleta = Boleta.objects.get(idBoleta=idb)
    return render(request, 'usuarios/miCompra.html', {'boleta': deboleta, 'infoBoleta': infoBoleta})

def mi_perfil(request):
    if not request.user.is_authenticated:
        return redirect(inicio)
    idu = request.user.id
    pUsuario = PerfilUsuario.objects.get(user_id=idu)
    formPerfil = PerfilForm(request.POST or None, request.FILES or None, instance=pUsuario)
    dataUsuario = User.objects.get(id=idu)
    formUser = UsuarioForm(request.POST or None, request.FILES or None, instance=dataUsuario)
    esSub = pUsuario.esSubscriptor
    if request.method == 'POST':
        rutUsuario = request.POST.get("rut")
        direccionUsuario = request.POST.get("direccion")
        imagenUsuario = request.POST.get("fotoperfil")
        esSubUsuario = request.POST.get("consubscripcion")
        if(esSubUsuario == 'on'):
            esSub = 'Si'
        else:
            esSub = 'No'

        usuarioUsername = request.POST.get("username")
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        usuarioEmail = request.POST.get("email")
        rolUsuario = request.POST.get("staff")
        esStaff = False
        if(rolUsuario == 'on'):
            esStaff = True

        PerfilUsuario.objects.filter(id=idu).update(
            rut=rutUsuario, 
            direccion=direccionUsuario, 
            imagenUs=imagenUsuario, 
            esSubscriptor =esSub
        )

        User.objects.filter(id=idu).update(
            username=usuarioUsername,
            first_name=firstName,
            last_name=lastName,
            email=usuarioEmail,
            is_staff=esStaff
        )
        return redirect(mi_perfil)
    return render(request, 'usuarios/perfil.html', 
    {'formPerfil': formPerfil, 'formUser': formUser, 'esSub': esSub, 'pUsuario': pUsuario})

def admin_bodega(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    if request.method == 'POST':
        producto = int(request.POST.get("producto"))
        cantidad = int(request.POST.get("Cantidad"))
        accion = request.POST.get("accion")
        if(accion == "+"):
            Producto.objects.filter(idProducto = producto).update(cantidad = (Producto.objects.get(idProducto = producto).cantidad) + cantidad)
        else:
            if(Producto.objects.get(idProducto = producto).cantidad  < cantidad):
                 Producto.objects.filter(idProducto = producto).update(cantidad =0)
            else:
                Producto.objects.filter(idProducto = producto).update(cantidad = (Producto.objects.get(idProducto = producto).cantidad) - cantidad)
    return render(request, 'administrador/adminBodega.html', {'productos': Producto.objects.all()})

###API ET###
class SubscriptoresAPI(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, idu = 0):
        resultado = {'respuesta': 'No se pudo encontrar el usuario...'}
        if(idu > 0):
            usuarios = list(PerfilUsuario.objects.filter(id=idu).values())
            if(len(usuarios) > 0):
                resultado = usuarios[0]
        else:
            usuarios = list(PerfilUsuario.objects.values())
            resultado = {'respuesta': 'Ok', 'usuarios': usuarios}
        return JsonResponse(resultado)

    def put(self, request, idu):
        resultado = {'respuesta': 'No se pudo encontrar el usuario...'}
        jd = json.loads(request.body)
        usuarios = list(PerfilUsuario.objects.filter(id=idu).values())
        if(len(usuarios) > 0):
            usuario = PerfilUsuario.objects.get(id = idu)
            usuario.esSubscriptor = jd["esSubscriptor"]
            usuario.save()
            resultado = {'respuesta': 'Ok'}
        return JsonResponse(resultado)

def poblar_db(request):
    Producto.objects.create(categoria="Perros", nombreProducto="Saco de alimento Royal Canin", precio=8000, porcSub=5, porcOferta = 0, descripcion="Saco alimento para perros de alta calidad.", imagenProducto="https://cdn.royalcanin-weshare-online.io/-GkXtGsBG95Xk-RB-Ptr/v4/ar-l-producto-maxi-puppy-pouch-size-health-nutrition-humedo")
    Producto.objects.create(categoria="Gatos", nombreProducto='Leonardo Quality Selection Kitten', precio=37900, porcSub=5, porcOferta= 0, descripcion= "Alimento húmedo completo para gatitos.", imagenProducto="https://http2.mlstatic.com/D_NQ_NP_763510-MLA48462210776_122021-O.webp")
    Producto.objects.create(categoria="Perros", nombreProducto='Desparasitante Bravecto', precio=41592, porcSub=5, porcOferta= 0, descripcion= "Comprimido masticable contra pulgas y garrapatas en perros.", imagenProducto="https://www.amigales.cl/pub/media/catalog/product/cache/c687aa7517cf01e65c009f6943c2b1e9/a/n/antiparasitario_bravecto_perros_01.jpg")
    Producto.objects.create(categoria="Gatos", nombreProducto='Saco de alimento don Cuchito', precio=3000, porcSub=5, porcOferta= 0, descripcion= "Alimento para gatos don cuchito (Saco).", imagenProducto="https://mascotaslosandes.cl/562-home_default/don-cucho-20kg.jpg")
    return redirect(inicio)