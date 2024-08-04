from flask import Flask, request, jsonify
import requests

import xml.etree.ElementTree as ET


# TODO write test (pytest)
# TODO write type annotation (mypy)

def create_app():
    app = Flask(__name__)

    NDL_OPEN_SEARCH_ENDPOINT = 'https://ndlsearch.ndl.go.jp/api/opensearch'
    NDL_XML_NAMESPACE = {
        'dc': 'http://purl.org/dc/elements/1.1/',
        'dcterms': 'http://purl.org/dc/terms/',
        'dcndl': 'http://ndl.go.jp/dcndl/terms/'}

    @app.route('/', methods=['POST'])
    def search_book():
        request_json = request.get_json()
        title = request_json['title']

        payload = {'title': title}
        xml_text = fetch_xml_from_ndl_endpoint(payload)
        xml_obj = ET.fromstring(xml_text)
        items = get_items(xml_obj)
        if len(items) == 0:
            return jsonify({'message': 'No results match the submitted word'})
        books = organize_info(items)
        return jsonify({'result': books})

    def fetch_xml_from_ndl_endpoint(payload):
        try:
            xml_res = requests.get(NDL_OPEN_SEARCH_ENDPOINT, params=payload)
            xml_res.raise_for_status()
        except Exception as e:
            raise Exception(f'POST ERROR: {e}')
        return xml_res.text

    def get_items(xml_obj):
        items = xml_obj.findall('.//item')
        if items is None:
            return []
        filtered_items = list(filter(lambda item: (
            item.find('.//category') is not None
            and item.find('.//category').text == '図書'), items))
        return filtered_items

    def organize_info(items):
        books = []
        for item in items:
            book = {}
            title = find_with_namespace(item, './/dc:title')
            book['title'] = title.text if title is not None else ''
            creator = findall_with_namespace(item, './/dc:creator')
            book['creator'] = (
                list(map(lambda name: name.text, creator))
                if creator is not None else [])
            issued = find_with_namespace(item, './/dcterms:issued')
            book['issued'] = issued.text if issued is not None else ''
            price = find_with_namespace(item, './/dcndl:price')
            book['price'] = price.text if price is not None else ''
            edition = find_with_namespace(item, './/dcndl:edition')
            book['edition'] = edition.text if edition is not None else ''
            identifier = find_with_namespace(item, './/dc:identifier')
            if identifier is not None:
                identifier = identifier.text
                book['thumbnail'] = (
                    'https://ndlsearch.ndl.go.jp/thumbnail/'
                    '{"".join(identifier.split("-"))}.jpg')
            books.append(book)
        return books

    def find_with_namespace(xml_obj, element, namespace=NDL_XML_NAMESPACE):
        return xml_obj.find(element, namespace)

    def findall_with_namespace(xml_obj, element, namespace=NDL_XML_NAMESPACE):
        return xml_obj.findall(element, namespace)

    return app
