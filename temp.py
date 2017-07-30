import flickrapi

flickr = flickrapi.FlickrAPI('e8da46355582dfa4165641c938638de8', '9f667d8ad49e540a', cache=True, format='parsed-json')
res = flickr.photos.getSizes(photo_id=4581149290)
print(res)