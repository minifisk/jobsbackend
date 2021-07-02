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

## Usage
The following section describes how to set up the application on your local machine after cloning the repo.

### AWS
Before being able to run the application you need to set up the needed resoruces on AWS. AWS has a free tier (https://aws.amazon.com/free/) where you can set up an account for free to be used for 1 year.

#### S3-Bucket
After created an account, set up an S3 bucket, note the name of your bucket and the region your bucket is located in. Then use the following settings for the permissions of your bucket:

##### Public access
Block public access to buckets and objects granted through new access control lists (ACLs)
 Off
Block public access to buckets and objects granted through any access control lists (ACLs)
 Off
Block public access to buckets and objects granted through new public bucket or access point policies
 On
Block public and cross-account access to buckets and objects through any public bucket or access point policies
 On
 
 ##### Cross-origin resource sharing (CORS)
 Note that you should change "Allowed origins" to your website origin later on for increased security.
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "HEAD",
            "POST",
            "PUT"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]

#### IAM permissions
You need to set up an IAM account for your bucket, which you will use in the application for uploading files to the bucket with.

Create an IAM account with the following permissions, attached directly to your created S3 bucket:

S3-permissions:
* GetObject
* PutObject
* ListAllMyBuckets (optional if you want to test the IAM users access)
* PutObjectAcl

Take note of the Access Key and Security Key for the user (you will only see them once), you will have to provide them when setting up the application.

### Setting up the .env file
In the repo is included an ".env.example" file, this contain the needed lines for setting up your own .env file. Remove the ".example" ending so it's just named ".env" and start filling out the credentials for your project.

#### Secret Key
This is a secret key that Django use for internal operations, you can generate yourself a secure key here: https://djecrety.ir/

#### Database engine
You need to set up a postgres database, which is the database of choice for this application. When you have set this up, fill in the credentials.

#### Bucket name and region
Here you fill out the name of your bucket and the region

#### Email backend
This project use a "dummy" email backend - meaning that all mails that go out are stored in a "fake inbox" and don't go out to the actual recipient, which is good for testing an application out. You can create a dummy email-backend over here for free https://mailtrap.io/ - check out their tutorials on how to get your credentials and then fill these out in your .env file.





