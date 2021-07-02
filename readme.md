# Job postings web application
This is a web application aimed at providing a platform for job-applicants and employers to connect with each others and fill job vacancies. 

Last update: 2021-07-02

## Main functionalities:

* At the home directory ("/") a user can search for jobs postings, not limited if the user is logged in or not. The search results are made on the title of the posting (e.g. "Consultant company looking for web developer" as well as the job-title of the vacancy (e.g. "Web Developer" 
* If the user clicks on a posting it will take them to the page for submitting an application to the chosen posting. Here the user will have to enter their email, upload their CV (in PDF-format) and write a cover letter for their application. The CV is instantaneously uploaded to an Amazon S3-bucket that the developer have set up in the settings of the project (more about how to set this up below), furthermore each CV is given an unique id (UUID v.4) when uploaded to the S3-bucket to prevent duplicates in the storage area. After the file is uploaded, a corresponding link to the file is attached to each applicants application.
* If there isn't any account connected to the email that the applicant has provided in their application, an account will automaticly be created. The applicant will then receive an email with instructions on how to set up a password for their account to be able to log-in. If there already is an account connected to the email provided, the application is simply connected to this account.
* A logged-in user can access their "profile page" where they can see all the applications they have applied to, with a summary of the job-posting as well as the related files to their application.
* A user can naturally access a log-in page to access their account, coupled with a "recover password" link in case the user have forgotten their password. A user can also log-out if they are already logged in.

### Browsable API-access

* The web application is coupled with a browsable api to be used by a developer to overview the current database-entries and make additional entries. At this point, the API is not password protected but is publicly available, which will be restricted in forthcoming versions of the application.
* The available end-points are the following:
1. /postings - See all current postings
2. /applicants - See all current applicants
3. /employers - See all current employers
4. /applications - See all current applications

### Planned additional functionalities:
* A page for employers to create job-postings

## Technologies used
* The app us built with Django and Django-rest-framework on the back-end and using Django-templates to generate the user views.
* The app is planned to be migrated on the front-end to use Next JS.
