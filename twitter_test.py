#!/usr/bin/python
#
# Copyright 2007 Google Inc. All Rights Reserved.

'''Unit tests for the twitter.py library'''

__author__ = 'dewitt@google.com'

import os
import simplejson
import time
import unittest

import twitter

class StatusTest(unittest.TestCase):

  SAMPLE_JSON = '''{"created_at": "Fri Jan 26 23:17:14 +0000 2007", "id": 4391023, "text": "Canvas. JC Penny. Three ninety-eight.", "user": {"description": "Canvas. JC Penny. Three ninety-eight.", "id": 718443, "location": "Okinawa, Japan", "name": "Kesuke Miyagi", "profile_image_url": "http:\/\/twitter.com\/system\/user\/profile_image\/718443\/normal\/kesuke.png", "screen_name": "kesuke", "url": "http:\/\/twitter.com\/kesuke"}}'''

  def _GetSampleUser(self):
    return twitter.User(id=718443,
                        name='Kesuke Miyagi',
                        screen_name='kesuke',
                        description=u'Canvas. JC Penny. Three ninety-eight.',
                        location='Okinawa, Japan',
                        url='http://twitter.com/kesuke',
                        profile_image_url='http://twitter.com/system/user/pro'
                                          'file_image/718443/normal/kesuke.pn'
                                          'g')

  def _GetSampleStatus(self):
    return twitter.Status(created_at='Fri Jan 26 23:17:14 +0000 2007',
                          id=4391023,
                          text='Canvas. JC Penny. Three ninety-eight.',
                          user=self._GetSampleUser())

  def testInit(self):
    '''Test the twitter.Status constructor'''
    status = twitter.Status(created_at='Fri Jan 26 23:17:14 +0000 2007',
                            id=4391023,
                            text='Canvas. JC Penny. Three ninety-eight.',
                            user=self._GetSampleUser())

  def testGettersAndSetters(self):
    '''Test all of the twitter.Status getters and setters'''
    status = twitter.Status()
    status.SetId(4391023)
    self.assertEqual(4391023, status.GetId())
    status.SetCreatedAt('Fri Jan 26 23:17:14 +0000 2007')
    self.assertEqual('Fri Jan 26 23:17:14 +0000 2007', status.GetCreatedAt())
    status.SetText('Canvas. JC Penny. Three ninety-eight.')
    self.assertEqual('Canvas. JC Penny. Three ninety-eight.',
                     status.GetText())
    status.SetUser(self._GetSampleUser())
    self.assertEqual(718443, status.GetUser().id)

  def testProperties(self):
    '''Test all of the twitter.Status properties'''
    status = twitter.Status()
    status.id = 1
    self.assertEqual(1, status.id)
    status.created_at = 'Fri Jan 26 23:17:14 +0000 2007'
    self.assertEqual('Fri Jan 26 23:17:14 +0000 2007', status.created_at)
    status.user = self._GetSampleUser()
    self.assertEqual(718443, status.user.id)

  def testAsJsonString(self):
    '''Test the twitter.Status AsJsonString method'''
    self.assertEqual(StatusTest.SAMPLE_JSON,
                     self._GetSampleStatus().AsJsonString())

  def testAsDict(self):
    '''Test the twitter.Status AsDict method'''
    status = self._GetSampleStatus()
    data = status.AsDict()
    self.assertEqual(4391023, data['id'])
    self.assertEqual('Fri Jan 26 23:17:14 +0000 2007', data['created_at'])
    self.assertEqual('Canvas. JC Penny. Three ninety-eight.', data['text'])
    self.assertEqual(718443, data['user']['id'])

  def testEq(self):
    '''Test the twitter.Status __eq__ method'''
    status = twitter.Status()
    status.created_at = 'Fri Jan 26 23:17:14 +0000 2007'
    status.id = 4391023
    status.text = 'Canvas. JC Penny. Three ninety-eight.'
    status.user = self._GetSampleUser()
    self.assertEqual(status, self._GetSampleStatus())

  def testNewFromJsonDict(self):
    '''Test the twitter.Status NewFromJsonDict method'''
    data = simplejson.loads(StatusTest.SAMPLE_JSON)
    status = twitter.Status.NewFromJsonDict(data)
    self.assertEqual(self._GetSampleStatus(), status)

class UserTest(unittest.TestCase):

  SAMPLE_JSON = '''{"description": "Indeterminate things", "id": 673483, "location": "San Francisco, CA", "name": "DeWitt", "profile_image_url": "http:\/\/twitter.com\/system\/user\/profile_image\/673483\/normal\/me.jpg", "screen_name": "dewitt", "status": {"created_at": "Fri Jan 26 17:28:19 +0000 2007", "id": 4212713, "text": "\\"Select all\\" and archive your Gmail inbox.  The page loads so much faster!"}, "url": "http:\/\/unto.net\/"}'''

  def _GetSampleStatus(self):
    return twitter.Status(created_at='Fri Jan 26 17:28:19 +0000 2007',
                          id=4212713,
                          text='"Select all" and archive your Gmail inbox. '
                               ' The page loads so much faster!')

  def _GetSampleUser(self):
    return twitter.User(id=673483,
                        name='DeWitt',
                        screen_name='dewitt',
                        description=u'Indeterminate things',
                        location='San Francisco, CA',
                        url='http://unto.net/',
                        profile_image_url='http://twitter.com/system/user/prof'
                                          'ile_image/673483/normal/me.jpg',
                        status=self._GetSampleStatus())



  def testInit(self):
    '''Test the twitter.User constructor'''
    user = twitter.User(id=673483,
                        name='DeWitt',
                        screen_name='dewitt',
                        description=u'Indeterminate things',
                        url='http://twitter.com/dewitt',
                        profile_image_url='http://twitter.com/system/user/prof'
                                          'ile_image/673483/normal/me.jpg',
                        status=self._GetSampleStatus())

  def testGettersAndSetters(self):
    '''Test all of the twitter.User getters and setters'''
    user = twitter.User()
    user.SetId(673483)
    self.assertEqual(673483, user.GetId())
    user.SetName('DeWitt')
    self.assertEqual('DeWitt', user.GetName())
    user.SetScreenName('dewitt')
    self.assertEqual('dewitt', user.GetScreenName())
    user.SetDescription('Indeterminate things')
    self.assertEqual('Indeterminate things', user.GetDescription())
    user.SetLocation('San Francisco, CA')
    self.assertEqual('San Francisco, CA', user.GetLocation())
    user.SetProfileImageUrl('http://twitter.com/system/user/profile_im'
                            'age/673483/normal/me.jpg')
    self.assertEqual('http://twitter.com/system/user/profile_image/673'
                     '483/normal/me.jpg', user.GetProfileImageUrl())
    user.SetStatus(self._GetSampleStatus())
    self.assertEqual(4212713, user.GetStatus().id)

  def testProperties(self):
    '''Test all of the twitter.User properties'''
    user = twitter.User()
    user.id = 673483
    self.assertEqual(673483, user.id)
    user.name = 'DeWitt'
    self.assertEqual('DeWitt', user.name)
    user.screen_name = 'dewitt'
    self.assertEqual('dewitt', user.screen_name)
    user.description = 'Indeterminate things'
    self.assertEqual('Indeterminate things', user.description)
    user.location = 'San Francisco, CA'
    self.assertEqual('San Francisco, CA', user.location)
    user.profile_image_url = 'http://twitter.com/system/user/profile_i' \
                             'mage/673483/normal/me.jpg'
    self.assertEqual('http://twitter.com/system/user/profile_image/6734'
                     '83/normal/me.jpg', user.profile_image_url)
    self.status = self._GetSampleStatus()
    self.assertEqual(4212713, self.status.id)

  def testAsJsonString(self):
    '''Test the twitter.User AsJsonString method'''
    self.assertEqual(UserTest.SAMPLE_JSON,
                     self._GetSampleUser().AsJsonString())

  def testAsDict(self):
    '''Test the twitter.User AsDict method'''
    user = self._GetSampleUser()
    data = user.AsDict()
    self.assertEqual(673483, data['id'])
    self.assertEqual('DeWitt', data['name'])
    self.assertEqual('dewitt', data['screen_name'])
    self.assertEqual('Indeterminate things', data['description'])
    self.assertEqual('San Francisco, CA', data['location'])
    self.assertEqual('http://twitter.com/system/user/profile_image/6734'
                     '83/normal/me.jpg', data['profile_image_url'])
    self.assertEqual('http://unto.net/', data['url'])
    self.assertEqual(4212713, data['status']['id'])

  def testEq(self):
    '''Test the twitter.User __eq__ method'''
    user = twitter.User()
    user.id = 673483
    user.name = 'DeWitt'
    user.screen_name = 'dewitt'
    user.description = 'Indeterminate things'
    user.location = 'San Francisco, CA'
    user.profile_image_url = 'http://twitter.com/system/user/profile_image/67' \
                             '3483/normal/me.jpg'
    user.url = 'http://unto.net/'
    user.status = self._GetSampleStatus()
    self.assertEqual(user, self._GetSampleUser())

  def testNewFromJsonDict(self):
    '''Test the twitter.User NewFromJsonDict method'''
    data = simplejson.loads(UserTest.SAMPLE_JSON)
    user = twitter.User.NewFromJsonDict(data)
    self.assertEqual(self._GetSampleUser(), user)


class FileCacheTest(unittest.TestCase):

  def testInit(self):
    """Test the twitter._FileCache constructor"""
    cache = twitter._FileCache()
    self.assert_(cache is not None, 'cache is None')

  def testSet(self):
    """Test the twitter._FileCache.Set method"""
    cache = twitter._FileCache()
    cache.Set("foo",'Hello World!')
    cache.Remove("foo")

  def testRemove(self):
    """Test the twitter._FileCache.Remove method"""
    cache = twitter._FileCache()
    cache.Set("foo",'Hello World!')
    cache.Remove("foo")
    data = cache.Get("foo")
    self.assertEqual(data, None, 'data is not None')

  def testGet(self):
    """Test the twitter._FileCache.Get method"""
    cache = twitter._FileCache()
    cache.Set("foo",'Hello World!')
    data = cache.Get("foo")
    self.assertEqual('Hello World!', data)
    cache.Remove("foo")

  def testGetCachedTime(self):
    """Test the twitter._FileCache.GetCachedTime method"""
    now = time.time()
    cache = twitter._FileCache()
    cache.Set("foo",'Hello World!')
    cached_time = cache.GetCachedTime("foo")
    delta = cached_time - now
    self.assert_(delta <= 1,
                 'Cached time differs from clock time by more than 1 second.')
    cache.Remove("foo")

class ApiTest(unittest.TestCase):
  def setUp(self):
    self._urllib = MockUrllib()
    api = twitter.Api()
    api.SetCache(NullCache())
    api.SetUrllib(self._urllib)
    self._api = api

  def testGetPublicTimeline(self):
    '''Test the twitter.Api GetPublicTimeline method'''
    self._AddHandler('http://twitter.com/statuses/public_timeline.json',
                     curry(self._OpenTestData, 'public_timeline.json'))
    statuses = self._api.GetPublicTimeline()
    # This is rather arbitrary, but spot checking is better than nothing
    self.assertEqual(20463, statuses[0].user.id)
    news = [s.text for s in statuses if s.user.screen_name == 'googlenews']
    self.assertEqual(3, len(news))

  def testGetUserTimeline(self):
    '''Test the twitter.Api GetUserTimeline method'''
    self._AddHandler('http://twitter.com/t/status/user_timeline/673483?count=1',
                     curry(self._OpenTestData, 'user_timeline.json'))
    statuses = self._api.GetUserTimeline(673483, count=1)
    # This is rather arbitrary, but spot checking is better than nothing
    self.assertEqual(4212713, statuses[0].id)
    self.assertEqual(673483, statuses[0].user.id)

  def testGetFriendsTimeline(self):
    '''Test the twitter.Api GetFriendsTimeline method'''
    self._AddHandler('http://twitter.com/statuses/friends_timeline.json',
                     curry(self._OpenTestData, 'friends_timeline.json'))
    statuses = self._api.GetFriendsTimeline('kesuke', 'xxx')
    # This is rather arbitrary, but spot checking is better than nothing
    buzz = [s.text for s in statuses if s.user.screen_name == 'buzz']
    self.assertEqual('Surprisingly strong 6k run in Golden Gate Park.', buzz[0])

  def testGetFriends(self):
    '''Test the twitter.Api GetFriends method'''
    self._AddHandler('http://twitter.com/statuses/friends.json',
                     curry(self._OpenTestData, 'friends.json'))
    users = self._api.GetFriends('kesuke', 'xxx')
    # This is rather arbitrary, but spot checking is better than nothing
    buzz = [u.status.text for u in users if u.screen_name == 'buzz']
    self.assertEqual('Surprisingly strong 6k run in Golden Gate Park.', buzz[0])

  def testGetFollowers(self):
    '''Test the twitter.Api GetFollowers method'''
    self._AddHandler('http://twitter.com/statuses/followers.json',
                     curry(self._OpenTestData, 'followers.json'))
    users = self._api.GetFollowers('kesuke', 'xxx')
    # This is rather arbitrary, but spot checking is better than nothing
    buzz = [u.status.text for u in users if u.screen_name == 'buzz']
    self.assertEqual('Surprisingly strong 6k run in Golden Gate Park.', buzz[0])

  def testPostUpdate(self):
    '''Test the twitter.Api PostUpdate method'''
    self._AddHandler('http://twitter.com/statuses/update.json',
                     curry(self._OpenTestData, 'update.json'))
    status = self._api.PostUpdate('kesuke', 'xxx', 'This is a test')
    # This is rather arbitrary, but spot checking is better than nothing
    self.assertEqual('This is a test', status.text)

  def _AddHandler(self, url, callback):
    self._urllib.AddHandler(url, callback)

  def _GetTestDataPath(self, filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(directory, 'testdata')
    return os.path.join(test_data_dir, filename)

  def _OpenTestData(self, filename):
    return open(self._GetTestDataPath(filename))

class MockUrllib(object):
  '''A mock replacement for urllib that hardcodes specific responses.'''

  def __init__(self):
    self._handlers = {}
    self.HTTPBasicAuthHandler = MockHTTPBasicAuthHandler

  def AddHandler(self, url, callback):
    self._handlers[url] = callback

  def build_opener(self, *handlers):
    return MockOpener(self._handlers)

class MockOpener(object):
  '''A mock opener for urllib'''

  def __init__(self, handlers):
    self._handlers = handlers

  def open(self, url, data=None):
    if url in self._handlers:
      return self._handlers[url]()
    else:
      raise Exception('Unexpected URL %s' % url)

class MockHTTPBasicAuthHandler(object):
  '''A mock replacement for HTTPBasicAuthHandler'''

  def add_password(self, realm, uri, user, passwd):
    # TODO(dewitt): Add verification that the proper args are passed
    pass


class NullCache(object):
  '''A no-op replacement for the cache class'''

  def Get(self, key):
    return None

  def Set(self, key, data):
    pass

  def Remove(self, key):
    pass

  def GetCachedTime(self, key):
    return None


class curry:
  # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52549

  def __init__(self, fun, *args, **kwargs):
    self.fun = fun
    self.pending = args[:]
    self.kwargs = kwargs.copy()

  def __call__(self, *args, **kwargs):
    if kwargs and self.kwargs:
      kw = self.kwargs.copy()
      kw.update(kwargs)
    else:
      kw = kwargs or self.kwargs
    return self.fun(*(self.pending + args), **kw)


def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(FileCacheTest))
  suite.addTests(unittest.makeSuite(StatusTest))
  suite.addTests(unittest.makeSuite(UserTest))
  suite.addTests(unittest.makeSuite(ApiTest))
  return suite

if __name__ == '__main__':
  unittest.main()
