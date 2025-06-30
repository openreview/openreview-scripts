import openreview
import nampi

def recruit_reviewer(client, email, first, verbose=True):
    '''
    Recruit a reviewer to NAMPI 2018

    The hashkey is important for uniquely identifying the user, without
    requiring them to already have an openreview account. The second argument
    to the client.get_hash() function is just a big random number that the
    invitation's "process function" also knows about.
    '''
    hashkey = client.get_hash(email.encode('utf-8'), "2810398440804348173")

    # build the URL to send in the message
    url = '{baseurl}/invitation?id={recruitment_inv}&email={email}&key={hashkey}&response='.format(
        baseurl = client.baseurl,
        recruitment_inv = nampi.recruit_reviewers.id,
        email = email,
        hashkey = hashkey
    )

    # format the message defined above
    personalized_message = nampi.RECRUIT_MESSAGE.format(
        name = first,
        accept_url = url + "Yes",
        decline_url = url + "No"
    )

    # send the email through openreview
    response = client.send_mail(nampi.RECRUIT_MESSAGE_SUBJ, [email], personalized_message)

    if 'groups' in response and response['groups']:
        reviewers_invited = client.get_group(nampi.REVIEWERS_INVITED_ID)
        client.add_members_to_group(reviewers_invited, response['groups'])

    if verbose:
        print "Sent to the following: ", response
        print personalized_message
