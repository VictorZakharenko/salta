import requests 
import xml.etree.ElementTree as et
from lxml import etree
from flask import current_app
from bs4 import BeautifulSoup

def build_root():
	with current_app.open_resource('static/xtemplates/store2.xml', 'rb') as f:
		r = type('obj', (object,), {'content' : f.read()})
	# r = requests.get('https://www.atlasformen.ru/feeds/GlobalFeeds/GetResponse_12_ru-RU.xml')
	# current_app.logger.info(r.status_code)
	tree = et.ElementTree(etree.fromstring(r.content))
	root = tree.getroot()
	current_app.logger.info(root)	
	return root

def build_it(form_data):
	root = build_root()
	ready_dic = get_ready_dic(root, form_data)
	current_app.logger.info(ready_dic)
	html_dic = get_html_dic(ready_dic)
	return html_dic

def get_html_dic(ready_dic):
	with current_app.open_resource('static/xtemplates/xtemplate.html', 'rb') as f:
		xtemplate = f.read()

	soup = BeautifulSoup(xtemplate, 'html.parser')
	tables = iter(soup.find_all('table', {"class": "width296auto"}))
	for key, value in ready_dic.items():
		substitute_table_components(next(tables), value)
	ready_html = soup.find('table').getText
	all_a = soup.find('table').findAll('a')
	wrap_links(all_a)
	wrapped_html = str(soup)
	return {'plane_links_html' : str(soup.find('table')),\
			'wrapped_html' : wrapped_html}

def get_ready_dic(root, form_data):
	ready_dic = {}
	for data_key, group_id in form_data.items():
		if data_key[:-1] != 'group_id':
			continue
		current_app.logger.info('requests')
		search_group_output = root.findall(f".//offer/[@group_id='{group_id}']")
		if len(search_group_output) == 0:
			ready_dic[data_key] = {
				'name' : f'{group_id} НЕТ В ФИДЕ',
				'url' : '---',
				'picture' : 'https://image.freepik.com/free-vector/error-with-glitch-effect-screen-error-404-page-found_143407-1.jpg',
				'price' : '---',
				'old_price' : '---',
				'discount' : 0
			}
			current_app.logger.info(f'{group_id} НЕТ В ФИДЕ')
			current_app.logger.info('#####')
			continue
		target_el = search_group_output[0]
		name = target_el.find('name').text
		if len(name)>20:
			name = name[:17]+'...'
		url = target_el.find('url').text
		picture = target_el.find('picture').text
		price = target_el.find('price').text.split(' ')[0]
		old_price = target_el.find("param/[@name='oldprice']").text.split(' ')[0]
		opv = int(old_price.split('.')[0])
		cpv = int(price.split('.')[0])
		discount = -round(((opv-cpv)/opv)*100)
		ready_dic[data_key] = {
			'name' : name,
			'url' : url,
			'picture' : picture,
			'price' : price,
			'old_price' : old_price,
			'discount' : discount
		}
		# current_app.logger.info([name, url, picture, price, old_price, discount])
		current_app.logger.info('#####')
	return ready_dic

def substitute_table_components(table, value):
	tds = table.find_all('td')
	tds[0].clear()
	tds[0].append(f'\n\n{value["discount"]}%\n\n')
	'---'
	tds[1].a['href'] = value["url"]
	tds[1].a.img['alt'] = value["discount"]
	tds[1].a.img['src'] = value["picture"]
	'---'
	tds[2].img['alt'] = f'{value["discount"]}%'
	'---'
	tds[3].img['alt'] = f'{value["discount"]}%'
	'---'
	td4_rows = tds[4].table.tbody.find_all('tr')
	td4_rows[0].td.a['href'] = f'{value["url"]}'
	td4_rows[0].td.a.clear()
	td4_rows[0].td.a.append(f'{value["name"]}')

	td4_tr3_tds = td4_rows[3].find_all('td')
	td4_tr3_tds[0].a['href'] = value["url"]
	td4_tr3_tds[0].a.clear()
	td4_tr3_tds[0].a.append(value["price"])

	td4_rows[5].td.a['href'] = value["url"]
	td4_rows[5].td.a.clear()
	td4_rows[5].td.a.append(value["old_price"])

def wrap_links(soup_html):
	for a in soup_html :
		a['href'] = "{{LINK `"+f"{a['href']}" + '`}}'

