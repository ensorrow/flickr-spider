"""
Flickr API Service Module

This module provides functions to interact with the Flickr API for various operations
including authentication, user management, photo operations, and group interactions.
"""

import flickrapi

# Initialize Flickr API client with API key and secret
flickr = flickrapi.FlickrAPI('e8da46355582dfa4165641c938638de8', '9f667d8ad49e540a', cache=True, format='parsed-json')

def auth():
    """
    Authenticate with Flickr API using OAuth.
    
    Checks if a valid token exists, otherwise initiates the OAuth flow:
    1. Gets a request token
    2. Opens authentication URL in browser
    3. Prompts user for verification code
    4. Trades request token for access token
    
    Returns:
        None
    """
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
    """
    Get groups that a user belongs to.
    
    Args:
        userId (str): The Flickr user ID
        
    Returns:
        dict: Groups information or None if error occurs
    """
    try:
        result = flickr.people.getGroups(user_id=userId)['groups']['group']
    except Exception as err:
        print(err)
    else:
        return result

# TODO: consider the pagination
def getMembers(groupId): # deprecated
    """
    Get members of a group (deprecated).
    
    Args:
        groupId (str): The Flickr group ID
        
    Returns:
        dict: Members information or None if error occurs
    """
    try:
        result = flickr.groups.members.getList(group_id=groupId)
    except Exception as err:
        print(err)
    else:
        return result

def getPhotos(userId):
    """
    Get photos uploaded by a user.
    
    Args:
        userId (str): The Flickr user ID
        
    Returns:
        dict: Photos information or None if error occurs
    """
    try:
        result = flickr.people.getPhotos(user_id=userId)
    except Exception as err:
        print(err)
    else:
        return result

def getPhotoInfo(photoId):
    """
    Get detailed information about a photo.
    
    Args:
        photoId (str): The Flickr photo ID
        
    Returns:
        dict: Photo information or None if error occurs
    """
    try:
        result = flickr.photos.getInfo(photo_id=photoId)
    except Exception as err:
        print(err)
    else:
        return result

def getPhotoFavi(photoId): # deprecated
    """
    Get favorites for a photo (deprecated).
    
    Args:
        photoId (str): The Flickr photo ID
        
    Returns:
        dict: Favorites information or None if error occurs
    """
    try:
        result = flickr.photos.getFavorites(photo_id=photoId)
    except Exception as err:
        print(err)
    else:
        return result

def getFaviPhotos(userId):
    """
    Get favorite photos of a user.
    
    Args:
        userId (str): The Flickr user ID
        
    Returns:
        list: List of favorite photos or None if error occurs
    """
    try:
        result = flickr.favorites.getList(user_id=userId, perpage=500)['photos']['photo']
    except Exception as err:
        print("from getFaviPhotos")
        print(err)
    else:
        return result

def getUserInfo(userId):
    """
    Get detailed information about a user.
    
    Args:
        userId (str): The Flickr user ID
        
    Returns:
        dict: User information or None if error occurs
    """
    try:
        result = flickr.people.getInfo(user_id=userId)
    except Exception as err:
        print('from userinfo')
        print(err)
    else:
        return result

def getContactInfo(userId):
    """
    Get contacts of a user (private).
    
    Args:
        userId (str): The Flickr user ID
        
    Returns:
        list: List of contacts or empty list if none or error occurs
    """
    try:
        result = flickr.contacts.getList(user_id=userId)['contacts']
        if result.has_key('contact'):
            result = result['contact']
        else:
            result = []
    except Exception as err:
        print('from contactInfo')
        print(err)
    else:
        return result

def getPublicContactInfo(userId):
    """
    Get public contacts of a user.
    
    Args:
        userId (str): The Flickr user ID
        
    Returns:
        list: List of public contacts or empty list if none or error occurs
    """
    try:
        result = flickr.contacts.getPublicList(user_id=userId)['contacts']
        if result.has_key('contact'):
            result = result['contact']
        else:
            result = []
    except Exception as err:
        print('from pubcontactInfo')
        print(err)
    else:
        return result

def getUserTagInfo(userId):
    """
    Get tags used by a user.
    
    Args:
        userId (str): The Flickr user ID
        
    Returns:
        list: List of user tags or None if error occurs
    """
    try:
        result = flickr.tags.getListUser(user_id=userId)['who']['tags']['tag']
        if result:
            result = map(lambda item: item['_content'], result)
    except Exception as err:
        print('from tag')
        print(err)
    else:
        return result