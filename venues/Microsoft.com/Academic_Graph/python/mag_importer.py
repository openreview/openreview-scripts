#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import pdf_tools

## MAG-specific functions below

def mag_query(query_input, expression, headers):
    normalized_input = pdf_tools.normalize(query_input)
    params = {
        'expr': expression.format(normalized_input),
        'model': 'latest',
        'count': '150',
        'offset': '0',
        'attributes': 'Ti,Id,AA.AuN,E',
    }
    mag_response = requests.get(
        'https://westus.api.cognitive.microsoft.com/academic/v1.0/evaluate',
        params = params,
        headers = headers)

    mag_dict = json.loads(mag_response.text)

    entities = mag_dict['entities']
    for entity in entities:
        if 'E' in entity:
            entity['E'] = json.loads(entity['E'])

    return mag_dict['expr'], mag_dict['entities']

def get_data_by_title(title, headers):
    return mag_query(title, 'Ti=\'{}\'', headers)

def get_data_by_author(author, headers):
    return mag_query(author, "Composite(AA.AuN=='{}')", headers)

def entities_from_file(csv_infile):
    loaded_entities = []
    with open(csv_infile) as f:
        reader = csv.reader(f)
        for row in reader:
            loaded_entities.append(json.loads(row[0]))
    return loaded_entities

def entities_to_file(entities, csv_outfile):
    with open(csv_outfile, 'wb') as f:
        writer = csv.writer(f)
        for entity in entities:
            writer.writerow([json.dumps(entity)])

def processANF(ANF):
    sorted_authors = sorted(ANF, key=lambda entry: entry.get('S'))
    return ['{} {}'.format(entry.get('FN', ''), entry.get('LN', '')) for entry in sorted_authors]

def process_inverted_index(inverted_index):
    forward_index = {}
    max_index = 0
    word_array = []
    for word in inverted_index:
        index_list = inverted_index[word]
        for index in index_list:
            forward_index[index] = word.replace('$','')
            if index > max_index:
                max_index = index
    for c in range(max_index + 1):
        word_array.append(forward_index[c])
    return ' '.join(word_array)

def find_valid_source(sources):
    for source in sources:
        if 'Ty' in source and 'U' in source and source.get('Ty') == 3 and source.get('U', '').endswith('.pdf'):
            return source.get('U')

    return None

def mag_transform(raw_entity):
    '''
    Transform a MAG entity into a format that is compatible with OpenReview.

    The return value of this function will be the "content" field of an OpenReview Note.
    '''

    # argument raw_entity is equivalent to the variable mag_raw in magTransform.js

    # variable transformed_content is equivalent to the returned variable json in magTransform.js
    transformed_content = {}

    if 'Ti' in raw_entity:
        transformed_content['title'] = raw_entity.get('Ti','').replace('.','')
    if 'AA' in raw_entity:
        transformed_content['authors'] = [author_entry.get('AuN','') for author_entry in raw_entity.get('AA', [])]
    if 'E' in raw_entity:
        entity = raw_entity.get('E', {})
    if 'DN' in entity:
        transformed_content['title'] = entity.get('DN','').replace('.','')
    if 'ANF' in entity:
        transformed_content['authors'] = processANF(entity.get('ANF',[]))
    if 'DOI' in entity:
        transformed_content['DOI'] = entity.get('DOI') # should this default to the empty string?
    if 'IA' in entity and 'InvertedIndex' in entity['IA']:
        transformed_content['abstract'] = process_inverted_index(entity['IA']['InvertedIndex'])
    if 'S' in entity:
        valid_source = find_valid_source(entity.get('S',[]))
        if valid_source:
            transformed_content['pdf'] = valid_source
    return transformed_content

