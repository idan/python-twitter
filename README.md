#Python Twitter#

_A python wrapper around the Twitter API_

Author: `DeWitt Clinton <dewitt@google.com>`
Github fork: `Idan Gazit <idan@pixane.net>`

##Introduction##

This library provides a pure python interface for the Twitter API.

Twitter (http://twitter.com) provides a service that allows people to
connect via the web, IM, and SMS.  Twitter exposes a web services API 
(http://twitter.com/help/api) and this library is intended to make
it even easier for python programmers to use. 

  
##Building##

###From source:###

Install the dependencies:

http://cheeseshop.python.org/pypi/simplejson

Download the latest python-twitter library from:

http://github.com/idangazit/python-twitter

Untar the source distribution and run:

    $ python setup.py build
    $ python setup.py install

###Testing###

With setuptools installed:

    $ python setup.py test

Without setuptools installed:

    $ python twitter_test.py

##Getting the code##

View the trunk at:

http://github.com/idangazit/python-twitter/tree/master

Check out the latest development version anonymously with:

    $ git clone git://github.com/idangazit/python-twitter.git

##Documentation##

The API documentation is included in the `doc` directory, in the form of
`twitterapi.html`.

##Using##

The library provides a python wrapper around the Twitter API and
the twitter data model.

*Model:*

The three model classes are twitterapi.Status, twitterapi.User, and
twitterapi.DirectMessage.  The API methods return instances of these
classes.

To read the full API for twitterapi.Status, twitterapi.User, or
twitterapi.DirectMessage, run:

    $ pydoc twitterapi.Status
    $ pydoc twitterapi.User
    $ pydoc twitterapi.DirectMessage

*API:*

The API is exposed via the twitterapi.Api class.

To create an instance of the twitterapi.Api class:

    >>> import twitterapi
    >>> api = twitterapi.Api()

To create an instance of the twitterapi.Api with login credentials (many API
calls required the client to be authenticated):

    >>> api = twitterapi.Api(username='username', password='password) 

To fetch the most recently posted public twitter status messages:

    >>> statuses = api.GetPublicTimeline()
    >>> print [s.user.name for s in statuses]
    [u'DeWitt', u'Kesuke Miyagi', u'ev', u'Buzz Andersen', u'Biz Stone'] 

To fetch a single user's public status messages, where "user" is either
a Twitter "short name" or their user id.

    >>> statuses = api.GetUserTimeline(user)
    >>> print [s.text for s in statuses]

To fetch a list a user's friends (requires authentication):

    >>> users = api.GetFriends()
    >>> print [u.name for u in users]

To post a twitter status message (requires authentication):

    >>> status = api.PostUpdate(username, password, 'I love python-twitter!')
    >>> print status.text
    I love python-twitter!

There are many more API methods, to read the full API documentation:

    $ pydoc twitterapi.Api

##Todo##
 
Patches and bug reports are welcome, just please keep the style
consistent with the original source.

Add more example scripts.

The twitterapi.Status and twitterapi.User classes are going to be hard
to keep in sync with the API if the API changes.  More of the 
code could probably be written with introspection.

Statement coverage of twitter_test is only about 80% of twitterapi.py.

The twitterapi.Status and twitterapi.User classes could perform more validation
on the property setters.

##More Information##

Please visit http://groups.google.com/group/python-twitter for more discussion.

##Contributors##

Additional thanks to Pierre-Jean Coudert, Omar Kilani, Jodok Batlogg, edleaf,glen.tregoning, and the rest of the python-twitter mailing list.

##License##

    Copyright 2007 Google Inc. All Rights Reserved.
    
    Licensed under the Apache License, Version 2.0 (the 'License');
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an 'AS IS' BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
