from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Cliente, DocumentoAgente
from .forms import ContactForm
from django.http import HttpResponseRedirect
from django.db.models import Q
# Create your views here.


class SignInView(LoginView):
    pass

@login_required
def render_tablas(request):
    """Vista para listar y resetear tablas"""
    if request.method == 'GET':
        queryset_clts = Cliente.objects.all()
        documento_rel_list = DocumentoAgente.objects.all()
        return render(request, 'dash/tablas.html',
                      {'clientes': queryset_clts,
                       'agente_cliente_list': documento_rel_list})

    if request.method == 'POST':
        Cliente.objects.all().update(resultado=None, agente=None)
        DocumentoAgente.objects.all().delete()
        return HttpResponseRedirect('/tablas/')

@login_required
def dashboard(request):
    """Vista de ficha."""
    if request.method == 'GET':
        # una vez logueado, cargo los clientes
        current_user = request.user
        nombre_usuario = current_user.username
        # verifico si no tengo algun documento precargado
        # con mi id agente
        if not DocumentoAgente.objects.filter(agente=current_user):
            clientes = Cliente.objects.filter(agente=None).order_by('id')[:1]
        else:
            docu = DocumentoAgente.objects.get(agente=current_user)
            clientes = Cliente.objects.filter(documento=docu.documento, resultado=None)
            # si existen
            if clientes:
                clientes = clientes.order_by('id')[:1]
            else:
                clientes = Cliente.objects.filter(agente=None).order_by('id')[:1]
                DocumentoAgente.objects.filter(agente=current_user).delete()

        form = ContactForm()
        if not clientes:
            return render(request, 'dash/culminated.html')
        else:
            cliente_obj = clientes.get()
            documento = cliente_obj.documento
            nombres = cliente_obj.nombres
            telefono = cliente_obj.telefono
            Cliente.objects.filter(documento=documento).update(agente=current_user)
            if not DocumentoAgente.objects.filter(agente=current_user):
                doc = DocumentoAgente(agente=current_user, documento=documento)
                doc.save()


            return render(request, 'dash/ficha.html',
                          {'documento': documento,
                           'nombres': nombres,
                           'telefono': telefono,
                           'cliente': cliente_obj.id,
                           'user': nombre_usuario,
                           'form': form})



    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        cliente = request.POST['cliente']
        tipo_contacto = request.POST['tipo_contacto']

        cliente = Cliente.objects.get(pk=cliente)
        cliente.resultado = tipo_contacto
        cliente.save()
        if tipo_contacto == 'cd':
            Cliente.objects.filter(documento=cliente.documento, resultado=None).update(resultado='X')

        return HttpResponseRedirect('/dashboard/')
