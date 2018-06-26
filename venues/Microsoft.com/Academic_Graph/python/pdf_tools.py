import re
import requests
from string import punctuation
from tika import parser
from fuzzywuzzy import fuzz
from ortools.graph import pywrapgraph


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

def get_emails_from_text(text):
    '''
    This function borrowed mostly unaltered from Chetan and Aditya's MS independent study project.
    '''
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

        if (re.findall(r"[a-zA-Z0-9]}@", new_tokens[i])):
            # (1)for when multiple email addresses are present non trivially in the form {a,b,c}@d.e

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

        if (re.findall(r"^@$|^AT$", new_tokens[i])):
            # (2)for when multiple email addresses are present non trivially in the form a AT b DOT c or a @ b . c (space separated)

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

def email_distance(email, author):
    """
    Fuzzy matching for calculating string edit distance between two emails.

    Comparing part of email before '@' with both full name of author and with
    just the initials of author, and taking max value among the two
    """
    email_parts = email.split('@')

    name_parts = author.split(' ')
    initials = ""
    for x in name_parts:
        if x:
            initials += x[0]

    return 1000 - max(fuzz.token_set_ratio(email_parts[0], author), fuzz.token_set_ratio(email_parts[0], initials))
    # return 1000-fuzz.token_set_ratio(email_parts[0], author)

def match_authors_to_emails(author_names, author_emails, verbose=False):
    """
    The node number for source, author emails, author names and sink are continuous values starting from 0.
    The edge capacities are 1. Supply at source is min(number of authors, number of emails), negative of which is
    demand at sink. Cost of edges from source to author email nodes and from author name nodes to sink are all zero.
    Cost of edges from emails to names are string edit distance calculated in email_distance function.
    """
    matched_emails = []
    matched_names = []

    start_nodes = []
    end_nodes = []
    costs = []
    capacities = []
    supplies = []

    # Edges from source to emails
    node_emails = 1
    for i in range(len(author_emails)):
        start_nodes.append(0)
        end_nodes.append(node_emails)
        costs.append(0)
        capacities.append(1)
        node_emails = node_emails + 1

    start_node_names = node_emails

    # Edges from emails to names
    node_emails = 1
    for i in author_emails:
        node_names = start_node_names
        for j in author_names:
            start_nodes.append(node_emails)
            end_nodes.append(node_names)
            capacities.append(1)

            pair_cost = email_distance(i, j)
            costs.append(pair_cost)
            node_names = node_names + 1
        sink_val = node_names
        node_emails = node_emails + 1

    # Edges from names to sink
    node_names = start_node_names
    for i in range(len(author_names)):
        start_nodes.append(node_names)
        end_nodes.append(sink_val)
        costs.append(0)
        capacities.append(1)
        node_names = node_names + 1

    min_pairs = min(len(author_emails), len(author_names))

    supplies.append(min_pairs)
    supplies_emails = [0] * len(author_emails)
    supplies_authors = [0] * len(author_names)
    supplies.extend(supplies_emails)
    supplies.extend(supplies_authors)
    supplies.append(-min_pairs)

    source = 0
    sink = sink_val

    # Instantiate a SimpleMinCostFlow solver.
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

    # Add each arc.
    for i in range(len(start_nodes)):
        min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i],
                                                    capacities[i], costs[i])

    # Add node supplies.
    for i in range(len(supplies)):
        min_cost_flow.SetNodeSupply(i, supplies[i])

    # Find the minimum cost flow between source and sink.
    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        if verbose: print('Total cost = ', min_cost_flow.OptimalCost())

        for arc in range(min_cost_flow.NumArcs()):

            # Can ignore arcs leading out of source or into sink.
            if min_cost_flow.Tail(arc) != source and min_cost_flow.Head(arc) != sink:

                # Arcs in the solution have a flow value of 1. Their start and end nodes
                # give an assignment of worker to task.

                if min_cost_flow.Flow(arc) > 0:
                    if verbose: print('Email %s | %s  Cost = %d' % (
                        author_emails[min_cost_flow.Tail(arc) - 1],
                        author_names[min_cost_flow.Head(arc) - start_node_names],
                        min_cost_flow.UnitCost(arc)))

                    matched_emails.append(author_emails[min_cost_flow.Tail(arc) - 1])
                    matched_names.append(author_names[min_cost_flow.Head(arc) - start_node_names])

    else:
        print('There was an issue with the min cost flow input.')

    return matched_emails, matched_names
