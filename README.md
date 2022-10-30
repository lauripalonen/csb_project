# Cyber Security Base Project
This is a project done for University of Helsinki's [Cyber Security course](https://cybersecuritybase.mooc.fi/). Task was to introduce five cyber security flaws in a web application. Application was created by following the tutorial of [Writing your first Django app](https://docs.djangoproject.com/en/3.1/intro/tutorial01/).

# Installation
This application requires Python 3 and Django. Installation instructions can be found here: https://cybersecuritybase.mooc.fi/installation-guide  

To run the application, run command `python3 manage.py runserver` in the `csb_project/csbproject/` directory. By default the application runs in http://127.0.0.1:8000.

# Security flaws

[Flaw 1: Cross Site Request Forgery](#flaw-1--cross-site-request-forgery)  
[Flaw 2: Identification and Authentication Failures](#flaw-2-identification-and-authentication-failures)  
[Flaw 3: Injection](#flaw-3-injection)  
[Flaw 4: Security Misconfiguration](#flaw-4-security-misconfiguration)  
[Flaw 5: Broken Access Control](#flaw-5-broken-access-control)

## Flaw 1:  Cross Site Request Forgery
https://github.com/lauripalonen/csb_project/blob/45d8a68af7031d4384131aa28dfee8eca6813422/csbproject/polls/views.py#L49
  
  
**Description:**  
The application has enabled a CSRF exempt for the requests considering the voting. This disables the CSRF token validation for the vote requests. An adversary can disquise a vote request (for example) as a tempting link or a 0x0px fake image, and lure an authenticated user to launch the request. Without the CSRF token validation our website accepts the malign request and the adversary can make a vote as the authenticated user once the user clicks the link or “opens” the image.
  
  
**How to fix:**  
Remove CSRF_exempt decorators and ensure that csrf_tokens ({% csrf_token %}) are used throughout the whole application in the template files that introduce POST requests. Modern frameworks tend to handle CSRF attacks well, and to enable this security risk in our application we had to specifically allow the CSRF exempt.
  
## Flaw 2: Identification and Authentication Failures
https://github.com/lauripalonen/csb_project/blob/45d8a68af7031d4384131aa28dfee8eca6813422/csbproject/usermgmt/views.py#L12 
https://github.com/lauripalonen/csb_project/blob/45d8a68af7031d4384131aa28dfee8eca6813422/csbproject/usermgmt/views.py#L38
  
**Description:**  
The application uses a custom User model that introduces several faults. Firstly, the application has no password validation, which means that user can register with a weak password, making it easy to figure out with bruteforce methods. Secondly, the passwords are store as plaintext in the database, which means that in case it gets compromised, all the passwords are leaked as is, making it trivial for an adversary to exploit them.  

**How to fix:**  
 Use Django's built in authentication utilities. Django has its own User model, which by default encrypts the passwords, so they are never stored in the database as plaintext. The password validation can be handled with Django’s validate_password() function. Django has a few default validation options for the passwords and they can be extended further with custom validations if needed. Validators can be found in the settings.py file under the variable AUTH_PASSWORD_VALIDATORS. For code fixes, see:
https://github.com/lauripalonen/csb_project/blob/45d8a68af7031d4384131aa28dfee8eca6813422/csbproject/usermgmt/views.py#L51

## Flaw 3: Injection 
https://github.com/lauripalonen/csb_project/blob/45d8a68af7031d4384131aa28dfee8eca6813422/csbproject/usermgmt/views.py#L31

**Description:**  
 The application accepts a user input without sanitation, which is then used in a SQL query. This enables SQL injection attacks, in which an adversary can freely read and manipulate the database. In this case the adversary can attempt to login with username that includes SQL queries, and tamper the database that way. With right queries, they can for example wipe out the user database.  
 
**How to fix:**  
 In this case the vulnerability can be prevented by using Django's built in User model and authentication utilities, avoiding the use of raw sql queries in whole. However, if for some reason the custom User model is required, injections can be prevented with parameterized statements, either by using Django's ORM function: User.objects.get(username=username) or using following parameterized query format: User.objects.raw("SELECT * FROM usermgmt_user WHERE username = %s", [username]).  
 

## Flaw 4: Security Misconfiguration
See commit https://github.com/lauripalonen/csb_project/commit/f3e724ff47c69420552e5fa23a4f295d8230d710  

**Description:**  
The application developer accidentally leaked a secret production token. This vulnerability was then patched by hiding the key as an environment variable. However, the developer did not update the key. This introduces two problems; firstly, someone might have snatched the key in the timeframe between the exposure and patch. Secondly. and more importantly, version control platforms like Github keep track on previous versions, leaving the unpatched version visible to the project history. Without updating the key (and keeping it secret), anyone can use the key exposed in the history, and potentially tamper the production version of the application.  

  
**How to fix:**  
Revoke the leaked token and generate a new one. Use environment variable middleware to handle secret keys and tokens. Ensure that the file containing the secrets is ignored in the version control system. These steps were already done in the application’s latest version, expect for the token regeneration.  


## Flaw 5: Broken Access Control
https://github.com/lauripalonen/csb_project/blob/45d8a68af7031d4384131aa28dfee8eca6813422/csbproject/polls/views.py#L38  

**Description:**  
On polls page, there is a link that leads to another page which is intended to be only for registered users. However there is no access control present and it is assumed that users navigate to polls page always through login. By browsing directely to the restricted access page's url, an adversary can get access to the page without logging in.  

  
**How to fix:**  
Introduce access control. Depending on the framework that is in use, the access control can be handled in various ways. Django has built in @login_required decorator that prevents access to a view if user has not logged in. This also requires using Django's own user model, and login functions in the login view. Regardless the framework, one should not assume that user always follows the expected path when navigating on a website. Users can get quite creative and try to reach different parts of website directly by entering different urls or tampering with the query parameters.




