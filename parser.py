#!/usr/bin/python3
# xml.etree.ElementTree
import defusedxml.ElementTree as ET
import sys

xmlFile = open(sys.argv[1], "r")

tree = ET.parse(xmlFile)
root = tree.getroot()

root.remove(root.find('infoDataset'))

for contenido in root:
	print('\n', contenido.tag, '\n')
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

	print(ID)
	print(name)
	print(descr)
	print(acc)
	print(url)
	print(url)
	print(dirr)
	print(tel)
	print(email)

# from bs4 import BeautifulSoup
# soup = BeautifulSoup(xmlFile, 'xml')
# print(soup.prettify())
# print(soup.Contenidos.next_element)
# print(soup.Contenidos.next_element.next_element)

# cont = soup.Contenidos.contenido.extract()
# print(cont("atributo"))
# print(cont.prettify(formatter='xml'))
# soup.Contenidos.infoDataset.decompose()

# for cont in soup.Contenidos.contents:
# cont = soup.Contenidos.contenido.atributos.extract()

# for child in soup.Contenidos.children:
# 	cont = child
# 	for child2 in cont.children:
# 		print('QWER')
# 		print(child2)

# print(cont.children[0])

# print(cont.atributo)
# print(cont.next_element.next_element)
# print(cont.next_element.next_element.next_element)
# for element in cont.next_elements:
#     print(element)