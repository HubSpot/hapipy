## What is it?

hapipy is a Python wrapper for the HubSpot APIs.  You can find more information about HubSpot's APIs here: [[http://docs.hubapi.com]].  The hapipy wrapper is meant to make it easier for external developers to use the HubSpot APIs by giving easy access to data that gets returned to you after an API call gets made.

The following documentation will describe the different calls that you can make via the hapipy wrapper and includes some sample code for how to make these calls and deal with the responses.  Please keep in mind that we'll be working hard to improve and add to this wrapper as we add to and iterate on our APIs so if a method that you're looking for isn't here today, please check back soon!

## Description of Wrapper Files

The base hapi.py includes all of the methods that you can call to use the wrapper. As I mentioned above, we're in progress with this and will continue to develop out different methods for all of our APIs going forward.  The other files to note are  the objects files which include all of the classes and define the data that you can access with each call you make.  For the leads methods please refer to "lead_objects.py", for blog please refer to "blog_objects.py", for lead nurturing...well you get the idea.

### PyCurl Dependency

A few API methods require using PyCURL in order to make parallel API calls.  On OSX and Linux machines, PyCURL can be installed via pip (run "pip install pycurl" ).  For windows machines, pre-compiled PyCURL binaries can be downloaded [here for python 2.6 and 2.7](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl), and [and here for python 2.5](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl).

## Notes on Authentication and API Options

The HubSpot APIs enable you to use OAuth for authentication, as well as the old API key system (hapikey).  We've also setup a couple of files that will help you specify these authentication options: 'test/helper.py' and 'test/test_credentials_sample.json'.  The 'helper.py' file contains a method that will get the options from the JSON file mentioned above.  You can also set the options in this file, as you can see we've done on line 8 of this file.

If you're using use API keys, then just keep the file as is currently, replacing the 'demo' API key with your user's key and you're all set.  If you're using OAuth, then you need to make sure you provide a valid OAuth Access Token at the least, and if you're making offline API calls (while the user isn't in the Marketplace), you'll want to provide a valid refresh token and client ID as well.  You can read all about how to get these pieces of data here: [http://developers.hubspot.com/auth/oauth_apps](http://developers.hubspot.com/auth/oauth_apps). Of course, you should feel free to ask us any questions here: http://developers.hubspot.com/forum

## Description of Methods and Example Implementation

### hapipy Leads Methods

Please see http://developers.hubspot.com/docs/endpoints#leads-api for the main Blog API documentation.  Then read the [blog API client](https://github.com/HubSpot/hapipy/blob/master/hapi/leads.py) and [unit tests](https://github.com/HubSpot/hapipy/blob/master/hapi/test/test_leads.py) to see code examples.

### hapipy Lead Nurturing Methods

Please see http://developers.hubspot.com/docs/endpoints#nurture-api for the main Blog API documentation.  Then read the [blog API client](https://github.com/HubSpot/hapipy/blob/master/hapi/nurturing.py) and [unit tests](https://github.com/HubSpot/hapipy/blob/master/hapi/test/test_nurturing.py) to see code examples.

### hapipy Blog Methods

Please see http://developers.hubspot.com/docs/endpoints#blog-api for the main Blog API documentation.  Then read the [blog API client](https://github.com/HubSpot/hapipy/blob/master/hapi/blog.py) and [unit tests](https://github.com/HubSpot/hapipy/blob/master/hapi/test/test_blog.py) to see code examples.

### hapipy Prospects Methods

Please see http://developers.hubspot.com/docs/endpoints#prospects-api for the main Prospects API documentation.  Then read the [prospects API client](https://github.com/HubSpot/hapipy/blob/master/hapi/prospects.py) and [unit tests](https://github.com/HubSpot/hapipy/blob/master/hapi/test/test_prospects.py) to see code examples.

### hapipy Settings Methods

Please see http://developers.hubspot.com/docs/endpoints#settings-api for the main Settings API documentation.  Then read the [prospects API client](https://github.com/HubSpot/hapipy/blob/master/hapi/settings.py) and [unit tests](https://github.com/HubSpot/hapipy/blob/master/hapi/test/test_settings.py) to see code examples.