#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
import ast
from difflib import SequenceMatcher
from itertools import permutations
import requests
from string import punctuation
from tika import parser

def normalize(paper_name):
    paper_name_nopunc = paper_name
    for s in punctuation:
        paper_name_nopunc = paper_name_nopunc.replace(s, ' ')

    paper_name_nopunc_nowhitespace = ' '.join(c for c in paper_name_nopunc.split()).strip()
    normalized_paper_name = paper_name_nopunc_nowhitespace.lower()

    return normalized_paper_name

def pdf_to_text(pdf_path, timeout=5.0):
    response = requests.get(pdf_path, timeout=timeout)
    pdf_response_parsed = parser.from_buffer(response.content)
    pdf_text = pdf_response_parsed['content']
    return pdf_text

def mag_query(query_input, expression, headers):
    normalized_input = normalize(query_input)
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

'''
Code below borrowed mostly unaltered from Chetan and Aditya's MS independent study project.
'''
def get_emails_from_text(text):
    valid_extensions = [
        'ac', 'ad', 'ae', 'aero', 'af', 'ag', 'ai', 'al', 'am',
        'an', 'ao', 'aq', 'ar', 'arpa', 'as', 'asia', 'at', 'au',
        'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh',
        'bi', 'biz', 'bj', 'bl', 'bm', 'bn', 'bo', 'bq', 'br', 'bs',
        'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cat', 'cc', 'cd', 'cf',
        'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'com', 'coop',
        'cr', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'dd', 'de',
        'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'edu', 'ee', 'eg', 'eh',
        'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr',
        'ga', 'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm',
        'gn', 'gov', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy',
        'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im',
        'in', 'info', 'int', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm',
        'jo', 'jobs', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp',
        'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'local',
        'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me',
        'mf', 'mg', 'mh', 'mil', 'mk', 'ml', 'mm', 'mn', 'mo', 'mobi',
        'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'museum', 'mv', 'mw', 'mx',
        'my', 'mz', 'na', 'name', 'nato', 'nc', 'ne', 'net', 'nf', 'ng',
        'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'onion', 'org',
        'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'pro',
        'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa',
        'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm',
        'sn', 'so', 'sr', 'ss', 'st', 'su', 'sv', 'sx', 'sy', 'sz', 'tc',
        'td', 'tel', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to',
        'tp', 'tr', 'travel', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk',
        'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu',
        'wf', 'ws', 'xxx', 'ye', 'yt', 'yu', 'za', 'zm', 'zr', 'zw'
    ]

    tokens = text.split()
    new_tokens = []
    # split the whole .txt converted pdf into tokens for facilitating extraction of emails
    for item in tokens:
        for token in item.split(","):
            if (len(token) > 0):
                new_tokens.append(token)
    emaillist = []

    # the following code conatins regular expressions for identifying and extracting emails in different formats
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"  # regular expression for extraction of emails in trivial format i.e.each email is present as a single independent token of the form  a@b.c
    for i in range(len(new_tokens)):
        inst = re.findall(pattern, new_tokens[
            i])  # for when the email address is trivially present as a single token and a simple regular expression can enable extraction of emails
        if (inst):
            emaillist.append(inst[0])
        emaillist2 = []
        if (re.findall(r"[a-zA-Z0-9]}@", new_tokens[
            i])):  # (1)for when multiple email addresses are present non trivially in the form {a,b,c}@d.e
            address_extension = new_tokens[i].split("}")[1]
            name = new_tokens[i].split("}")[0]
            if (re.findall(r"{", name)):
                name = name.split("{")[1]
                look = 0
            else:
                look = 1
            emaillist2.append(name + address_extension)
            j = i - 1
            while ((len(re.findall(r"{", new_tokens[j])) == 0) and (look == 1) and (j >= 1)):
                emaillist2.append(new_tokens[j] + address_extension)
                j = j - 1
            if look == 1 and '{' in new_tokens[j]:
                emaillist2.append(new_tokens[j].replace('{', '') + address_extension)
            if ((look == 1) & (j == 0)):
                emaillist2 = []
            emaillist2.reverse()
            emaillist.extend(emaillist2)
        at = re.findall(r"^@$|^AT$", new_tokens[i])
        if (
                at):  # (2)for when multiple email addresses are present non trivially in the form a AT b DOT c or a @ b . c (space separated)
            if (new_tokens[i - 2] == "." or new_tokens[i - 2] == "DOT"):
                email_string = new_tokens[i - 3] + "." + new_tokens[i - 1] + '@'
            else:
                email_string = new_tokens[i - 1] + '@'
            for j in range(i + 1, len(new_tokens)):
                if new_tokens[j].lower() in valid_extensions:
                    email_string = email_string + new_tokens[j]
                    break
                else:
                    if (new_tokens[j] == "DOT"):
                        email_string = email_string + '.'
                    else:
                        email_string = email_string + new_tokens[j]
            if (len(email_string) < 35):
                emaillist.append(email_string)
    pattern = r"(^ *[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    email_list = []
    # an extra level of check where each email address extracted is comapared with the regular expressions to prevent false positives being selected as email addressed(could result from non trivial extraction(2)
    for email in emaillist:
        if re.search(pattern, email):
            if email[0] == ' ':
                email = email.split(' ')[1]
            email_list.append(email)
    # write the downloaded link into a file
    email_list = [e.lower() for e in email_list]
    return email_list

def match_emails_to_ordered_authors(emails, authors):
    '''
    to get best email order arrangement, all permutations of the email arrangments or orders
    are computed and the sum of SequenceMatcher ratios for each email order assignment and given
    sequence of DBLP authors is used as the similarity score for that arrangement
    '''
    max_length = max(len(emails), len(authors))

    if max_length < 16:
        print "computing {} permutations".format(max_length)
        for i in range(max_length):
            if len(emails) < i+1:
                emails.append('')
            if len(authors) < i+1:
                authors.append('')

        list_of_email_permutations = [item for item in permutations(emails)]

        list_of_sequence_scores = [0] * len(list_of_email_permutations)

        # compute a similarity score for each email order permutation
        for index1, email_permutations in enumerate(list_of_email_permutations):
            for index2, email in enumerate(list_of_email_permutations[index1]):
                list_of_sequence_scores[index1] += SequenceMatcher(None, email, authors[index2].replace('.', '')).ratio()

        largest_score_index = list_of_sequence_scores.index(max(list_of_sequence_scores))

        # get the best email arrangement for matching with authors
        email_order_list = list(list_of_email_permutations[largest_score_index])

        #return [pair for pair in zip(email_order_list, authors)]
        return email_order_list, authors
    else:
        return emails, authors

