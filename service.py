import flickrapi

flickr = flickrapi.FlickrAPI('e8da46355582dfa4165641c938638de8', '9f667d8ad49e540a', cache=True, format='parsed-json')
    
def auth():
    if not flickr.token_valid(perms='read'):
        # Get a request token
        flickr.get_request_token(oauth_callback='oob')
        # Open a browser at the authentication URL. Do this however
        # you want, as long as the user visits that URL.
        authorize_url = flickr.auth_url(perms=u'read')
        print(authorize_url)
        # Get the verifier code from the user. Do this however you
        # want, as long as the user gives the application the code.
        verifier = unicode(input('Verifier code: '))
        # Trade the request token for an access token
        flickr.get_access_token(verifier)
        print('authentication successed!')
    else:
        print('you have already authenticated')
        pass

def getUserGroup(userId):
    try:
        result = flickr.people.getGroups(user_id=userId)['groups']['group']
    except Exception as err:
        print(err)
    else:
        return result

# TODO: consider the pagination
def getMembers(groupId): # duprecated
    try:
        result = flickr.groups.members.getList(group_id=groupId)
    except Exception as err:
        print(err)
    else:
        return result

def getPhotos(userId):
    try:
        result = flickr.people.getPhotos(user_id=userId)
    except Exception as err:
        print(err)
    else:
        return result

def getPhotoInfo(photoId):
    try:
        result = flickr.photos.getInfo(photo_id=photoId)
    except Exception as err:
        print(err)
    else:
        return result

def getPhotoFavi(photoId): # duprecated
    try:
        result = flickr.photos.getFavorites(photo_id=photoId)
    except Exception as err:
        print(err)
    else:
        return result

def getFaviPhotos(userId):
    try:
        result = flickr.favorites.getList(user_id=userId, perpage=500)['photos']['photo']
    except Exception as err:
        print(err)
    else:
        return result

def getUserInfo(userId):
    try:
        result = flickr.people.getInfo(user_id=userId)
    except Exception as err:
        print(err)
    else:
        return result

def getContactInfo(userId):
    try:
        result = flickr.contacts.getList(user_id=userId)['contacts']['contact']
    except Exception as err:
        print(err)
    else:
        return result

def getPublicContactInfo(userId):
    try:
        result = flickr.contacts.getPublicList(user_id=userId)['contacts']['contact']
    except Exception as err:
        print(err)
    else:
        return result

def getUserTagInfo(userId):
    try:
        result = flickr.tags.getListUser(user_id=userId)['who']['tags']['tag']
        if result is not None:
            result = map(lambda item: item['_content'], result)
    except Exception as err:
        print(err)
    else:
        return result