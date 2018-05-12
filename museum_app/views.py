from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_vs

import defusedxml.ElementTree as ET
from museum_app.models import Museum

def load_museums(request):
    xmlFile = open('museo.xml', "r")
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    root.remove(root.find('infoDataset'))
    resp = ''
    for contenido in root:
        # print('\n', contenido.tag, '\n')
        for atributos in contenido:
            for atributo in atributos.findall('atributo'):
                nombre = atributo.get('nombre')
                # print(nombre)
                if nombre == "ID-ENTIDAD":
                    ID = atributo.text
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
                    for sub_atributo in atributo.findall('atributo'):
                        nombre = sub_atributo.get('nombre')
                        # print(nombre)
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
                    for sub_atributo in atributo.findall('atributo'):
                        nombre = sub_atributo.get('nombre')
                        # print(nombre)
                        if nombre == "TELEFONO":
                            tel = sub_atributo.text
                        elif nombre == "EMAIL":
                            email = sub_atributo.text

        Museum(id=ID, name=name, url=url, description=descr,
               address=dirr, district=distr, tel=tel,
               email=email).save()
        resp += ID +'<br>'+name +'<br>'+descr +'<br>'+acc +'<br>'+url +'<br>'+distr +'<br>'+dirr +'<br>'+tel +'<br>'+email+'<br><br>'
    return HttpResponse(resp)


def login_view(request):
    if request.user.is_authenticated():
        return ("<p>Hi," + request.user.username +
                " <a href=/logout>logout</a></p>")
    else:
        return ("<p>Not logged in: <a href=/login>login</a></p>")


def main_page(request):
    return render(request, 'main.html')


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
