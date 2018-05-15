from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_vs

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from museum_app.forms import Comment_Form

# import defusedxml.ElementTree as ET
import xml.etree.ElementTree as ET
from museum_app.models import Museum, Collection
from django.db.models import Count


def load_museums():
    xmlFile = open('201132-0-museos.xml', "r")
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    # DESCARTA infoDataset 
    root.remove(root.find('infoDataset'))
    # resp = ''
    # ITERA SOBRE EL XML
    for contenido in root:
        for atributos in contenido:
            # ITERA SOBRE LOS ATRIBUTOS DEL MUSEO
            for atributo in atributos.findall('atributo'):
                nombre = atributo.get('nombre')
                if nombre == "ID-ENTIDAD":
                    id = atributo.text
                elif nombre == "NOMBRE":
                    name = atributo.text
                elif nombre == "DESCRIPCION-ENTIDAD":
                    descr = atributo.text
                elif nombre == "HORARIO":
                    descr += atributo.text
                elif nombre == "ACCESIBILIDAD":
                    acc = atributo.text
                elif nombre == "CONTENT-URL":
                    url = atributo.text
                elif nombre == "LOCALIZACION":
                    # ITERA SOBRE LOS ATRIBUTOS DE LOCALIZACION
                    for sub_atributo in atributo.findall('atributo'):
                        nombre = sub_atributo.get('nombre')
                        if nombre == "CLASE-VIAL":
                            dirr0 = sub_atributo.text + ' '
                        elif nombre == "NOMBRE-VIA":
                            dirr1 = sub_atributo.text + ', '
                        elif nombre == "NUM":
                            dirr1 += sub_atributo.text + ', '
                        elif nombre == "LOCALIDAD":
                            dirr2 = sub_atributo.text + ', '
                        elif nombre == "PROVINCIA":
                            dirr2 += sub_atributo.text
                        elif nombre == "CODIGO-POSTAL":
                            pcode = sub_atributo.text + ', '
                        elif nombre == "DISTRITO":
                            distr = sub_atributo.text
                    dirr = dirr0 + dirr1 + pcode + dirr2
                elif nombre == "DATOSCONTACTOS":
                    # ITERA SOBRE LOS ATRIBUTOS DE DATOSCONTACTOS
                    for sub_atributo in atributo.findall('atributo'):
                        nombre = sub_atributo.get('nombre')
                        if nombre == "TELEFONO":
                            tel = sub_atributo.text
                        elif nombre == "EMAIL":
                            email = sub_atributo.text
        if acc == '1':
            access = True
        else:
            access = False

        Museum(id=id, name=name, url=url, description=descr,
               access=access, address=dirr, district=distr,
               tel=tel, email=email).save()
        # resp += ID +'<br>'+name +'<br>'+descr +'<br>'+acc +'<br>'+url +'<br>'+distr +'<br>'+dirr +'<br>'+tel +'<br>'+email+'<br><br>'
    # return HttpResponse('Job done')

def museums_lists(filter_key):
    if filter_key and filter_key != 'ALL':
        print('FILTER')
        m = Museum.objects.filter(district=filter_key)
    else:
        m = Museum.objects.all()
    d = Museum.objects.values_list('district', flat=True).distinct()
    return {'Museum_list': m, 'District_list': d}


def museums(request):
    filter_key = ''
    if request.method == "GET":
        if 'filter' in request.COOKIES:
            filter_key = request.COOKIES['filter']
        context = museums_lists(filter_key)
        return render(request, 'museos.html', context)
    elif request.method == "POST":
        response = HttpResponseRedirect('museos')
        if request.POST.get('district'):
            response.set_cookie('filter', request.POST.get('district'))
        elif request.POST.get('refresh'):
            print('REFRESH')
            load_museums()
        return response
    else:
        return HttpResponseNotFound()


def museum(request, ID):
    print(ID)
    if request.method == "GET":
        m = Museum.objects.filter(id=ID)
        f = Comment_Form()
        context = {'Museum': m, 'Form': f}
        return render(request, 'museo.html', context)
    elif request.method == "POST":
        if request.POST.get('text'):
            m = Museum.objects.get(id=ID)
            # m.coment.add(request.POST.get('coment'))
            f = Comment_Form(request.POST)
            # f.save(commit=False)
            comm = f.save()
            m.coment.add(comm)
            m.save()

            # Create a form instance with POST data.
            # f = AuthorForm(request.POST)
            # Create, but don't save the new author instance.
            # new_comment = f.save(commit=False)
            # # Save the new instance.
            # new_comment.save()
            # # Now, save the many-to-many data for the form.
            # f.save_m2m()
        return HttpResponseRedirect(request.path)
    else:
        return HttpResponseNotFound()


def sign_up(request):
    if request.method == "GET":
        f = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': f})
    elif request.method == "POST":
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            Collection(user=f.cleaned_data['username']).save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect('signup')
        else:
            messages.warning(request, 'Username already exist and/or passwords don\'t match up')
            # print(f.cleaned_data['password1'])
            # print(f.cleaned_data['password2'])
            # if f.cleaned_data['password1'] !=  f.cleaned_data['password2']:
            #     messages.warning(request, 'Check password')
            # else:
            #     messages.warning(request, 'Username alredy exist')
            return HttpResponseRedirect('signup')
    else:
        return HttpResponseNotFound()


def main_page(request):
    if request.method == "GET":
        # museos
        m = Museum.objects.exclude(coment__isnull=True)\
        .annotate(num_coment=Count('coment'))\
        .order_by('num_coment')
        # Museum_list = {'Museum_list': m}
        # Usuarios
        u = Collection.objects.all()
        # User_list = {'User_list': u}
        context = {'Museum_list': m, 'User_list': u}
        print(m.count())
        return render(request, 'main.html', context)
    else:
        return HttpResponseNotFound()


# @csrf_exempt
# def get_page(request, req_name):
#     if request.method == "PUT":
#         if request.user.is_authenticated():
#             Pages(name=req_name, page=request.body).save()
#             return HttpResponse("Page submitted.<br><br><a href=/>Home</a>")
#         else:
#             return HttpResponseNotFound("<h1>Login to add pages. "
#                                         "<a href=/login>login</a></h1>")
#     else:
#         try:
#             req_page = login_view(request)
#             req_page += Pages.objects.get(name=req_name).page
#             if request.method == "GET":
#                 return HttpResponse(req_page)
#             else:
#                 return HttpResponseNotAllowed("['GET', 'PUT']",
#                                               "<h1>405 Not Allowed</h1>")
#         except Pages.DoesNotExist:
#                 return HttpResponseNotFound("<h1>Page does not exist.</h1>")


# def ann_main(request):
#     Pages_list = {'Pages_list': Pages.objects.all()}
#     return render(request, 'ann_main.html', Pages_list)


# def ann_get_page(request, req_name):
#     if request.method == "GET":
#         try:
#             content = {'content': Pages.objects.get(name=req_name)}
#             return render(request, 'page.html', content)
#         except Pages.DoesNotExist:
#                 return HttpResponseNotFound("<h1>Page does not exist.</h1>")
#     else:
#         return HttpResponseNotAllowed("['GET']", "<h1>405 Not Allowed</h1>")


# def edit_main(request):
#     Pages_list = {'Pages_list': Pages.objects.all()}
#     return render(request, 'edit_main.html', Pages_list)


# @csrf_exempt
# def edit_page(request, req_name):
#     print(request.user.is_authenticated())
#     if request.user.is_authenticated():
#         if request.method == "GET":
#             try:
#                 content = {'content': Pages.objects.get(name=req_name)}
#                 return render(request, 'edit.html', content)
#             except Pages.DoesNotExist:
#                 return HttpResponseNotFound("<h1>Page does not exist.</h1>")
#         elif request.method == "POST":
#             Pages(name=req_name, page=request.POST["page"]).save()
#             return HttpResponseRedirect('/edit/'+req_name)
#         else:
#             return HttpResponseNotAllowed("['GET', 'POST']",
#                                           "<h1>405 Not Allowed</h1>")
#     else:
#         return HttpResponseNotFound("<b>Login to edit pages. "
#                                     "<a href=/login>login</a></b>")
