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
                "center": "true",
                "content": " _ italic formatted with markdown _"
            }
        },
        {
            "name": "HappeningNow"
        },
        {
            "name": "Organizers"
        },
        {
            "name": "Sponsors"
        },
        {
            "name": "JumbotronImage"
        },
        {
            "name": "Footer"
        }
    ],
    "footer": {
        "color": "lightgray",
        "columns": [
            {
                "id": "1",
                "type": "imageText",
                "hideOnSmallScreen": "true",
                "image": "/navlogo.png",
                "imageWidth": "80%",
                "textContents": [
                    "The International Conference on Learning Representations(ICLR).",
                    "All Rights Reserved.",
                ],
            },
            {
                "id": "2",
                "type": "list",
                "title": "About",
                "links": [
                    {
                        "text": "ICLR Board",
                        "url": "",
                    },
                    {
                        "text": "Organizing Committee",
                        "url": "",
                    },
                    {
                        "text": "Program Committee",
                        "url": "",
                    },
                    {
                        "text": "ICLR Archived",
                        "url": "",
                    },
                    {
                        "text": "Contact ICLR",
                        "url": "",
                    },
                ],
            },
            {
                "id": "3",
                "type": "list",
                "title": "Submissions",
                "links": [
                    {
                        "text": "Deadlines",
                        "url": "",
                    },
                    {
                        "text": "Papers",
                        "url": "",
                    },
                    {
                        "text": "Workshops",
                        "url": "",
                    },
                    {
                        "text": "Socials",
                        "url": "",
                    },
                    {
                        "text": "Reviewers",
                        "url": "",
                    },
                    {
                        "text": "Sponsor Expo",
                        "url": "",
                    },
                ],
            },
            {
                "id": "4",
                "type": "list",
                "title": "Attending",
                "links": [
                    {
                        "text": "Registration",
                        "url": "",
                    },
                    {
                        "text": "Code of Conduct",
                        "url": "",
                    },
                    {
                        "text": "Schedule",
                        "url": "/event/calendar2",
                    },
                    {
                        "text": "Accessibility",
                        "url": "",
                    },
                    {
                        "text": "Privacy",
                        "url": "",
                    },
                    {
                        "text": "FAQ",
                        "url": "",
                    },
                ],
            },
        ],
    }
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

meta_data_guides={
    "menuText":"Guides",
    "layout":[
        {
            "name":"Markdown",
            "option":"## Sponsor Information for ICLR 2021"
        }
    ]
}
meta_data_presentationGuide={
    "menuText":"Presentation Guide",
    "layout":[
        {
            "name":"Markdown",
            "option":"""# Presentations Guide
A quick reference on all presentation-related elements of ICLR2020. We will share an allocation schedule in February 2020.

## Posters
All accepted papers are allocated a poster presentation. Make sure your poster can be contained within a size of 90cm x 122cm (width x height). ICLR does not provide any poster printing facilities, and presenters are responsible for printing their posters. Posters will be fixed to the poster boards using tape, which we will supply.

Note that a significant number of attendees are color-blind, so it is important to present colorblind friendly documents (papers/posters/slides). To this end, when illustrating a graph or picture, consider using patterns and textures (e.g. dotted lines, dashes, etc.) to show contrast and not rely only on colors in order to convey a message. Also, please avoid using color combinations known to be difficult for color-blind people. More information in this regard can be found at the links below: [How to Design for Color Blindness](https://usabilla.com/blog/how-to-design-for-color-blindness/), [Three Tools to Help You Make Colorblind-Friendly Graphics](https://knightlab.northwestern.edu/2016/07/18/three-tools-to-help-you-make-colorblind-friendly-graphics/)

## Spotlight Talks
ICLR2020 includes **spotlight talks that are be 4mins long**. To ensure that we have the smoothest handover, all spotlight presenters will be asked to share their slides with their session chair ahead of the conference using Google Slides. Session chairs will get in touch 2 weeks before the conference. We will update this page soon with tips on giving a good spotlight talk.

## Selected Talks
There will be several longer talks that are **10mins long, with an additional 2 mins for questions**. Slides for longer talks should also be shared with your session chair using Google slides two weeks before the conference. We will update the specific allocation of talks before.

"""
        }
    ]
}
meta_data_reviewerGuide={
    "menuText":"Reviewer Guide",
    "layout":[
        {
            "name":"Markdown",
            "option":"""# **ICLR 2021 Reviewer Guide**
Thank you for agreeing to serve as an ICLR 2021 reviewer. Your contribution as a reviewer is paramount to creating an exciting and high-quality program. We ask that:

1. Your reviews are timely and substantive.

2. You follow the reviewing guidelines below.

3. You adhere to our Code of Ethics in your role as a reviewer. You must also adhere to our [Code of Conduct](/event/group?id=ICLR.cc/2020/Conference/Virtual/CodeOfConduct).

This guide is intended to help you understand the ICLR 2021 decision process and your role within it. It contains:

1. A flowchart outlining the [global review process](#review_process)

2. An outline of the [main reviewer tasks](#main_tasks)

3. Step-by-step [reviewing instructions](#step_by_step) (especially relevant for reviewers that are new to ICLR)

4. [Review examples](#exmaples)

5. An [FAQ](#faq).

---

<h2 style="color:#337ab7">We’re counting on you</h2>
As a reviewer you are on the front line of the program creation process for ICLR 2021. Your ACs and the PCs will rely greatly on your expertise and your diligent and thorough reviews to make decisions on each paper. Therefore, your role as a reviewer is critical to ensuring a strong program for ICLR 2021.


High-quality reviews are also very valuable for helping authors improve their work, whether it is eventually accepted by ICLR 2021, or not. Therefore it is important to treat each valid ICLR 2021 submission with equal care.

As a token of our appreciation for your essential work, all reviewers will be acknowledged during the opening ceremony. Top reviewers will receive special acknowledgement and free registration to ICLR 2021.


---
<h2 id="review_process" style="color:#337ab7">The global review process</h2>

<img src="https://lh3.googleusercontent.com/1BZWkuflo20dDNy5nEPhXbsNdet8U-EtnwPj3_WyQAu0W1jAiE8Uwf9BfC5DbDzy0QeQTSK7I7XuyzpbDslXLZr6prKHDvzZNhz5RMhbEPS0L8LwjaJwrhoQ6bHr5xqVQYdF8k-u" style="height:351px; margin-left:0px; margin-top:0px; width:624px">

---
<h2 id="main_tasks" style="color:#337ab7">Main reviewer tasks</h2>
The main reviewer tasks and dates are as follows:

- Create your profile (by September 4th)

- Bid on papers (Monday, 5 October 2020 - Thursday, 8 October 2020)

- Write a constructive, thorough and timely review (Monday, 12 October 2020 - Wednesday, 28 October 2020)

- Discuss with authors and other reviewers to clarify and improve the paper (Tuesday,  10 November 2020 - Monday, 30 November 2020)

- Provide a final recommendation to the area chair assigned to the paper (by Monday, 30 November 2020)

- Flag any potential CoE violations and/or concerns (throughout the review and discussion phase).

---
<h2 id="step_by_step" style="color:#337ab7">Reviewing a submission: step-by-step</h2>
Summarized in one line, a review aims to determine whether a submission will bring sufficient value to the community and contribute new knowledge. The process can be broken down into the following main reviewer tasks:


1. **Read the paper**: It’s important to carefully read through the entire paper, and to look up any related work and citations that will help you comprehensively evaluate it. Be sure to give yourself sufficient time for this step.

2. **While reading, consider the following**:

	1. Objective of the work: What is the goal of the paper? Is it to better address a known application or problem, draw attention to a new application or problem, or to introduce and/or explain a new theoretical finding? A combination of these? Different objectives will require different considerations as to potential value and impact.

	2. Strong points: is the submission clear, technically correct, experimentally rigorous, reproducible, does it present novel findings (e.g. theoretically, algorithmically, etc.)?

	3. Weak points: is it weak in any of the aspects listed in b.?

	4. Be mindful of potential biases and try to be open-minded about the value and interest a paper can hold for the entire ICLR community, even if it may not be very interesting for you.

3. **Answer three key questions for yourself, to make a recommendation to Accept or Reject**:

	1. What is the specific question and/or problem tackled by the paper?

	2. Is the approach well motivated, including being well-placed in the literature?

	3. Does the paper support the claims? This includes determining if results, whether theoretical or empirical, are correct and if they are scientifically rigorous.

4. **Write your initial review, organizing it as follows**:

	1. Summarize what the paper claims to contribute. Be positive and generous.

	2. List strong and weak points of the paper. Be as comprehensive as possible.

	3. Clearly state your recommendation (accept or reject) with one or two key reasons for this choice.

	4. Provide supporting arguments for your recommendation.

	5. Ask questions you would like answered by the authors to help you clarify your understanding of the paper and provide the additional evidence you need to be confident in your assessment.

	6. Provide additional feedback with the aim to improve the paper. Make it clear that these points are here to help, and not necessarily part of your decision assessment.

5. **Complete the CoE report**: ICLR has adopted the following Code of Ethics (CoE). Reviewers must complete a CoE report for each paper assigned to them. The report is a simple form with two questions.The first asks whether there is a potential violation of the CoE. The second is relevant only if there is a potential violation and asks the reviewer to explain why there may be a potential violation. In order to answer these questions, it is therefore important that you read the CoE before starting your reviews. We recommend that, for each paper, reviewers complete this report immediately after completing their initial review.

6. **Engage in discussion**: The discussion phase at ICLR is different from most conferences in the AI/ML community. During this phase, reviewers, authors and area chairs engage in asynchronous discussion and authors are allowed to revise their submissions to address concerns that arise. It is crucial that you are actively engaged during this phase.

7. **Provide final recommendation**: Update your review, taking into account the new information collected during the discussion phase, and any revisions to the submission. Maintain a spirit of openness to changing your initial recommendation (either to a more positive or more negative) rating.


**For great in-depth resources on reviewing, see these resources:**

- Daniel Dennet, [Criticising with Kindness](https://www.brainpickings.org/2014/03/28/daniel-dennett-rapoport-rules-criticism/).

- Comprehensive advice: [Mistakes Reviewers Make](https://sites.umiacs.umd.edu/elm/2016/02/01/mistakes-reviewers-make/)

- Views from multiple reviewers: [Last minute reviewing advice](https://acl2017.wordpress.com/2017/02/23/last-minute-reviewing-advice/)

- Perspective from instructions to Area Chairs: [Dear ACs](https://www.seas.upenn.edu/~nenkova/AreaChairsInstructions.pdf).

---

<h2 id="examples" style="color:#337ab7">Review Examples</h2>
Below are two reviews, copied verbatim from previous ICLR conferences, that adhere well to our guidelines above: one for an "Accept" recommendation, and the other for a "Reject" recommendation. Note that while each review is formatted differently according to each reviewer's style, both reviews are well-structured and therefore easy to navigate.



### Example 1: Recommendation to Accept

##########################################################################

Summary:


The paper provides a interesting direction in the meta-learning filed. In particular, it proposes to enhance meta learning performance by fully exploring relations across multiple tasks. To capture such information, the authors develop a heterogeneity-aware meta-learning framework by introducing a novel architecture--meta-knowledge graph, which can dynamically find the most relevant structure for new tasks.

##########################################################################

Reasons for score:


Overall, I vote for accepting. I like the idea of mining the relation between tasks and handle it by the proposed meta-knowledge graph. My major concern is about the clarity of the paper and some additional ablation models (see cons below). Hopefully the authors can address my concern in the rebuttal period.


##########################################################################Pros:


1. The paper takes one of the most important issue of meta-learning: task heterogeneity. For me, the problem itself is real and practical.


2. The proposed meta-knowledge graph is novel for capturing the relation between tasks and address the problem of task heterogeneity. Graph structure provides a more flexible way of modeling relations. The design for using the prototype-based relational graph to query the meta-knowledge graph is reasonable and interesting.


3. This paper provides comprehensive experiments, including both qualitative analysis and quantitative results, to show the effectiveness of the proposed framework. The newly constructed Art-Multi dataset further enhances the difficulty of tasks and makes the performance more convincing.


##########################################################################

Cons:


1. Although the proposed method provides several ablation studies, I still suggest the authors to conduct the following ablation studies to enhance the quality of the paper:

	(1) It might be valuable to investigate the modulation function. In the paper, the authors compare sigmoid, tanh, and Film layer. Can the authors analyze the results by reducing the number of gating parameters in Eq. 10 by sharing the gate value of each filter in Conv layers?


	(2) What is the performance of the proposed model by changing the type of aggregators?


2. For the autoencoder aggregator, it would be better to provide more details about it, which seems not very clear to me.


3. In the qualitative analysis (i.e., Figure 2 and Figure 3), the authors provide one visualization for each task. It would be more convincing if the authors can provide more cases in the rebuttal period.


##########################################################################

Questions during rebuttal period:


Please address and clarify the cons above


#########################################################################

Some typos:

(1) Table 7: I. no sample-level graph -> I. no prototype-based graph

(2) 5.1 Hyperparameter Settings: we try both sigmoid, tanh Film -> we try both sigmoid, tanh, Film.

(3) parameteric -> parametric

(4) Table 2: Origninal -> original

(5) Section 4 first paragraph: The enhanced prototype representation -> The enhanced prototype representations


Updates: Thanks for the authors' response. The newly added experimental results address my concerns. I believe this paper will provide new insights for this field and I recommend this paper to be accepted.



### Example 2: Recommendation to Reject


Review: This paper proposes Recency Bias, an adaptive mini batch selection method for training deep neural networks. To select informative minibatches for training, the proposed method maintains a fixed size sliding window of past model predictions for each data sample. At a given iteration, samples which have highly inconsistent predictions within the sliding window are added to the minibatch. The main contribution of this paper is the introduction of sliding window to remember past model predictions, as an improvement over the SOTA approach: Active Bias, which maintains a growing window of model predictions. Empirical studies are performed to show the superiority of Recency Bias over two SOTA approaches. Results are shown on the task of (1) image classification from scratch and (2) image classification by fine-tuning pretrained networks.


+ves:

\+ The idea of using a sliding window over a growing window in active batch selection is interesting.

\+ Overall, the paper is well written. In particular, the Related Work section has a nice flow and puts the proposed method into context. Despite the method having limited novelty (sliding window instead of a growing window), the method has been well motivated by pointing out the limitations in SOTA methods.

\+ The results section is well structured. It's nice to see hyperparameter tuning results; and loss convergence graphs in various learning settings for each dataset.


Concerns:

\- The key concern about the paper is the lack of rigorous experimentation to study the usefulness of the proposed method. Despite the paper stating that there have been earlier work (Joseph et al, 2019 and Wang et al, 2019) that attempt mini-batch selection, the paper does not compare with them. This is limiting. Further, since the proposed method is not specific to the domain of images, evaluating it on tasks other than image classification, such as text classification for instance, would have helped validate its applicability across domains.


\- Considering the limited results, a deeper analysis of the proposed method would have been nice. The idea of a sliding window over a growing window is a generic one, and there have been many efforts to theoretically analyze active learning over the last two decades. How does the proposed method fit in there? (For e.g., how does the expected model variance change in this setting?) Some form of theoretical/analytical reasoning behind the effectiveness of recency bias (which is missing) would provide greater insights to the community and facilitate further research in this direction.


\- The claim of 20.5% reduction in test error mentioned in the abstract has not been clearly addressed and pointed out in the results section of the paper.


\- On the same note, the results are not conclusively in favor of the proposed method, and only is marginally better than the competitors. Why does online batch perform consistently than the proposed method? There is no discussion of these inferences from the results.


\- The results would have been more complete if results were shown in a setting where just recency bias is used without the use of the selection pressure parameter. In other words, an ablation study on the effect of the selection pressure parameter would have been very useful.


\- How important is the warm-up phase to the proposed method? Considering the paper states that this is required to get good estimates of the quantization index of the samples, some ablation studies on reducing/increasing the warm-up phase and showing the results would have been useful to understand this.


\- Fig 4: Why are there sharp dips periodically in all the graphs? What do these correspond to?


\- The intuition behind the method is described well, however, the proposed method would have been really solidified if it were analysed in the context of a simple machine learning problem (such as logistic regression). As an example, verifying if the chosen minibatch samples are actually close to the decision boundary of a model (even if the model is very simple) would have helped analyze the proposed method well.


Minor comments:

\* It would have been nice to see the relation between the effect of using recency bias and the difficulty of the task/dataset.

\* In the 2nd line in Introduction, it should be "deep networks" instead of "deep networks netowrks".

\* Since both tasks in the experiments are about image classification, it would be a little misleading to present them as "image classification" and "finetuning". A more informative way of titling them would be "image classification from scratch" and "image classification by finetuning".

\* In Section 3.1, in the LHS of equation 3, it would be appropriate to use P(y_i/x_i; q) instead of P(y/x_i; q) since the former term was used in the paragraph.


=====POST-REBUTTAL COMMENTS========

I thank the authors for the response and the efforts in the updated draft. Some of my queries were clarified. However, unfortunately, I still think more needs to be done to explain the consistency of the results and to study the generalizability of this work across datasets. I retain my original decision for these reasons.


<h2 id="faq" style="color:#337ab7">FAQ</h2>

**Q**: How should I use supplementary material?

**A**: It is not necessary to read supplementary material but such material can often answer questions that arise while reading the main paper, so consider looking there before asking authors.


**Q**: How should I handle a policy violation?

**A**: To flag a CoE violation related to a submission, please indicate it when submitting the CoE report for that paper. The AC will work with the PC and the ethics board to resolve the case. To discuss other violations (e.g. plagiarism, double submission, paper length, formatting, etc.), please contact either the AC or the PC as appropriate. You can do this by sending an offical comment with the appropriate readership restrictions.



**Q**: How can I contact the AC for a paper?

**A**: To contact the AC for a paper: (i) go to the OpenReview page for that paper (while being logged into OpenReview); (ii) click the button to add an official comment and fill out the comment form; (iii) add the ACs to the list of "Readers".


**Q**: Am I allowed to ask for additional experiments?

**A**: You can ask for additional experiments. New experiments should not significantly change the content of the submission. Rather, they should be limited in scope and serve to more thoroughly validate existing results from the submission.


**Q**: If a submission does not achieve state-of-the-art results, is that grounds for rejection?

**A**: No, a lack of state-of-the-art results does not by itself constitute grounds for rejection. Submissions bring value to the ICLR community when they convincingly demonstrate new, relevant, impactful knowledge. Submissions can achieve this without achieving state-of-the-art results.



**Q**: Are authors expected to cite and compare with very recent work? What about non peer-reviewed (e.g., ArXiv) papers?

**A**: We consider papers contemporaneous if they are published within the last two months. That means, since our full paper deadline is Oct 2, if a paper was published on or after Aug 2, 2020, authors are not required to compare their own work to that paper. Authors are encouraged to cite and discuss all relevant papers, but they may be excused for not knowing about papers not published in peer-reviewed conference proceedings or journals.



**Q**: How can I avoid being assigned papers that present a conflict of interest?

**A**: Conflicts of interest are detected using your OpenReview profile information (co-authors, past and current institutions, etc.). Therefore, the best way to avoid conflicts of interest is to update your OpenReview profile. If, while bidding, you come across a paper that presents a conflict of interest, please bid "Very Low" for that paper. If you are assigned a paper that presents a conflict of interest, please contact the program chairs immediately to have that paper re-assigned."""
        }
    ]
}
meta_data_acGuide={
    "menuText":"AC Guide",
    "layout":[
        {
            "name":"Markdown",
            "option":"""# ICLR 2021 Area Chair Guide
Area Chairs play a critical role in curating the technical programme for ICLR. Use this as a resource for any questions related to your role as an Area Chair. You will also find useful information in Metareview Guide, Reviewer Guide, Code of Ethics, and Code of Conduct. Please contact the Program Chairs via email (iclr2021programchairs@googlegroups.com) with any questions or comments. Thank you for your contribution!

## Timeline for ICLR 2020
- Abstract Deadline: Mon, Sept 28, 2020, 8 am PDT (5 pm in Vienna, Austria)
- Submission Deadline: Fri, Oct 2, 2020, 8 am PDT (5 pm in Vienna, Austria)
- AC Bidding: Tues, Sept 29 to Fri, Oct 2
- Check Assignments & Recommend Reviewers: Tues, Oct 6 to Thurs, Oct 8
- Check Reviewer Fit: Mon, Oct 12 to Thur, Oct 16
- Review Period: Mon, Oct 12 to Wed, Oct 28
- Substitute Reviewing Period: Thurs, Oct 29 - Mon, Nov 9
- Review Release: Tues, Nov 10
* Discussion Stage 1:  Tues, Nov 10 - Tues, Nov 17
    + Discussions among Reviewers/Authors/Public.
    + Anyone may post comments, but they must be logged in, and their names will be shown. Reviewers remain anonymous (R1, R2, etc.).
* Discussion Stage 2 - Tues, Nov 17 - Tues, Nov 24
    + Discussions among authors, reviewers and AC.
    + Comments are all anonymous.
    + ACs encourage reviewers to acknowledge and respond to author responses.

* Discussion Stage 3 - Tues, Nov 24 - Mon, Nov 30
    + Discussions among reviewers and AC.
    + Comments are all anonymous and not visible to authors.

* Meta-review Period: Mon, Nov 30 - Fri, Dec 11
    + No public comments allowed.
    + PC/AC Calibration Period: Fri, Dec 11 - Fri, Dec 18

- Decision Notification: Thurs, Jan 14, 2021
- Best Paper Selections: Subset of ACs will be asked to form a committee to select the best papers and mentions during January and February, 2021
- Conference: May 4-8, 2021


## Abstract Submission
This year, we added an abstract submission deadline. Having the abstracts a few days earlier will allow ACs to bid on the abstracts, recommend appropriate reviewers, and check the reviewer fit early in the reviewing period.

## Code of Ethics
This year, ICLR is adopting the new Code of Ethics which needs to be acknowledged and adhered to by all participants including authors and reviewers. If any submission, review, or discussion comments raise ethical concerns, please flag the problematic content and contact the Program Chairs.

## Multi-Stage Discussion
Similar to last year, the review process is designed to maximize discussions while clearly distinguishing the different stages of discussion. After the initial review period, during which each assigned reviewer is required to submit a formal review, there will be three stages of discussion.

- In the first stage (Public Discussion), anyone can post a comment on a submission. Authors may post any clarification anonymously, and the assigned reviewers and AC may post further comments. Public commentators can also participate and leave comments, but cannot do so anonymously, of which the decision was made to avoid any potential adverse behavior.

- In the second stage (Author/Reviewer/AC Discussion), the authors, assigned reviewers and AC are allowed to post their comments, while posts from the public will be blinded (they will eventually appear after the decision notifications are sent.)

- During the final review stage (Reviewer/AC Discussion) only the assigned reviewers and ACs discuss the merits of each submission. Discussions in this final stage remain private to the assigned reviewers and ACs, as well as the Program Chairs.

This design of the three-stage discussion addresses the concerns that were raised during past iterations of ICLR. First, it clearly designates a fixed period over which authors are expected to respond to the reviewers', ACs’ and public’s comments, thereby removing the burden of non-stop commitment of several months on the authors. Second, by gradually reducing the size of participants toward a core set of decision makers (assigned reviewers and ACs), we facilitate the convergence of discussion toward the final decision. Lastly, each comment on a submission is marked with the stage in which it was made. This is expected to help ACs and PCs easily identify the maturity/stage of each comment, which in turn gives us a better ability to judge the merit and significance of these comments when making the final decision.

## Additional Paper Assignments
We have substantially more Area Chairs for ICLR 2021 compared to previous years, which means your initial set of assignments is likely smaller. This is good news for all of us, as you can devote more of your time and efforts to the assigned submissions. However, we expect some conflicts and unforeseen circumstances that require us to re-assign some of the papers during the reviewing process. You can expect an additional small batch of papers to handle for discussions and metareviews starting from mid-October to mid-December. The later the re-assignment, the less time we expect you to devote to those submissions. We will, of course, ask you before these re-assignments are made.

## Your Roles and Action Items
### Reviewing Process Manager
Your first role is to help the Program Chairs manage the reviewing process for the thousands of submissions we expect to receive. When you are assigned a batch of papers to handle based on your bids on the abstracts, please recommend a set of appropriate reviewers (you may skip this, and the reviewers will be assigned based on their bids only), and when some of those reviewers are delinquent or not responsive, please help us assign alternate reviewers in a timely manner so that every submission gets a chance to be judged fairly and expertly.

- Bid on abstracts
- Recommend reviewers
- Identify delinquent reviews and assign alternate reviewers

### Decision Maker
From the moment all papers are submitted, perhaps the most important role as AC is making decisions for the ICLR program. For every submission that goes through the reviewing process, please recommend whether it should be accepted or rejected. The recommendation should be accompanied by a metareview summarizing the reviews and the three stages of discussion, optionally adding your own view of the merits and limitations of the paper. The Program Chairs will actively engage in this decision making and help with the metareviews, so please do not hesitate to contact us if you find the need to discuss any submission assigned to you.

- Flag papers for desk reject
- Watch out for reviewers’ flags for Code of Ethics violations. For all papers flagged, collect information, make an informed recommendation, and provide any evidence obtained (e.g., from the paper, discussion with author and/or reviewers). Please note the AC recommendation will be non-binding, and any of the flagged papers may be passed to the Ethics board for further review
- Write metareviews with recommendations for accept/reject

### Discussion Moderator
Each submission is considered a forum on its own, and you as an AC has full responsibility in encouraging and moderating active discussions. When a submission does not receive enough attention that it deserves or requires, you should actively engage with the assigned reviewers as well as the authors and ask for clarification or argument. You should also “moderate” discussion by discouraging the participation in any discussion that is irrelevant to scientific claims and merits of a submission.

- Encourage reviewers to respond to author rebuttals
- Moderate the discussions so that they are not toxic and focus on the scientific merits, limitations, and clarifications
- Identify any violations of Code of Ethics during the discussion phase

### Discussion Participant
We have invited you to serve as an AC because of your expertise and reputation. In other words, your assessment of a submission is a critical factor behind the entire decision-making process, and we ask you to actively participate in discussions not only as a moderator but also as a scientific expert. You are encouraged to ask authors (as well as any other commentator of the submission including assigned reviewers) for clarification. In other words, please be an active participant in discussion.

- Participate in discussions with your own view of the paper
- Ask authors for clarifications when needed to understand and judge the contributions fairly

## FAQ for ICLR 2021 Area Chairs
**Q**: How do the reviewers and ACs deal with the revisions of the paper during the discussion period?

**A**: The authors may revise their submission during the first two stages of discussion (Public Discussion Period and Author/Reviewer/AC Discussion Period,) but you reserve the right to ignore this revision if it is substantially different from the original version.

**Q**: When do we seek emergency/additional reviewers?

**A**: In two cases:

1. Assigned reviewers are unresponsive and are close to missing the deadline.

2. Additional reviews could improve the confidence in your recommendation. This is an important part of your responsibility, as we strive to provide timely feedback to the authors so that they can appropriately and fairly respond to these feedback. Especially if a review had not been submitted by the review deadline, immediately start looking for and recruiting an emergency reviewer.

**Q**: How do we assign emergency/additional reviewers?

**A**: When you find an emergency reviewer, you will be able to assign them to the paper using the links in   your AC console. If you struggle to find an emergency reviewer, please get in touch with us ([iclr2021programchairs@googlegroups.com](mailto:iclr2021programchairs@googlegroups.com)) as soon as possible.

**Q**: How do we identify and respond to potential breaches of the Code of Ethics?

**A**: All authors, reviewers, and Area Chairs must adhere to the Code of Ethics. If reviewers flag submissions, or if authors raise issues with reviewers/commenters, first carefully consider the facts of the situation, and if you find it is indeed problematic, please contact the Program Chairs.

**Q**: Are authors expected to cite and compare with very recent work? What about non peer-reviewed (e.g., ArXiv) papers?

**A**: We consider papers contemporaneous if they are published within the last two months. That means, since our full paper deadline is Oct 2, if a paper was published on or after Aug 2, 2020, authors are not required to compare their own work to that paper. Authors are encouraged to cite and discuss all relevant papers, but they may be excused for not knowing about papers not published in peer-reviewed conference proceedings or journals."""
        }
    ]
}
meta_data_metaReviewGuide={
    "menuText":"Meta Review Guide",
    "layout":[
        {
            "name":"Markdown",
            "option":"""# Meta-review Guidelines
As an AC, we trust you to make a reasonable recommendation based on reasonable bases and to clearly and thoroughly convey this recommendation and reasoning behind it to the authors. We recommend that your meta-review contain the following sections, and hasat least 100 words. You will have an AC buddy, so you should read the meta-reviews from your partner ACs and give them feedback for any cases you think could need a second opinion.

1. **A concise description of the submission’s main content** (scientific claims and findings) based on your own reading and reviewers’ characterization. Ideally this description should contain both what have been discussed in the submission and what are missing from the submission.

2. **A concise summary of discussion**. Unlike other conferences in which there is only a single round of back-and-forth between reviewers and authors, ICLR distinguishes itself by providing three weeks of discussion. These weeks of discussion not only serve the purpose of decision making but also to contribute scientifically to the submission. We thus encourage the AC to summarize the discussion in the meta-review. In particular, it is advised that the AC lists the points that were raised by the reviewers, how each of these points was addressed by the authors and whether you as the AC found each point worth consideration in decision making.

3. **Your recommendation and justification**. The meta-review should end with a clear indication of your recommendation. Your recommendation must be justified based on the content and discussion of the submission (i.e., the points you described above.)"""
        }
    ]
}
meta_data_authorGuide={
    "menuText":"Author Guide",
    "layout":[
        {
            "name":"Markdown",
            "option":"""# Author Guide
## Submission
This year we are asking authors to submit paper abstracts by the abstract submission deadline of 28 September 2020, 08:00 AM PDT (UTC-7). The full paper submission deadline is 2 October 2020, 08:00 AM PDT (UTC-7). Abstracts and papers must be submitted using the conference submission system at: [https://openreview.net/group?id=ICLR.cc/2021/Conference](https://openreview.net/group?id=ICLR.cc/2021/Conference). It is key that authors submit genuine and informative abstracts that reflect the content of the full submission, as abstracts will be used in Area Chair bidding before the final paper submission deadline. Placeholder or duplicate abstracts will be removed.

For detailed submission instructions, including paper length and style file, please refer to the call for papers on https://iclr.cc/Conferences/2021/CallForPapers.

**Source code submission**: Source code associated with a paper can be uploaded as part of the supplementary material. Code submission gives more information to reviewers, especially for replicability of the paper. We encourage all authors to submit code as part of their submission. Note that reviewers are encouraged, but not required to review supplementary material during the review process. All supplementary material must be self-contained and zipped into a single file. Note that supplementary material will be visible to reviewers and the public throughout and after the review period, and ensure all material is anonymized.

## Code of Ethics
All ICLR participants, including authors, are required to adhere to the ICLR Code of Ethics (https://iclr.cc/public/CodeOfEthics). All authors of submitted papers are required to read the Code of Ethics, adhere to it, and explicitly acknowledge this during the submission process. The Code of Ethics applies to all conference participation, including paper submission, reviewing, and paper discussion.

As part of the review process, reviewers will be encouraged to raise potential violations of the ICLR Code of Ethics. If authors feel that their paper submission raises questions regarding the Code of Ethics, they are encouraged to discuss any potential issues as part of their submission. This discussion is not counted against the maximum page limit of the paper and should be included as a separate section.

Authors who encounter potential violations of the Code of Ethics, e.g., as part of the review or public discussion, should raise these issues in a private message to their paper’s Area Chair through the open review interface.

## Reviewing Process
Submissions to ICLR are uploaded on OpenReview, which enables public discussion during the review process public discussion phase, which lasts until November 17, 2020, as well as further discussion between authors, reviewers and area chairs until November 24, 2020.

Authors are encouraged to participate in the public discussion of their paper, as well as of any other paper submitted to the conference. Submissions and reviews are both anonymous and visible as follows:

- Official reviews are anonymous and publicly visible.

- Anybody who is logged in can post comments that are publicly visible or restrict visibility to reviewers and up, ACs and up, or just PCs. Login is required before posting any comment.

By 10 November 2020, we expect all reviews to be completed. Reviews are anonymous and publicly visible in Open Review. Once the reviews are posted, authors are free to upload modifications to the paper during the two week discussion period. The most relevant dates for authors are as follows:
- Review Release: Tues, Nov 10
- Discussion Stage 1:  Tues, Nov 10 - Tues, Nov 17
    - Discussions among Reviewers/Authors/Public.
    - Anyone may post comments, but they must be logged in, and their names will be shown. Reviewers remain anonymous (R1, R2, etc.).


- Discussion Stage 2 - Tues, Nov 17 - Tues, Nov 24
    - Discussions among authors, reviewers and AC.
    - Comments are all anonymous.
    - ACs encourage reviewers to acknowledge and respond to author responses.

In addition, authors can post "official comments" about their paper throughout the review process, and restrict visibility to reviewers, area chairs, or program chairs as appropriate. For example, this functionality can be used to post links to supplementary material.

Additional details of the review process can be found in the ICLR 2021 Call for Papers, [Reviewer Guide](/event/group?id=ICLR.cc/2020/Conference/Virtual/Guides/ReviewerGuide) and [AC Guide](/event/group?id=ICLR.cc/2020/Conference/Virtual/Guides/ACGuide).

## Camera-ready Submissions
The deadline for uploading camera-ready submissions will be in March 2021. Additional guidance on preparing your camera-ready version will be provided on this page in due course.

## Frequently Asked Questions
**Q: When is the submission deadline for supplementary materials?**

The deadline is the same for the full paper and for the supplementary materials.

**Q: Should appendices/supplementary material be added as a separate PDF or in the same PDF as the main paper?**

Either is allowed, you can include the supplementary material at the end of the main pdf after the references, or you can include it as a separate file for the supplementary materials.

**Q: How can we make our code available for reviewing anonymously?**

You can share your code in three ways:

1. Anonymize your code, put it in a .zip file and submit it as supplementary materials.

2. Make an anonymous repository and put the link in your paper.

	The above methods will make your code public, along with your paper and reviews/comments for the paper.

3. After we open the discussion forums for all submitted papers, make a comment directed to the reviewers and area chairs and put a link to an anonymous repository.

This method will let you keep your code visible only to the reviewers and ACs for your paper.

**Q: I can’t modify my submission to include the PDF and supplementary materials. Can you help?**

Make sure you logged in using the same account you used to upload the submission. If so, you should be able to click on your submission and see a "Revision" button.

If you are still having problems accessing your submission, follow these steps:

1. Go to your submission and hover over your name in the ‘Authors’ field.

2. If your name is associated with an email address that is not currently on your profile, add this email address to your OpenReview profile and confirm it. This will give you access to your submission and the ‘Revision’ button.

3. If your name is associated with another profile that is not the profile you submitted the paper with, contact the OpenReview team at info@openreview.net so they can merge your profiles.

If you are still having trouble, please contact OpenReview technical support at [info@openreview.net](mailto:info@openreview.net?subject=ICLR%202021%20-%20paper%20submission) and explain the situation."""
        }
    ]
}
meta_data_workshopOrganizerGuide={
    "menuText":"Workshop Organizer Guide",
    "layout":[
        {
            "name":"Markdown",
            "option":"""### ICLR 2021 Guidance for Workshop Proposals
<small>(Document updated: Oct. 10, 2020)</small>

Saturday, May 8, 2021

Virtual Conference (formerly Vienna), AUSTRIA

ICLR Workshop Co-Chairs

- Chelsea Finn, Stanford University & Google Research
- Sanmi Koyejo, University of Illinois at Urbana-Champaign & Google Research

This is the third year that ICLR will have workshops. With the rapid growth and interest in ICLR and its associated workshops, the competition for workshops has grown. To attempt to mitigate confusion and anxiety regarding what is expected, the workshop chairs have agreed on the following guidance for proposals to hold a ICLR workshop in 2021. Organizers of workshop proposals should take care to respect every piece of guidance provided here, and to provide explicit answers to the questions implied throughout, as well as explicitly addressing the selection criteria listed below.

### Timeline
1. Workshop Application Open: Sep 11, 2020

2. Workshop Application Deadline: Nov 09, 2020

3. Workshop Acceptance Notification: Dec 11, 2020

4. Suggested Submission Date for Workshop Contributions: 26 February 2021

5. Mandatory Accept/Reject Notification Date: Mar 26, 2021

Note that the final submission date for workshop contributions is suggested, and there is a trade-off between how much time workshops give authors to submit versus reviewers to review in the period between December 11, 2020 and March 26, 2021.

Workshops that do not meet this accept/reject notification deadline will have their speaker tickets withheld.



### Selection Criteria
1. Degree to which the proposal is focused on an important and topical problem, and the degree to which it is expected that the community will find the workshop interesting, exciting, and valuable.

2. Intellectual excitement of the topic. Is it likely to break new ground, or merely reiterate tired, old debates?

3. Diversity and inclusion, in all forms. (See expectations below.)

4. Degree to which the proposed program offers opportunity for discussion.

5. Quality of proposed invited speakers (including expertise, scientific achievements and presentation ability). Workshop organizers are encouraged to confirm tentative interest from proposed invited speakers and mention this in their proposal.

6. Degree to which the organizers have offered means to engage in the workshop for those unable to attend in person.

7. Organizational experience and ability of the team.

8. Other dimensions in the expectations below not explicitly listed in these criteria.

9. Points of difference. What makes this workshop enticingly different to the ICLR workshops held previously?



### Assessment Process and Criteria
The workshop chairs will appoint a number of reviewers who will provide written assessments of the proposals against the criteria listed above. Their reports will be considered by the workshop chairs who will jointly decide upon the selected workshops (subject to the notes on COIs listed below). The final decisions will be made by the workshop chairs via consensus and judgement; we will not simply add up scores assigned to the different criteria.

**Hard Constraints/Workshop Requirements**

- Global Notification Deadline Prior to February 25, 2021: By submitting a workshop proposal, workshop organizers commit to notifying those who submit contributions (including talks and posters) to their workshop of their acceptance status before February 25, 2021 to allow time for visa acquisition. A timeline should be included in the proposal that will allow for this.  This deadline of February 25, 2021 will be published on the ICLR main web page and cannot be extended under any circumstances.

**Managing Chair and Reviewer Conflicts of Interest**

- Workshop chairs cannot be organizers nor give invited talks at any workshop, but can submit papers and give contributed talks.

- Workshop reviewers cannot review any proposal on which they are listed as an organizer or invited speaker, and may not accept invitations to speak at any workshop they have reviewed after the workshop is accepted.

- Workshop chairs and reviewers cannot review or shape acceptance decisions about workshops with organizers from within their organization. (For large corporations, this means anyone in the corporation world-wide).

**Managing Organizer Conflicts of Interest**

- Workshop organizers cannot give talks at the workshops they organize. They can give a brief introduction to the workshop and/or act as a panel moderator.

- Workshop organizers should state in their proposal how they will manage conflicts of interest in assessing submitted contributions. At a minimum, an organizer should not be involved in the assessment of a submission from someone within the same organization.

### Other Guidance and Expectations for Workshop Proposals
1. We encourage, and expect, diversity in the organizing team and speakers. This includes diversity of viewpoint and thinking regarding the topics discussed at the workshop, gender, race, affiliations, seniority, geographic location, etc. If a workshop is part of a series, the organizer list should include people who have not organized in the past. Organizers should articulate how they have addressed diversity in their proposal in each of these senses.

2. Since the goal of the workshop is to generate discussion, sufficient time and structure needs to be included in the program for this. Proposals should explicitly articulate how they will encourage broad discussion.

3. Workshop proposals should list explicitly what the problems are they would like to see solved, or at least advances made, as part of their workshop. They should explain why these are important problems and how the holding of their proposed workshop will contribute to their solution.

4. Workshops are not a venue for work that has been previously published in other conferences on machine learning. Work that is presented at the main ICLR conference should not appear in a workshop, including as part of an invited talk. Organizers should make this clear in their calls and explain in their proposal how they will discourage presentation of already published machine learning work.

5. We encourage workshop submissions of varying lengths and scopes. Organizers should state whether their workshops are meant to be large-attendance talk format, or small group presentations. Organizers should articulate what they hope to achieve from the format proposal beyond the talks listed.

6. With the extraordinary growth of ICLR, and noting the finite capacity of venues and the impossibility of accurately predicting attendance, organizers should explain how they will provide access to the content of the workshop for those who cannot attend in person. This might include recording of talks, publishing short working papers or posters on the web, having a follow-up special issue of a journal, curating and maintaining a web page with a range of content, or other ideas.

7. Workshops should allow for choice of attendance based on content. Good workshops will put talk titles up publicly prior to site publication and note the archival status of their submissions. Organizers should articulate how they will do this.

8. Organizing a workshop is a complex task, and proposals should outline the organizational experience and skills of the proposed organizers (as a team). We encourage junior researchers to be involved in workshop organization, but prefer some collective experience in organizing a complex event.



### Example Successful Proposals
With permission of the respective workshop organizers, we are providing the successful proposals of past ICLR workshops as examples: [the ICLR 2020 BeTR-RL Workshop](https://drive.google.com/file/d/1sxNAQAi-depxbd7IwyaTsCdMSajY1sme/view?usp=sharing) and [the ICLR 2020 Workshop on Neural Architecture Search](https://drive.google.com/file/d/1CIDK-3iiZTdl6M8z7d6lM-8WMjb7kPEV/view?usp=sharing).



### Frequently Asked Questions From Past Workshops
**Workshop Series**
We neither encourage nor discourage workshops on topics that have appeared before. Membership of an existing sequence of workshops is irrelevant in the assessment of a workshop proposal (it neither helps nor hinders). Workshop proposals will be evaluated solely on their merits for this year’s conference.

**Overlapping Proposals**
We will not forcibly merge proposals.  If multiple strong proposals are submitted on similar topics, we will choose a single proposal to accept. We will then reach out to the organizers of the rejected proposals to ask whether they would like us to share their proposals with the organizers of the accepted workshop. The organizers of the accepted workshop may then optionally initiate a merge.

**Where will accepted be workshops listed?**

[calendar](/event/calendar2?invitation=ICLR.cc/2020/Conference/Virtual/-/Session)

**Publicizing your workshop**

When publicizing your workshop, you may mention the hashtag #ICLR2021



 """
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

#dropdown menu groups Grides
#a group should have "menuText" to appear in menu
client.post_group(openreview.Group(id=f"{virtual_group_id}/Guides",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[
                    f"{virtual_group_id}/Guides/PresentationGuide",
                    f"{virtual_group_id}/Guides/ReviewerGuide",
                    f"{virtual_group_id}/Guides/ACGuide",
                    f"{virtual_group_id}/Guides/MetaReviewGuide",
                    f"{virtual_group_id}/Guides/AuthorGuide",
                    f"{virtual_group_id}/Guides/WorkshopOrganizerGuide"
                ],
                web_string=json.dumps(meta_data_guides)))
client.post_group(openreview.Group(id=f"{virtual_group_id}/Guides/PresentationGuide",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_presentationGuide)))
client.post_group(openreview.Group(id=f"{virtual_group_id}/Guides/ReviewerGuide",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_reviewerGuide)))
client.post_group(openreview.Group(id=f"{virtual_group_id}/Guides/ACGuide",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_acGuide)))
client.post_group(openreview.Group(id=f"{virtual_group_id}/Guides/MetaReviewGuide",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_metaReviewGuide)))
client.post_group(openreview.Group(id=f"{virtual_group_id}/Guides/AuthorGuide",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_authorGuide)))
client.post_group(openreview.Group(id=f"{virtual_group_id}/Guides/WorkshopOrganizerGuide",
                readers=['everyone'],
                writers=[conference_id],
                signatures=[conference_id],
                signatories=[],
                members=[],
                web_string=json.dumps(meta_data_workshopOrganizerGuide)))

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

def create_poster_session(day, number, start, end):
    return client.post_note(openreview.Note(
        invitation=session_invitation_id,
        readers=['everyone'],
        writers=[conference_id],
        signatures=[conference_id],
        content={
            'start': openreview.tools.datetime_millis(start),
            'end': openreview.tools.datetime_millis(end),
            'title': '{day} Session {number}'.format(day=day, number=number),
            'description': 'poster',
        }
    ))

days = ['Mon', 'Tues', 'Wed', 'Thurs']
times = [5, 8, 12, 17, 20]

sessions = {}
## make sure the first day is a monday
first_day = datetime.datetime(2020, 10, 27, 0, 0)

## create poster sessions
for i, day in enumerate(days):
    for j, time in enumerate(times):
        start = first_day + datetime.timedelta(days=i) + datetime.timedelta(hours=time)
        end = start + datetime.timedelta(hours=2)
        session = create_poster_session(day, j+1, start, end)
        sessions[session.content['title']] = session

## create qa and expo sessions
## Download the file from https://iclr.cc/virtual/schedule.json
with open('/Users/mbok/iesl/data/iclr2021/schedule.json') as f:
    data = json.load(f)
    for i,d in enumerate(data['conference']):
        for e in d['events']:
            if e['type'] != 'poster':
                time = int(e['slot'][:-1])
                if time == 330:
                    time = 3
                if e['slot'][-1] == 'p':
                    time += 12
                start = first_day + datetime.timedelta(days=i) + datetime.timedelta(hours=time)
                end = start + datetime.timedelta(hours=1)
                session = client.post_note(openreview.Note(
                    invitation=session_invitation_id,
                    readers=['everyone'],
                    writers=[conference_id],
                    signatures=[conference_id],
                    content={
                        'start': openreview.tools.datetime_millis(start),
                        'end': openreview.tools.datetime_millis(end),
                        'title': e['name'],
                        'description': e['type'],
                    }
                ))
                sessions[session.content['title']] = session


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
            'zoom_links': { 'values-regex': '.*' },
            'sessions': { 'values-regex': '.*' },
            'presentation_type': { 'value-regex': '.*' },
            'topic': { 'value-regex': '.*' },
            'title': { 'value-regex': '.*' },
            'abstract': { 'value-regex': '.*' },
            'bio': { 'value-regex': '.*' },
            'authors': { 'values-regex': '.*' },
            'authorids': { 'values-regex': '.*' }
        }
    }
))


## Download the file from https://iclr.cc/virtual/papers.json
# with open('/Users/mbok/iesl/data/iclr2021/papers_iclr_2020.json') as f:
#     data = json.load(f)
#     for e in data:
#         paper_id = e['id']
#         session_names = e['content']['session']
#         session_times = e['content']['session_times']
#         zoom_links = e['content']['session_links']
#         session_ids = []
#         for i,s in enumerate(session_names):
#             if session_times[i]:
#                 session_ids.append(sessions[s].id)
#             else:
#                 topic = session_names[i].split(':')[-1].strip()

#         presentation_1 = client.post_note(openreview.Note(
#             invitation=presentation_invitation_id,
#             original=paper_id,
#             readers=['everyone'],
#             writers=[conference_id],
#             signatures=[conference_id],
#             content={
#                 'slideslive': '38915149',
#                 'chat': 'https://rocketchat.com/paper',
#                 'zoom_links': zoom_links,
#                 'sessions': session_ids,
#                 'presentation_type': 'poster',
#                 'topic': topic
#             }
#         ))

## Speaker presentations
presentation_1 = client.post_note(openreview.Note(
    invitation=presentation_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'slideslive': '38915149',
        'chat': 'https://rocketchat.com/paper',
        'zoom_links': [],
        'sessions': [sessions['Live QA: Aisha Walcott-Bryant'].id],
        'presentation_type': 'qa',
        'title': 'AI + Africa = Global Innovation',
        'authors': ['Aisha Walcott-Bryant'],
        'authorids': ['~Aisha_Walcott-Bryant1'],
        'abstract': "Artificial Intelligence (AI) has for some time stoked the creative fires of computer scientists and researchers world-wide -- even before the so-called AI winter. After emerging from the winter, with much improved compute, vast amounts of data, and new techniques, AI has ignited our collective imaginations. We have been captivated by its promise while wary of its possible misuse in applications. AI has certainly demonstrated its enormous potential especially in fields such as healthcare. There, it has been used to support radiologists and to further precision medicine; conversely it has been used to generate photorealistic videos which distort our concept of what is real. Hence, we must thoughtfully harness AI to address the myriad of scientific and societal challenges; and open pathways to opportunities in governance, policy, and management. In this talk, I will share innovative solutions which leverage AI for global health with a focus on Africa. I will present a vision for the collaborations in hopes to inspire our community to join on this journey to transform Africa and impact the world.",
        'bio': "Dr. Aisha Walcott-Bryant is a research scientist and manager of the AI Science and Engineering team at IBM Research, Africa. She is passionate about healthcare, interactive systems, and on addressing Africa's diverse challenges.In addition, Dr. Walcott-Bryant leads a team of researchers and engineers who are working on transformational innovations in global health and development while advancing the state of the art in AI, Blockchain, and other technologies.She and her team are engaged in projects in Maternal Newborn Child Health (MNCH), Family Planning (FP), disease intervention planning, and water access and management. Her team's recent healthcare work on \"Enabling Care Continuity Using a Digital Health Wallet\" was awarded Honorable Mention at the International Conference on Health Informatics, ICHI2019.Prior to her career at IBM Research Africa, Dr. Walcott-Bryant worked in Spain. There, she took on projects in the area of Smarter Cities at Barcelona Digital and Telefonica with a focus on physical systems for social media engagement, and multi-modal trip planning and recommending. Dr. Walcott-Bryant earned her PhD in Electrical Engineering and Computer Science at MIT where she conducted research on mobile robot navigation in dynamic environments at their Computer Science and Artificial Intelligence Lab (CSAIL)."
    }
))

presentation_1 = client.post_note(openreview.Note(
    invitation=presentation_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'slideslive': '38915149',
        'chat': 'https://rocketchat.com/paper',
        'zoom_links': [],
        'sessions': [sessions['Live QA: Leslie Kaebling'].id],
        'presentation_type': 'qa',
        'title': 'Doing for Our Robots What Nature Did For Us',
        'authors': ['Leslie Kaelbling'],
        'authorids': ['~Leslie_Pack_Kaelbling1'],
        'abstract': "Artificial Intelligence (AI) has for some time stoked the creative fires of computer scientists and researchers world-wide -- even before the so-called AI winter. After emerging from the winter, with much improved compute, vast amounts of data, and new techniques, AI has ignited our collective imaginations. We have been captivated by its promise while wary of its possible misuse in applications. AI has certainly demonstrated its enormous potential especially in fields such as healthcare. There, it has been used to support radiologists and to further precision medicine; conversely it has been used to generate photorealistic videos which distort our concept of what is real. Hence, we must thoughtfully harness AI to address the myriad of scientific and societal challenges; and open pathways to opportunities in governance, policy, and management. In this talk, I will share innovative solutions which leverage AI for global health with a focus on Africa. I will present a vision for the collaborations in hopes to inspire our community to join on this journey to transform Africa and impact the world.",
        'bio': "Dr. Aisha Walcott-Bryant is a research scientist and manager of the AI Science and Engineering team at IBM Research, Africa. She is passionate about healthcare, interactive systems, and on addressing Africa's diverse challenges.In addition, Dr. Walcott-Bryant leads a team of researchers and engineers who are working on transformational innovations in global health and development while advancing the state of the art in AI, Blockchain, and other technologies.She and her team are engaged in projects in Maternal Newborn Child Health (MNCH), Family Planning (FP), disease intervention planning, and water access and management. Her team's recent healthcare work on “Enabling Care Continuity Using a Digital Health Wallet” was awarded Honorable Mention at the International Conference on Health Informatics, ICHI2019.Prior to her career at IBM Research Africa, Dr. Walcott-Bryant worked in Spain. There, she took on projects in the area of Smarter Cities at Barcelona Digital and Telefonica with a focus on physical systems for social media engagement, and multi-modal trip planning and recommending. Dr. Walcott-Bryant earned her PhD in Electrical Engineering and Computer Science at MIT where she conducted research on mobile robot navigation in dynamic environments at their Computer Science and Artificial Intelligence Lab (CSAIL)."
    }
))

presentation_1 = client.post_note(openreview.Note(
    invitation=presentation_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'slideslive': '38915149',
        'chat': 'https://rocketchat.com/paper',
        'zoom_links': [],
        'sessions': [sessions['Live QA: Leslie Kaebling'].id],
        'presentation_type': 'qa',
        'title': 'Doing for Our Robots What Nature Did For Us',
        'authors': ['Leslie Kaelbling'],
        'authorids': ['~Leslie_Pack_Kaelbling1'],
        'abstract': "We, as robot engineers, have to think hard about our role in the design of robots and how it interacts with learning, both in 'the factory' (that is, at engineering time) and in 'the wild' (that is, when the robot is delivered to a customer). I will share some general thoughts about the strategies for robot design and then talk in detail about some work I have been involved in, both in the design of an overall architecture for an intelligent robot and in strategies for learning to integrate new skills into the repertoire of an already competent robot.",
        'bio': "Leslie Pack Kaelbling is the Panasonic Professor of Computer Science and Engineering at the Computer Science and Artificial Intelligence Laboratory (CSAIL) at the Massachusetts Institute of Technology. She has made research contributions to decision-making under uncertainty, learning, and sensing with applications to robotics, with a particular focus on reinforcement learning and planning in partially observable domains. She holds an A.B in Philosophy and a Ph.D. in Computer Science from Stanford University, and has had research positions at SRI International and Teleos Research and a faculty position at Brown University. She is the recipient of the US National Science Foundation Presidential Faculty Fellowship, the IJCAI Computers and Thought Award, and several teaching prizes; she has been elected a fellow of the AAAI. She was the founder and editor-in-chief of the Journal of Machine Learning Research."
    }
))

presentation_1 = client.post_note(openreview.Note(
    invitation=presentation_invitation_id,
    readers=['everyone'],
    writers=[conference_id],
    signatures=[conference_id],
    content={
        'slideslive': '38915149',
        'chat': 'https://rocketchat.com/paper',
        'zoom_links': [],
        'sessions': [sessions['Live QA: Leslie Kaebling'].id],
        'presentation_type': 'qa',
        'title': '2020 Vision: Reimagining the Default Settings of Technology & Society',
        'authors': ['Ruha Benjamin'],
        'authorids': [],
        'abstract': "From everyday apps to complex algorithms, technology has the potential to hide, speed, and even deepen discrimination, while appearing neutral and even benevolent when compared to racist practices of a previous era. In this talk, I explore a range of discriminatory designs that encode inequity: by explicitly amplifying racial hierarchies, by ignoring but thereby replicating social divisions, or by aiming to fix racial bias but ultimately doing quite the opposite. This presentation takes us into the world of biased bots, altruistic algorithms, and their many entanglements, and provides conceptual tools to decode tech promises with sociologically informed skepticism. In doing so, it challenges us to question not only the technologies we are sold, but also the ones we manufacture ourselves.",
        'bio': "Dr. Ruha Benjamin is Associate Professor of African American Studies at Princeton University, founder of the JUST DATA Lab, and author of People’s Science: Bodies and Rights on the Stem Cell Frontier (2013) and Race After Technology: Abolitionist Tools for the New Jim Code (2019) among other publications. Her work investigates the social dimensions of science, medicine, and technology with a focus on the relationship between innovation and inequity, health and justice, knowledge and power. Professor Benjamin is the recipient of numerous awards and fellowships including from the American Council of Learned Societies, National Science Foundation, Institute for Advanced Study, and the President’s Award for Distinguished Teaching at Princeton. For more info visit www.ruhabenjamin.com"
    }
))