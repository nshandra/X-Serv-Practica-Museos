from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from museum_app.forms import Comment_Form, CSS_Form, Title_Form
from museum_app.models import Museum, Collection, Added_Museum
from django.db.models import Count


def load_museums_xml():
    import defusedxml.ElementTree as ET
    xmlFile = open('201132-0-museos.xml', "r")
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    # DESCARTA infoDataset
    root.remove(root.find('infoDataset'))
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
                    descr = atributo.text + ' '
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
                            dirr2 = sub_atributo.text
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


def load_museums_json():
    import json
    jsonFile = open('201132-0-museos.json', "r")
    jdict = json.load(jsonFile)

    for item in jdict['@graph']:
        distr = item['address']['district']['@id'].split('/')[-1]
        dirr = (item['address']['street-address'] + ', ' +
                item['address']['postal-code'] + ', ' +
                item['address']['locality'])
        descr = (item['organization']['organization-desc'] + ', ' +
                 item['organization']['schedule'])
        if item['organization']['accesibility'] == '1':
            acc = True
        else:
            acc = False
        Museum(id=item['id'], name=item['title'], url=item['relation'],
               description=descr, access=acc, address=dirr,
               district=distr).save()


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
            refresh = request.POST.get('refresh')
            if refresh == 'xml':
                print('REFRESH XML')
                load_museums_xml()
            elif refresh == 'json':
                print('REFRESH JSON')
                load_museums_json()
        return response
    else:
        return HttpResponseNotFound()


def museum(request, ID):
    print(ID)
    if request.method == "GET":
        m = Museum.objects.get(id=ID)
        f = Comment_Form()
        context = {'Museum': m, 'Form': f}
        return render(request, 'museo.html', context)
    elif request.method == "POST":
        m = Museum.objects.get(id=ID)
        if request.POST.get('text'):
            f = Comment_Form(request.POST)
            coment = f.save()
            m.coment.add(coment)
            m.save()
        elif request.POST.get('add'):
            # if request.user.username != 'root':
            c = Collection.objects.get(user=request.user.username)
            # idempotent
            if not Added_Museum.objects.filter(museum=m, collection=c):
                added_museum = Added_Museum(museum=m, collection=c).save()
        elif request.POST.get('vote'):
            if request.user.is_authenticated():
                if not request.session.get('has_voted_%s' % ID, False):
                    m = Museum.objects.get(id=ID)
                    m.vote += 1
                    m.save()
                    request.session['has_voted_%s' % ID] = True

        return HttpResponseRedirect(request.path)
    else:
        return HttpResponseNotFound()


def load_custom_CSS(request):
    print('load_custom_CSS')
    if request.user.is_authenticated():
        user = request.user.username
        print(user)
        try:
            csssheet = Collection.objects.get(user=user)
        except ObjectDoesNotExist:
            print("Either the entry or blog doesn't exist.")
        context = {'CSS': csssheet}
        return render(request, 'custom.css', context, content_type="text/css")
    else:
        return HttpResponse('')


def user(request, user_name):
    from django.core.paginator import Paginator

    if request.method == "GET":
        c = get_object_or_404(Collection, user=user_name)
        am = Added_Museum.objects.filter(collection=c)
        page = request.GET.get('page', 1)

        paginator = Paginator(am, 5)
        try:
            am2 = paginator.page(page)
        except PageNotAnInteger:
            am2 = paginator.page(1)
        except EmptyPage:
            am2 = paginator.page(paginator.num_pages)

        f = CSS_Form(instance=c)
        f2 = Title_Form(instance=c)
        context = {'Collection': c, 'Added_Museums': am2,
                   'CSS_Form': f, 'Title_Form': f2}
        return render(request, 'usuario.html', context)
    elif request.method == "POST":
        c = Collection.objects.get(user=user_name)
        if 'css_page' in request.POST:
            f = CSS_Form(request.POST, instance=c)
            print(f)
            if f.is_valid():
                f.save()
        elif request.POST.get('title'):
            f = Title_Form(request.POST, instance=c)
            if f.is_valid():
                f.save()
        else:
            return HttpResponseNotFound()
        return HttpResponseRedirect(request.path)
    else:
        return HttpResponseNotFound()


def user_xml(request, user_name):
    # from django.core import serializers
    if request.method == "GET":
        c = Collection.objects.get(user=user_name)
        am = Added_Museum.objects.filter(collection=c)
        m = []
        for entry in am:
            print(entry.museum)
            m.append(entry.museum)
        # data = serializers.serialize("xml", m, exclude=('coment'))
        context = {'Collection': c, 'Museum_list': m}
        data = render(request, 'Collection_to_xml.xml', context)
        response = HttpResponse(data, content_type='text/xml')
        cd = 'attachment; filename="%s.xml"' % user_name
        response['Content-Disposition'] = cd
        return response
    else:
        return HttpResponseNotFound()


def user_json(request, user_name):
    if request.method == "GET":
        c = Collection.objects.get(user=user_name)
        am = Added_Museum.objects.filter(collection=c)
        m = []
        for entry in am:
            print(entry.museum)
            m.append(entry.museum)
        context = {'Collection': c, 'Museum_list': m}
        data = render(request, 'Collection_to_json.json', context)
        response = HttpResponse(data, content_type='text/json')
        cd = 'attachment; filename="%s.json"' % user_name
        response['Content-Disposition'] = cd
        return response
    else:
        return HttpResponseNotFound()


def sign_up(request):
    if request.method == "GET":
        f = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': f})
    elif request.method == "POST":
        f = UserCreationForm(request.POST)
        ban_list = ['museos', 'xml', 'json', 'set_language',
                    'lastcomments', 'topmuseums', 'logout',
                    'login', 'signup', 'custom.css', 'admin']
        u = request.POST.get('username')
        print(u)
        if u not in ban_list:
            if f.is_valid():
                f.save()
                Collection(user=f.cleaned_data['username']).save()
                messages.success(request, 'Account created successfully')
            return HttpResponseRedirect('signup')
        else:
            w = 'Username already exist and/or passwords don\'t match up'
            messages.warning(request, w)
            return HttpResponseRedirect('signup')
    else:
        return HttpResponseNotFound()


def main_xml(request):
    if request.method == "GET":
        m = Museum.objects.exclude(coment__isnull=True)\
            .annotate(num_coment=Count('coment'))\
            .order_by('num_coment')
        u = Collection.objects.all()
        context = {'Museum_list': m, 'User_list': u}
        data = render(request, 'main_to_xml.xml', context)
        response = HttpResponse(data, content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename="main.xml"'
        return response
    else:
        return HttpResponseNotFound()


def main_json(request):
    if request.method == "GET":
        m = Museum.objects.exclude(coment__isnull=True)\
            .annotate(num_coment=Count('coment'))\
            .order_by('num_coment')
        u = Collection.objects.all()
        context = {'Museum_list': m, 'User_list': u}
        data = render(request, 'main_to_json.json', context)
        response = HttpResponse(data, content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename="main.json"'
        return response
    else:
        return HttpResponseNotFound()


def set_language(request):
    from django.utils import translation
    if request.method == "POST":
        if request.POST.get('language'):
            user_language = request.POST.get('language')
            translation.activate(user_language)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return HttpResponseRedirect(request.POST.get('next'))
    else:
        return HttpResponseNotFound()


def main_page(request):
    if request.method == "GET":
        # museos
        m = Museum.objects.exclude(coment__isnull=True)\
            .annotate(num_coment=Count('coment'))\
            .order_by('-num_coment')[:5]
        # Usuarios
        u = Collection.objects.all()
        context = {'Museum_list': m, 'User_list': u}
        return render(request, 'main.html', context)
    else:
        return HttpResponseNotFound()
