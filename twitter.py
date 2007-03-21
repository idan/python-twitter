#!/usr/bin/python
#
# Copyright 2007 Google Inc. All Rights Reserved.

'''A library that provides a python interface to the Twitter API'''

__author__ = 'dewitt@google.com'
__version__ = '0.2'


import md5
import os
import simplejson
import tempfile
import time
import urllib
import urllib2
import urlparse
import twitter

class TwitterError(Exception):
  '''Base class for Twitter errors'''


class Status(object):
  '''A class representing the Status structure used by the twitter API.

  The Status structure exposes the following properties:

    status.created_at
    status.created_at_in_seconds # read only
    status.id
    status.text
    status.relative_created_at # read only
    status.user
  '''
  def __init__(self,
               created_at=None,
               id=None,
               text=None,
               user=None,
               now=None):
    '''An object to hold a Twitter status message.

    This class is normally instantiated by the twitter.Api class and
    returned in a sequence.

    Note: Dates are posted in the form "Sat Jan 27 04:17:38 +0000 2007"

    Args:
      created_at: The time this status message was posted
      id: The unique id of this status message
      text: The text of this status message
      relative_created_at:
        A human readable string representing the posting time
      user:
        A twitter.User instance representing the person posting the message
      now:
        The current time, if the client choses to set it.  Defaults to the
        wall clock time.
    '''
    self.created_at = created_at
    self.id = id
    self.text = text
    self.user = user
    if now:
      self.now = now
    else:
      self.now = time.localtime()

  def GetCreatedAt(self):
    '''Get the time this status message was posted.

    Returns:
      The time this status message was posted
    '''
    return self._created_at

  def SetCreatedAt(self, created_at):
    '''Set the time this status message was posted.

    Args:
      created_at: The time this status message was created
    '''
    self._created_at = created_at

  created_at = property(GetCreatedAt, SetCreatedAt,
                        doc='The time this status message was posted.')

  def GetCreatedAtInSeconds(self):
    '''Get the time this status message was posted, in seconds since the epoch.

    Returns:
      The time this status message was posted, in seconds since the epoch.
    '''
    return #

  created_at_in_seconds = property(GetCreatedAtInSeconds,
                                   doc="The time this status message was "
                                       "posted, in seconds since the epoch")

  def GetId(self):
    '''Get the unique id of this status message.

    Returns:
      The unique id of this status message
    '''
    return self._id

  def SetId(self, id):
    '''Set the unique id of this status message.

    Args:
      id: The unique id of this status message
    '''
    self._id = id

  id = property(GetId, SetId,
                doc='The unique id of this status message.')

  def GetText(self):
    '''Get the text of this status message.

    Returns:
      The text of this status message.
    '''
    return self._text

  def SetText(self, text):
    '''Set the text of this status message.

    Args:
      text: The text of this status message
    '''
    self._text = text

  text = property(GetText, SetText,
                  doc='The text of this status message')

  def GetRelativeCreatedAt(self):
    '''Get a human redable string representing the posting time

    Returns:
      A human readable string representing the posting time
    '''
    # Thanks to bear
    parsed = mktime(strptime(self.created_at, '%a %b %d %H:%M:%S %Z %Y'))
    delta  = this.now - parsed

    if delta < 60:
      return 'less than a minute ago'
    elif delta < 120:
      return 'about a minute ago'
    elif delta < _partialMinute:
      return '%d minutes ago' % (delta / 60)
    elif delta < _partialHour:
      return 'about an hour ago'
    elif delta < _fullDay:
      return 'about %d hours ago' % (delta / 3600)
    elif delta < _twoDays:
      return '1 day ago'
    else:
      return '%d days ago' % (delta / 86400)

  def GetUser(self):
    '''Get a twitter.User reprenting the entity posting this status message.

    Returns:
      A twitter.User reprenting the entity posting this status message
    '''
    return self._user

  def SetUser(self, user):
    '''Set a twitter.User reprenting the entity posting this status message.

    Args:
      user: A twitter.User reprenting the entity posting this status message
    '''
    self._user = user

  user = property(GetUser, SetUser,
                  doc='A twitter.User reprenting the entity posting this '
                      'status message')

  def __ne__(self, other):
    return not self.__eq__(other)

  def __eq__(self, other):
    try:
      return other and \
             self.created_at == other.created_at and \
             self.id == other.id and \
             self.text == other.text and \
             self.user == other.user
    except AttributeError:
      return False

  def __str__(self):
    '''A string representation of this twitter.Status instance.

    The return value is the same as the JSON string representation.

    Returns:
      A string representation of this twitter.Status instance.
    '''
    return self.AsJsonString()

  def AsJsonString(self):
    '''A JSON string representation of this twitter.Status instance.

    Returns:
      A JSON string representation of this twitter.Status instance
   '''
    return simplejson.dumps(self.AsDict(), sort_keys=True)

  def AsDict(self):
    '''A dict representation of this twitter.Status instance.

    The return value uses the same key names as the JSON representation.

    Return:
      A dict representing this twitter.Status instance
    '''
    data = {}
    if self.created_at:
      data['created_at'] = self.created_at
    if self.id:
      data['id'] = self.id
    if self.text:
      data['text'] = self.text
    if self.created_at: # required to calculate relative_created_at
      data['relative_created_at'] = self.relative_created_at
    if self.user:
      data['user'] = self.user.AsDict()
    return data

  @staticmethod
  def NewFromJsonDict(data):
    '''Create a new instance based on a JSON dict.

    Args:
      data: A JSON dict, as converted from the JSON in the twitter API
    Returns:
      A twitter.Status instance
    '''
    if 'user' in data:
      user = User.NewFromJsonDict(data['user'])
    else:
      user = None
    return Status(created_at=data.get('created_at', None),
                  id=data.get('id', None),
                  text=data.get('text', None),
                  relative_created_at=data.get('relative_created_at', None),
                  user=user)


class User(object):
  '''A class representing the User structure used by the twitter API.

  The User structure exposes the following properties:

    user.id
    user.name
    user.screen_name
    user.location
    user.description
    user.profile_image_url
    user.url
    user.status
  '''
  def __init__(self,
               id=None,
               name=None,
               screen_name=None,
               location=None,
               description=None,
               profile_image_url=None,
               url=None,
               status=None):
    self.id = id
    self.name = name
    self.screen_name = screen_name
    self.location = location
    self.description = description
    self.profile_image_url = profile_image_url
    self.url = url
    self.status = status


  def GetId(self):
    '''Get the unique id of this user.

    Returns:
      The unique id of this user
    '''
    return self._id

  def SetId(self, id):
    '''Set the unique id of this user.

    Args:
      id: The unique id of this user.
    '''
    self._id = id

  id = property(GetId, SetId,
                doc='The unique id of this user.')

  def GetName(self):
    '''Get the real name of this user.

    Returns:
      The real name of this user
    '''
    return self._name

  def SetName(self, name):
    '''Set the real name of this user.

    Args:
      name: The real name of this user
    '''
    self._name = name

  name = property(GetName, SetName,
                  doc='The real name of this user.')

  def GetScreenName(self):
    '''Get the short username of this user.

    Returns:
      The short username of this user
    '''
    return self._screen_name

  def SetScreenName(self, screen_name):
    '''Set the short username of this user.

    Args:
      screen_name: the short username of this user
    '''
    self._screen_name = screen_name

  screen_name = property(GetScreenName, SetScreenName,
                         doc='The short username of this user.')

  def GetLocation(self):
    '''Get the geographic location of this user.

    Returns:
      The geographic location of this user
    '''
    return self._location

  def SetLocation(self, location):
    '''Set the geographic location of this user.

    Args:
      location: The geographic location of this user
    '''
    self._location = location

  location = property(GetLocation, SetLocation,
                      doc='The geographic location of this user.')

  def GetDescription(self):
    '''Get the short text description of this user.

    Returns:
      The short text description of this user
    '''
    return self._description

  def SetDescription(self, description):
    '''Set the short text description of this user.

    Args:
      description: The short text description of this user
    '''
    self._description = description

  description = property(GetDescription, SetDescription,
                         doc='The short text description of this user.')

  def GetUrl(self):
    '''Get the homepage url of this user.

    Returns:
      The homepage url of this user
    '''
    return self._url

  def SetUrl(self, url):
    '''Set the homepage url of this user.

    Args:
      url: The homepage url of this user
    '''
    self._url = url

  url = property(GetUrl, SetUrl,
                 doc='The homepage url of this user.')

  def GetProfileImageUrl(self):
    '''Get the url of the thumbnail of this user.

    Returns:
      The url of the thumbnail of this user
    '''
    return self._profile_image_url

  def SetProfileImageUrl(self, profile_image_url):
    '''Set the url of the thumbnail of this user.

    Args:
      profile_image_url: The url of the thumbnail of this user
    '''
    self._profile_image_url = profile_image_url

  profile_image_url= property(GetProfileImageUrl, SetProfileImageUrl,
                              doc='The url of the thumbnail of this user.')


  def GetStatus(self):
    '''Get the latest twitter.Status of this user.

    Returns:
      The latest twitter.Status of this user
    '''
    return self._status

  def SetStatus(self, status):
    '''Set the latest twitter.Status of this user.

    Args:
      status: The latest twitter.Status of this user
    '''
    self._status = status

  status = property(GetStatus, SetStatus,
                  doc='The latest twitter.Status of this user.')

  def __ne__(self, other):
    return not self.__eq__(other)

  def __eq__(self, other):
    try:
      return other and \
             self.id == other.id and \
             self.name == other.name and \
             self.screen_name == other.screen_name and \
             self.location == other.location and \
             self.description == other.description and \
             self.profile_image_url == other.profile_image_url and \
             self.url == other.url and \
             self.status == other.status
    except AttributeError:
      return False

  def __str__(self):
    '''A string representation of this twitter.User instance.

    The return value is the same as the JSON string representation.

    Returns:
      A string representation of this twitter.User instance.
    '''
    return self.AsJsonString()

  def AsJsonString(self):
    '''A JSON string representation of this twitter.User instance.

    Returns:
      A JSON string representation of this twitter.User instance
   '''
    return simplejson.dumps(self.AsDict(), sort_keys=True)

  def AsDict(self):
    '''A dict representation of this twitter.User instance.

    The return value uses the same key names as the JSON representation.

    Return:
      A dict representing this twitter.User instance
    '''
    data = {}
    if self.id:
      data['id'] = self.id
    if self.name:
      data['name'] = self.name
    if self.screen_name:
      data['screen_name'] = self.screen_name
    if self.location:
      data['location'] = self.location
    if self.description:
      data['description'] = self.description
    if self.profile_image_url:
      data['profile_image_url'] = self.profile_image_url
    if self.url:
      data['url'] = self.url
    if self.status:
      data['status'] = self.status.AsDict()
    return data

  @staticmethod
  def NewFromJsonDict(data):
    '''Create a new instance based on a JSON dict.

    Args:
      data: A JSON dict, as converted from the JSON in the twitter API
    Returns:
      A twitter.User instance
    '''
    if 'status' in data:
      status = Status.NewFromJsonDict(data['status'])
    else:
      status = None
    return User(id=data.get('id', None),
                name=data.get('name', None),
                screen_name=data.get('screen_name', None),
                location=data.get('location', None),
                description=data.get('description', None),
                profile_image_url=data.get('profile_image_url', None),
                url=data.get('url', None),
                status=status)


class Api(object):
  '''A python interface into the Twitter API

  By default, the Api caches results for 1 minute.

  Example usage:

    To create an instance of the twitter.Api class:

      >>> import twitter
      >>> api = twitter.Api()

    To fetch the most recently posted public twitter status messages:

      >>> statuses = api.GetPublicTimeline()
      >>> print [s.user.name for s in statuses]
      [u'DeWitt', u'Kesuke Miyagi', u'ev', u'Buzz Andersen', u'Biz Stone'] #...

    To fetch a single user's public status messages:

      >>> statuses = api.GetUserTimeline(id)
      >>> print [s.text for s in statuses]

    To fetch a list a user's friends:

      >>> users = api.GetFriends(username, password)
      >>> print [u.name for u in users]

    To post a twitter status message:

      >>> status = api.PostUpdate(username, password, 'I love python-twitter!')
      >>> print status.text
      I love python-twitter!
  '''

  DEFAULT_CACHE_TIMEOUT = 60 # cache for 1 minute

  _API_REALM = 'Twitter API'

  def __init__(self):
    '''Instantiate a new twitter.Api object.'''
    self._cache = _FileCache()
    self._urllib = urllib2
    self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
    self._user_agent = 'Python-urllib/%s (python-twitter/%s)' % \
                       (self._urllib.__version__, twitter.__version__)

  def GetPublicTimeline(self):
    '''Fetch the sequnce of public twitter.Status message for all users.

    Returns:
      An sequence of twitter.Status instances, one for each message
    '''
    url = 'http://twitter.com/statuses/public_timeline.json'
    json = self._FetchUrl(url)
    data = simplejson.loads(json)
    return [Status.NewFromJsonDict(x) for x in data]

  def GetUserTimeline(self, id, count=None):
    '''Fetch the sequence of public twitter.Status messages for a single user.

    Args:
      id:
        the id of the user to be fetched (not their username, their id number)
      count: the number of status messages to retrieve

    Returns:
      A sequence of twitter.Status instances, one for each message up to count
    '''
    try:
      int(id)
    except:
      raise TwitterError("Twitter id must be an integer")
    try:
      if count:
        int(count)
    except:
      raise TwitterError("Count must be an integer")
    if count:
      parameters = {'count':count}
    else:
      parameters = {}
    url = 'http://twitter.com/t/status/user_timeline/%s' % id
    json = self._FetchUrl(url, parameters=parameters)
    data = simplejson.loads(json)
    return [Status.NewFromJsonDict(x) for x in data]

  def GetFriendsTimeline(self, username, password):
    '''Fetch the sequence of twitter.Status messages for a user\'s friends

    Args:
      username: The username to be fetched
      password: The password for the username to be fetched.

    Returns:
      A sequence of twitter.Status instances, one for each message
    '''
    url = 'http://twitter.com/statuses/friends_timeline.json'
    json = self._FetchUrl(url, username=username, password=password)
    data = simplejson.loads(json)
    return [Status.NewFromJsonDict(x) for x in data]

  def GetFriends(self, username, password):
    '''Fetch the sequence of twitter.User instances, one for each friend

    Args:
      username: The username whose friends should be fetched
      password: The password for the username to be fetched.

    Returns:
      A sequence of twitter.User instances, one for each friend
    '''
    url = 'http://twitter.com/statuses/friends.json'
    json = self._FetchUrl(url, username=username, password=password)
    data = simplejson.loads(json)
    return [User.NewFromJsonDict(x) for x in data]

  def GetFollowers(self, username, password):
    '''Fetch the sequence of twitter.User instances, one for each follower

    Args:
      username: The username whose followers should be fetched
      password: The password for the username to be fetched.

    Returns:
      A sequence of twitter.User instances, one for each follower
    '''
    url = 'http://twitter.com/statuses/followers.json'
    json = self._FetchUrl(url, username=username, password=password)
    data = simplejson.loads(json)
    return [User.NewFromJsonDict(x) for x in data]

  def PostUpdate(self, username, password, text):
    '''Post a twitter status message.

    Args:
      username: The username to post the status message
      password: The password for the username to be posted
      text: The message text to be posted

    Returns:
      A twitter.Status instance representing the message posted
    '''
    url = 'http://twitter.com/statuses/update.json'
    post_data = 'status=%s' % text
    json = self._FetchUrl(url,
                          post_data=post_data,
                          username=username,
                          password=password,
                          no_cache=True)
    data = simplejson.loads(json)
    return Status.NewFromJsonDict(data)


  def SetCache(self, cache):
    '''Override the default cache.  Set to None to prevent caching.

    Args:
      cache: an instance that supports the same API as the  twitter._FileCache
    '''
    self._cache = cache

  def SetUrllib(self, urllib):
    '''Override the default urllib implementation.

    Args:
      urllib: an instance that supports the same API as the urllib2 module
    '''
    self._urllib = urllib

  def SetCacheTimeout(self, cache_timeout):
    '''Override the default cache timeout.

    Args:
      cache_timeout: time, in seconds, that responses should be reused.
    '''
    self._cache_timeout = cache_timeout

  def SetUserAgent(self, user_agent):
    '''Override the default user agent

    Args:
      user_agent: a string that should be send to the server as the User-agent
    '''
    self._user_agent = user_agent

  def _BuildUrl(self, url, path_elements=None, extra_params=None):
    # Break url into consituent parts
    (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)

    # Add any additional path elements to the path
    if path_elements:
      # Filter out the path elements that have a value of None
      p = [i for i in path_elements if i]
      if not path.endswith('/'):
        path += '/'
      path += '/'.join(p)

    # Add any additional query parameters to the query string
    if extra_params and len(extra_params) > 0:
     # Filter out the parameters that have a value of None (but '' is okay)
     p = dict([ (k, v) for k, v in extra_params.items() if v is not None])
     # Convert the parameters into key=value&key=value form
     extra_query = urllib.urlencode(p)
     # Add it to the existing query
     if query:
       query += '&' + extra_query
     else:
       query = extra_query

    # Return the rebuilt URL
    return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))


  def _GetOpener(self, url, username=None, password=None):
    if username and password:
      handler = self._urllib.HTTPBasicAuthHandler()
      (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)
      handler.add_password(Api._API_REALM, netloc, username, password)
      opener = self._urllib.build_opener(handler)
    else:
      opener = self._urllib.build_opener()
    opener.addheaders = [('User-agent', self._user_agent)]
    return opener


  def _FetchUrl(self,
                url,
                post_data=None,
                parameters=None,
                username=None,
                password=None,
                no_cache=None):
    """Fetch a URL, optionally caching for a specified time.

    Args:
      url: The URL to retrieve
      post_data: A string to be sent in the body of the request. [OPTIONAL]
      parameters: A dict of key/value pairs that should added to
                  the query string. [OPTIONAL]
      username: A HTTP Basic Auth username for this request
      username: A HTTP Basic Auth password for this request
      no_cache: If true, overrides the cache on the current request

    Returns:
      A string containing the body of the response.
    """
    # Add key/value parameters to the query string of the url
    url = self._BuildUrl(url, extra_params=parameters)

    # Get a url opener that can handle basic auth
    opener = self._GetOpener(url, username=username, password=password)

    # Open and return the URL immediately if we're not going to cache
    if no_cache or not self._cache or not self._cache_timeout:
      url_data = opener.open(url, post_data).read()
    else:
      # Unique keys are a combination of the url and the username
      if username:
        key = username + ':' + url
      else:
        key = url

      # See if it has been cached before
      last_cached = self._cache.GetCachedTime(key)

      # If the cached version is outdated then fetch another and store it
      if not last_cached or time.time() >= last_cached + self._cache_timeout:
        url_data = opener.open(url, post_data).read()
        self._cache.Set(key, url_data)
      else:
        url_data = self._cache.Get(key)

    # Always return the latest version
    return url_data


class _FileCacheError(Exception):
  '''Base exception class for FileCache related errors'''

class _FileCache(object):

  DEFAULT_ROOT_DIRECTORY = os.path.join(tempfile.gettempdir(), 'python.cache')

  DEPTH = 3

  def __init__(self,root_directory=None):
    self._InitializeRootDirectory(root_directory)

  def Get(self,key):
    path = self._GetPath(key)
    if os.path.exists(path):
      return open(path).read()
    else:
      return None

  def Set(self,key,data):
    path = self._GetPath(key)
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
      os.makedirs(directory)
    if not os.path.isdir(directory):
      raise _FileCacheError('%s exists but is not a directory' % directory)
    temp_fd, temp_path = tempfile.mkstemp()
    temp_fp = os.fdopen(temp_fd, 'w')
    temp_fp.write(data)
    temp_fp.close()
    if not path.startswith(self._root_directory):
      raise _FileCacheError('%s does not appear to live under %s' %
                            (path, self._root_directory))
    os.rename(temp_path, path)

  def Remove(self,key):
    path = self._GetPath(key)
    if not path.startswith(self._root_directory):
      raise _FileCacheError('%s does not appear to live under %s' %
                            (path, self._root_directory ))
    if os.path.exists(path):
      os.remove(path)

  def GetCachedTime(self,key):
    path = self._GetPath(key)
    if os.path.exists(path):
      return os.path.getmtime(path)
    else:
      return None

  def _InitializeRootDirectory(self, root_directory):
    if not root_directory:
      root_directory = _FileCache.DEFAULT_ROOT_DIRECTORY
    root_directory = os.path.abspath(root_directory)
    if not os.path.exists(root_directory):
      os.mkdir(root_directory)
    if not os.path.isdir(root_directory):
      raise _FileCacheError('%s exists but is not a directory' %
                            root_directory)
    self._root_directory = root_directory

  def _GetPath(self,key):
    hashed_key = md5.new(key).hexdigest()
    return os.path.join(self._root_directory,
                        self._GetPrefix(hashed_key),
                        hashed_key)

  def _GetPrefix(self,hashed_key):
    return os.path.sep.join(hashed_key[0:_FileCache.DEPTH])
