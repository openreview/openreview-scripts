import argparse
import openreview
import json
import datetime
from random import randrange
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


## metadata for the home/sponsor/organizer/diversity/codeofconduct page
meta_data_home = {
    "date": "2020-05-01",
    "title": "ICLR 2020 Conference Virtual",
    "layout": [
        {
            "name": "Markdown",
            "option": {
                "center":"true",
                "content":" _ italic formatted with markdown _"
            }
        },
        {
            "name": "Organizers"
        },
        {
            "name": "Sponsors"
        },
        {
            "name": "JumbotronImage"
        }
    ]
}

meta_data_sponsors={
    "menuText":"Sponsor Info",
    "layout":[
        {
            "name":"Markdown",
            "option":"""## Sponsor Information for ICLR 2021
View ICLR 2021 sponsors »

Sponsor payments are due Mar 31, 2021 (anywhere on earth).

Read the information below and then 

### ICLR 2021 Sponsorship
Due to growing concerns about COVID-19, ICLR 2020 has decided to cancel its physical conference this year, instead shifting to a fully virtual conference.

We were very excited to hold ICLR in Addis Ababa, Ethiopia and it is disappointing that we will not all be able to come together in person in April. However, this unfortunate event does give us the opportunity to innovate on how to host an effective remote conference. The organizing committees are now working to create a virtual conference that will be valuable and engaging for both presenters and attendees.

Your sponsorship of the ICLR conference is greatly appreciated, and necessary, whether it has a physical or virtual presence this year.  We anticipate more participation of registered attendees with the virtual conference this year - especially given the current situation.  As a sponsor you will still receive many of the same benefits as listed in the sponsorship prospectus, specifically: 

Access to opt-in database and registrant CVs who are interested in recruiting contact
- Opportunity to participate in EXPO Lunch Talks (Bronze level excluded)
- Complimentary full-access registrations (number based on sponsorship level)
- Company name and logo on website with link
- Recognition of sponsor contributions prominently displayed throughout the virtual conference

Sponsorship funds will help in offsetting the livestreaming / recording costs and will also help students that lack the funds to purchase a registration in order to participate in the virtual conference.

Additional details regarding EXPO Lunch Talk applications will be sent soon.

Your support is greatly appreciated at this time.

Please feel welcome to email or set up a call to discuss any questions you may have.

Andrea Brown

email: andrea.brown@aicons.org

mobile: +1 714-213-1616

\***

For sponsors, the annual ICLR conference is an extraordinary opportunity for recruiting, branding, and communicating with **the most highly skilled people in the international community of artificial intelligence research**.

Sponsorship funds have been critical in ensuring the continued success of the conference, and importantly, make it possible for future leaders in the field to attend and present their research. ICLR appreciates your support and participation and will do its best to ensure that your sponsorship meets the needs of your company.
 

#### Benefits of Sponsorship
- **Branding opportunity** to position your company, products and services **to, approximately, 2,000 professionals in the field of deep learning**—the pivotal technology responsible for recent advancements in the fields of artificial intelligence, statistics and data science, and important application areas such as machine vision, computational biology, speech recognition, and robotics
- **Access to the ICLR Recruiting Database**, in addition to recruiting opportunities at the ICLR conference, **to attract the most highly skilled talent in this crucial AI field**
- **Promotion as a sponsor at the ICLR conference**—the premier conference in the field of deep learning—**and on the ICLR website and mobile app**
#### Key Dates
- **March 20**: Deadline to submit shipping information and customs/broker forms to Afroline Logistic Service
- **March 31, 2021, 4 p.m.**: Deadline for sponsorship applications and to return executed Sponsorship contract and payment
- **March 27**: Deadline to send booth design drawings for inspection and approval to ICLR Management
- **March 27**: Deadline to assign complimentary full-access conference registrations
- **March 27**: Deadline to submit Exhibitor Appointed Contractor (EAC) notification forms to ICLR Management
- **March 31**: Deadline to submit Booth Equipment Details order form and any additional orders for in-booth internet service, AV service, furnishings or catering to Flawless Events 
- **April 14**: Deadline to assign exhibitor badges
- **April 14**: Deadline to return Sponsor Certificate of Insurance
- **April 14**: Deadline to return executed EAC Agreements along with EAC Certificates of Insurance and the names of all EAC personnel who will be working in the exhibit hall to ICLR Management
- **April 24-25**: Exhibitor move-in and set up, Friday, April 24 from 9:00am-5:00pm and Saturday, April 25 from 8:00am-5:00pm
- **April 26-30**: Exhibit hall open to conference attendees: Sunday, April 26 from 6:30pm-8:00pm and Monday, April 27 through Thursday, April 30 from 10:00am-5:00pm each day
- **April 30-May 1**: Exhibitor teardown and move-out, small boxing on Thursday, April 30 from 5:00pm-6:30pm and teardown and move-out on Friday, May 1 from 8:00am-4:00pm
#### Sponsorship
Corporate sponsorship of ICLR contributes to the successful outcome of each year’s conference. ICLR appreciates your support and participation and wants your sponsorship to meet the needs of your company. After completing sections 1-4 on this page, ICLR will send you a contract and the Sponsorship Code of Conduct. Once we receive your executed ICLR contract and your payment, you will gain access to the ICLR Recruitment Database and we will process your complimentary full-access conference registrations and exhibitor badges.

#### ICLR Policy for Sponsor Events
ICLR welcomes sponsors at the conference and provides adequate space for them to interact with ICLR attendees at the venue.

Offsite Sponsor parties during the ICLR Conference should be held after all official conference activities have concluded each day.

ICLR discourages corporate events that conflict with any official conference activities.  This includes parallel meetings organized by Sponsors. However, if offsite satellite Sponsor meetings are held, they should take place before or after the official ICLR conference activities begin and end each day.

### Levels of Sponsorship:
To start the application, it's helpful to gather some information up front. When you are ready, please  Enter the Sponsor Portal » button to begin.

1. **Company PO number**. After you complete the application, you may email yourself an invoice from ICLR.cc for the amount of the sponsorship. If you need that invoice to have a PO number from your company on it, then you will need to add that PO number in section 3 of the application.
 
2. **Will you host an event?** If you intend to host an event during the conference, you will be asked about the type of event you will host, your target audience, and how will attend. We collect this information so we can align our goals with yours.
 
3. **Branding**. Our sponsor page highlights your company **logo**, provides a **link to your website**, and displays a **paragraph about your company**. You will be asked for each of these in various steps.
 
4. **Vector logo**. We need a high-quality vector version of your logo in .pdf, .ai, or .svg format. This logo may be enlarged for a sponsor poster, so it is important that it be a high-quality image in vector format.
 
5. **Payment**. Sponsorship and exhibitor payment is due by **March 31, 2021, 4 p.m.**. Your invoice will be generated in section 4 of the application.
### Questions? Contact us

To find out more detailed information about being a Sponsor Enter the Sponsor Portal »

If we can supply any additional information or be of further assistance, please do not hesitate to email: [Chris Brown](mailto:chris.brown@aicons.org?subject=ICLR%20Sponsor%20Portal%20Assistance) 

Thank you for your interest and we look forward to seeing you in Addis Ababa, Ethiopia.

## Venue Information
### Setup, Exhibit Hours and Teardown
<u>**Move-in**</u>: 

Saturday, May 4 from 12:00pm-5:00pm and

Sunday, May 5 from 8:00am-5:00pm.

If you need extra time to set up your booth, please contact Freeman Exhibitor Services at [FreemanNewOrleansES@freeman.com](mailto:FreemanNewOrleansES@freeman.com) to make arrangements.

*** Early move-in requests are not guaranteed, although we will do all that we can to support your request.

<u>**Exhibitor Hours**</u>: 

Mon, May 6:  10:00am - 7:30pm

Tue, May 7:    10:00am - 5:00pm

Wed, May 8:   10:00am - 5:00pm

Thur, May 9:   10:00am - 5:00pm

**There will be a Monday evening reception, 6:30 pm - 7:30 pm, in the Sponsor’s Hall**

<u>**Move-out**</u>: 

Thur, May 9:  5:00pm to 10:00pm and

Fri, May 10:   8:00am - 12:00pm

 

### Shipping & Customs Information
<h4 style="margin:0;text-decoration:underline">Advanced Warehouse Shipping Information</h4>
<h4 style="margin:0">Send exhibit materials to the following address.</h4>
TO: (<u style="font-style:italic">Exhibitor Name</u>)<br/>
&nbsp&nbsp&nbsp&nbspc/o: Freeman<br/>
&nbsp&nbsp&nbsp&nbsp905 Sams Ave.<br/>
&nbsp&nbsp&nbsp&nbspNew Orleans, LA 70123

EVENT: <u>ICLR 2019</u>

BOOTH #: (<u style="font-style:italic">booth number will be provided by Sponsor/Exhibitor</u>)

NO:\_\_\_\_\_ of\_\_\_\_\_ PCS

For shipping questions, please contact: 

**FREEMAN EXHIBIT TRANSPORTATION**

(800) 995-3579  Toll Free US & Canada

(512) 982-4187  Outside the US

(817) 607-5183   International Shipping Services

exhibit .transportation@freeman.com

FreemanNewOrleansES@freeman.com

 

#### <u>Customs Information</u>
**FREEMAN** is our designated official freight forwarder.

Anyone sending exhibit material to New Orleans from outside the United States needs to contact Freeman at [international.freight@freemanco.com](mailto:international.freight@freemanco.com) or +1.817.607.5183 prior to shipping.

If you have vendors shipping from outside the United States on your behalf, please notify them in advance to contact Freeman’s freight forwarding group using that same contact information.
 

### Exclusive Service Providers & Designated Official Contractors
#### Designated Official Exhibitor Services Contractor
**FREEMAN** is the designated official exhibitor services contractor at ICLR 2019 in New Orleans. Please refer to [Freeman’s Online Service Kit](https://www.freemanco.com/store/show/landing?referer=s&nav=02&showID=480482)  or [Freemans's Service Kit (PDF)](https://media.neurips.cc/Conferences/ICLR2019/Freeman/Freeman_Service_Kit.pdf) for booth information, including rules, regulations and forms.

If you choose to use Exhibitor Appointed Contractors (EACs) for any service that is not exclusively provided, you must follow the procedure in section 9.
 

#### Ordering Materials Handling Service
**Materials Handling Services will be exclusively managed by FREEMAN**. Please notify your carrier and exhibit designer / producer. All advanced and onsite orders need to come through FREEMAN. Shipping and customs information is provided in section 7.
 

#### Ordering Rigging Service
Rigging will be exclusively managed by FREEMAN if you need rigging, please contact Freeman Exhibitor Services at [FreemanNewOrleansES@freeman.com](mailto:FreemanNewOrleansES@freeman.com) to make arrangements.

If you intend to have a hanging sign or graphics above your booth, you must contact Freeman Exhibitor Services at [FreemanNewOrleansES@freeman.com](mailto:FreemanNewOrleansES@freeman.com) to coordinate the installation.
 

#### Ordering Electrical, Plumbing & All Other Utilities Services
**Electrical, Plumbing & All Other Utilities Services will be exclusively managed by New Orleans Ernest N. Morial Convention Center (MCCNO)**.

CREATE AN ACCOUNT AND PLACE YOUR ORDER ONLINE AT:

[MCCNO Exhibitor Services Online Portal](https://services.mccno.com/store/ungerboeck.cshtml?aat=HEW4dEax%2fVjCdLGEVcrHw8UNgO2alQLkgVo6dQF%2b8kA%3d)

Contact the convention center’s Exhibit Services staff at exhibit_services@mccno.com or by phone at 504-582-3036 if you still have questions or need additional information.

 

#### Ordering Internet, WiFi & All Other Telecommunications Services
**Internet, WiFi & All Other Telecommunications Services will be exclusively managed by New Orleans Ernest N. Morial Convention Center (MCCNO)**.

CREATE AN ACCOUNT AND PLACE YOUR ORDER ONLINE AT:

[MCCNO Exhibitor Services Online Portal](https://services.mccno.com/store/ungerboeck.cshtml?aat=HEW4dEax%2fVjCdLGEVcrHw8UNgO2alQLkgVo6dQF%2b8kA%3d)

Contact Marquita Sparks, Technology Services Coordinator, at [msparks@mccno.com](mailto:msparks@mccno.com) or by phone at [(504) 582-3147](tel:(504) 582-3147) if you still have questions or need additional information.

 

#### Ordering Audio-Visual Service
FREEMAN is the designated official **Audio-Visual Service** provider for exhibitors at ICLR 2019 in New Orleans.

To use Freeman’s AV service, contact FreemanNewOrleansES@freeman.com to get a quote or place an order.

If you choose to use an Exhibitor Appointed Contractor (EACs) for AV service, you must follow the procedure in the section 8.


#### Ordering Food and Beverage Service
**Food and Beverage Service will be exclusively managed by New Orleans Ernest N. Morial Convention Center (MCCNO)**.

CREATE AN ACCOUNT AND PLACE YOUR ORDER ONLINE AT:

[MCCNO Exhibitor Services Online Portal](https://services.mccno.com/store/ungerboeck.cshtml?aat=HEW4dEax%2fVjCdLGEVcrHw8UNgO2alQLkgVo6dQF%2b8kA%3d)

Contact Linsey Normand-Marriott, the convention center’s Catering Sales Manager, at [Linsey.Marriott@Centerplate.com](mailto:Linsey.Marriott@Centerplate.com) or by phone at [(504) 670-7254](tel:(504) 670-7254) if you questions or would like to place an order.


#### Ordering Booth Security
COMING SOON.
 

#### Ordering Booth Cleaning Service
**Booth Cleaning Service will be exclusively provided by FREEMAN**. If you need booth cleaning, please contact Freeman Exhibitor Services at [FreemanNewOrleansES@freeman.com](mailto:FreemanNewOrleansES@freeman.com) to make arrangements.

 

### Exhibitor Appointed Contractors (EACs)
An Exhibitor Appointed Contractor (EAC) is any company other than the designated official contractors which a Sponsor wants to employ inside the exhibit hall before, during or after the conference. This includes all EAC exhibit designers/producers, booth security contractors, labor, supervisors and any other third party appointed by the Sponsor.

If your company plans to use a firm who is not an official service contractor as designated by ICLR Management, **please notify ICLR by April 5, 2019 by completing the ICLR 2019** EAC Notification Form  **for each EAC that you plan to use**. After completing each form email it to [Chris Brown](mailto:chris.brown@aicons.orgu?subject=ICLR%20-%20New%20Orleans%20-%20EAC%20Form%20Submittal).

Once your EAC Notification Form is received, ICLR Management will send your EAC instructions that they must complete by April 24, 2019 in order to be allowed in the exhibit hall.

General Rules Regarding EACs for ICLR 2019

In the event an EAC of record for the Sponsor hires sub-EACs, these sub-EACs must be identified to ICLR Management by the Sponsor and follow all rules and regulations outlined in Freeman’s Online Service Kit or Freemans's Service Kit (PDF) and in the EAC Agreement signed by the EAC of record.

ICLR Management cannot accept requests from the EAC or sub-EACs, only from Sponsors.

No permission will be given to use an EAC or sub-EAC for the performance of the following services:

- Materials Handling
- Rigging
- Electrical, Plumbing & All Other Utilities 
- Internet, WiFi & All Other Telecommunications
- Food & Beverage
- Booth Cleaning
Go to EAC Notification Form » 

### Exhibitor Badges
To access the exhibit hall, everyone will need a badge, either as an exhibitor-only or a full-access conference registrant. An Exhibitor Badge only grants access to the exhibit hall and public areas, not to any other academic conference activities. A full-access Conference Badge allows access to all events including academic events.

**Please enter the email address for each person needing an Exhibitor Badge in the form below. After entering an email address press the "Update Exhibitor Badges" button and then repeat that process for each person. If the email address of the person that you submit does not have an ICLR account, a red X will appear after you submit their email address.  Please invite those without an account to create an account by [sending them a Profile Create Request](mailto:?body=Each%20person%20manning%20a%20booth%20at%20the%20upcoming%20ICLR%20meeting%20will%20need%20a%20badge%20to%20access%20the%20exhibitor%20area.%20In%20order%20to%20get%20a%20badge%2C%20you%20will%20need%20to%20create%20a%20profile%20on%20the%20ICLR%20website.%20%20Please%20visit%2C%0A%0Ahttps%3A//ICLR.cc/Profile/create%0A%0Ato%20create%20your%20profile.%20Please%20reply%20with%20the%20email%20you%20used%20for%20your%20ICLR.cc%20profile%20and%20I%20will%20ensure%20that%20a%20badge%20is%20ready%20for%20you%20when%20you%20arrive.%20Thanks%0A%0A&subject=Please%20create%20a%20ICLR.cc%20profile)**."""
        }
    ]
}

meta_data_organizers={
    "layout":[
        {
            "name":"Markdown",
            "option":"_ content of organizers page formatted with markdown _"
        }
    ]
}

meta_data_codeofconduct={
    "menuText":"Code of Conduct",
    "layout":[
        {
            "name":"Markdown",
            "option":"""# ICLR Code of Conduct


The open exchange of ideas, the freedom of thought and expression, and respectful scientific debate are central to the goals of this conference on machine learning; this requires a community and an environment that recognizes and respects the inherent worth of every person.

# Who 
All participants---attendees, organizers, reviewers, speakers, sponsors, and volunteers at our conference, workshops, and conference-sponsored social events---are required to agree with this Code of Conduct both during the event and on official communication channels, including social media. Organizers will enforce this code, and we expect cooperation from all participants to help ensure a safe and productive environment for everybody.

# Scope
The conference commits itself to provide an experience for all participants that is free from harassment, bullying, discrimination, and retaliation. This includes offensive comments related to gender, gender identity and expression, age, sexual orientation, disability, physical appearance, body size, race, ethnicity, religion (or lack thereof), politics, technology choices, or any other personal characteristics. Bullying, intimidation, personal attacks, harassment, sustained disruption of talks or other events, and behavior that interferes with another participant's full participation will not be tolerated. This includes sexual harassment, stalking, following, harassing photography or recording, inappropriate physical contact, unwelcome sexual attention, public vulgar exchanges, and diminutive characterizations, which are all unwelcome in this community.

The expected behaviour in line with the scope above extends to any format of the conference, including any virtual forms, and to the use of any online tools related to the conference. These include comments on OpenReview within or outside of reviewing periods, conference-wide chat tools, Q&A tools, live stream interactions, and any other forms of virtual interaction. Trolling, use of inappropriate imagery or videos, offensive language either written or in-person over video or audio, unwarranted direct messages (DMs), and extensions of such behaviour to tools outside those used by the conference but related to the conference, its program and attendees, are not allowed. In addition, doxxing or revealing any personal information to target any participant will not be tolerated.

Sponsors are equally subject to this Code of Conduct. In particular, sponsors should not use images, activities, or other materials that are of a sexual, racial, or otherwise offensive nature. Sponsor representatives and staff (including volunteers) should not use sexualized clothing/uniforms/costumes or otherwise create a sexualized environment. This code applies both to official sponsors as well as any organization that uses the conference name as branding as part of its activities at or around the conference.

# Outcomes
Participants asked by any member of the community to stop any such behavior are expected to comply immediately. If a participant engages in such behavior, the conference organizers may take any action they deem appropriate, including: a formal or informal warning to the offender, expulsion from the conference (either physical expulsion, or termination of access codes) with no refund, barring from participation in future conferences or their organization, reporting the incident to the offender’s local institution or funding agencies, or reporting the incident to local law enforcement. A response of "just joking" will not be accepted; behavior can be harassing without an intent to offend. If action is taken, an appeals process will be made available.

# Reporting
If you have concerns related to your inclusion at that conference, or observe someone else's difficulties, or have any other concerns related to inclusion, please email the [ICLR 2021 Program Chairs](mailto:iclr2021programchairs@googlegroups.com).  For online events and tools, there are options to directly report specific chat/text comments, in addition to the above reporting. Complaints and violations will be handled with discretion. Reports made during the conference will be responded to within 24 hours; those at other times in less than two weeks. We are prepared and eager to help participants contact relevant help services, to escort them to a safe location, or to otherwise assist those experiencing harassment to feel safe for the duration of the conference. We gratefully accept feedback from the community on policy and actions; please contact us.

Updated March 29, 2020"""
        }
    ]
}

meta_data_diversityandinclusion={
    "menuText":"Diversity & Inclusion",
    "layout":[
        {
            "name":"Markdown",
            "option":"""### ICLR 2021 Group Activities
The schedule of events for diversity groups will appear here once it's known.

#### Diversity & Inclusion
The International Conference on Learning Representations is taking seriously questions of diversity, equity, and inclusion in our conference. Our efforts are building on several grassroots efforts from the Women in Machine Learning, Black in AI, Queer in AI and LatinX in AI.  ICLR is working to expand these efforts to make the conference as welcoming as possible to all.

In addition to hosting diversity-related events, the conference is also making and considering structural changes. These include a new [Code of Conduct](/event/group?id=ICLR.cc/2020/Conference/Virtual/CodeOfConduct) introduced in 2018. We are actively working to make the conference event itself more inclusive, including supporting childcare, nursing mothers, attendees with disabilities, and gender inclusive measures.  We are also exploring options with the venue and caterers to ensure that everyone can have a positive, equitable conference experience. 

#### WIML
WiML is holding a Virtual Social @ ICLR 2020, involving a Virtual Panel and a Mentoring Session, to discuss how COVID-19 has impacted our daily lives and our work and about ongoing research on COVID-19. 

Date: Thursday, April 30th, 2020, 9.00am-11.00am PST

Event details: https://wimlworkshop.org/sh_events/wiml-iclr/ 

Everyone registered for ICLR is encouraged to attend. The event is limited to 500 attendees and will operate on a first-come first-served basis. Information about how to participate in the event will be posted on https://iclr.cc/virtual/socials.html. Join the #wiml channel in the ICLR chat for more event announcements.

Additionally, as part of our efforts to support our community in this time of COVID-19, WiML introduced a new initiative to fund registration fees for students and individuals in-need from all over the world to attend the virtual ICLR conference. With this new initiative, we hope to extend WiML's geographic reach and impact beyond individuals who are able to attend conferences in-person. The application was due on April 21. With the support of WiML Corporate Partners (https://wimlworkshop.org/partners/), we were able to offer ICLR 2020 registration fee funding to a total of 103 individuals.

#### {Dis}Abilities in AI
Please contact us with any assistance needs at the conference. 

#### Safety Guide
To help LGBTQ+, and all other attendees, make informed decisions and have an understanding of some safety aspects of attending the conference, please see this SAFETY GUIDE."""
        }
    ]
}

## Main conference virtual group
conference_id='ICLR.cc/2020/Conference'
virtual_group_id='ICLR.cc/2020/Conference/Virtual'
client.post_group(openreview.Group(id=virtual_group_id,
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=[],
                 web_string=json.dumps(meta_data_home)))


client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=[f"{virtual_group_id}/Sponsors/Diamond", f"{virtual_group_id}/Sponsors/Gold", f"{virtual_group_id}/Sponsors/Silver"],
                 web_string=json.dumps(meta_data_sponsors)))

client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors/Diamond",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["deepmind", "facebook", "googleresearch"]))

client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors/Gold",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["amazon", "ibm", "openai"]))

client.post_group(openreview.Group(id=f"{virtual_group_id}/Sponsors/Silver",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["apple", "microsoft", "elementai"]))


client.post_group(openreview.Group(id=f"{virtual_group_id}/Organizers",
                 readers=['everyone'],
                 writers=[conference_id],
                 signatures=[conference_id],
                 signatories=[],
                 members=["~Alexander_Rush1", "~Shakir_Mohamed1", "~Martha_White1", "~Kyunghyun_Cho1", "~Dawn_Song1"],
                 web_string=json.dumps(meta_data_organizers)))

client.post_group(openreview.Group(id=f"{virtual_group_id}/CodeOfConduct",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_codeofconduct)))

client.post_group(openreview.Group(id=f"{virtual_group_id}/DiversityAndInclusion",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_diversityandinclusion)))

## Session invitation
session_invitation_id=f"{virtual_group_id}/-/Session"
client.post_invitation(openreview.Invitation(
    id=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    invitees=[conference_id],
    signatures=[conference_id],
    reply={
        'readers': { 'values': ['everyone'] },
        'writers': { 'values': [conference_id] },
        'signatures': { 'values': [conference_id] },
        'content': {
            'start': { 'value-regex': '.*' },
            'end': { 'value-regex': '.*' },
            'title': { 'value-regex': '.*' },
            'description': { 'value-regex': '.*' }
        }
    }
))


## Create two sessions
sessions = []
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 15, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 18, 0)),
        'title': 'Session 1',
        'description':'this is the description of session 1'
    }
)))
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 18, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 2, 20, 0)),
        'title': 'Session 2',
        'description':'this is the description of session 2'
    }
)))
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 9, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 10, 0)),
        'title': 'Session 3',
        'description':'this is the description of session 3'
    }
)))
sessions.append(client.post_note(openreview.Note(
    invitation=session_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'start': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 10, 0)),
        'end': openreview.tools.datetime_millis(datetime.datetime(2020, 10, 5, 12, 0)),
        'title': 'Session 4',
        'description':'this is the description of session 4'
    }
)))


## Presentation invitation
presentation_invitation_id=f"{virtual_group_id}/-/Presentation"
client.post_invitation(openreview.Invitation(
    id=presentation_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    invitees=[conference_id],
    signatures=[conference_id],
    reply={
        'readers': { 'values': ['everyone'] }, ## should be restricted?
        'writers': { 'values': [conference_id] },
        'signatures': { 'values': [conference_id] },
        'content': {
            'slideslive': { 'value-regex': '.*' },
            'chat': { 'value-regex': '.*' },
            'live': { 'value-regex': '.*' },
            'session': { 'value-regex': '.*' }
        }
    }
))


submissions = client.get_notes(invitation='ICLR.cc/2020/Conference/-/Submission')


for s in tqdm(submissions):
    ## Create presentations based on ICLR accepted papers
    presentation_1 = client.post_note(openreview.Note(
        invitation=presentation_invitation_id,
        original=s.id,
        readers=['everyone'],
        writers=[conference_id],
        signatures=[conference_id],
        content={
            'slideslive': '38915149',
            'chat': 'https://rocketchat.com/paper',
            'live': 'https://zoom.us/paper',
            'session': sessions[randrange(4)].id
        }
    ))
