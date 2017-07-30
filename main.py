import service,model
from time import time
presetGroup = ['family', 'school', 'girls', 'beautiy', 'model', 'camera']
#TODO: save progress
service.auth()
for query in presetGroup:
    groupId = service.searchGroup(query)['groups']['group'][0]['nsid']
    members = service.getMembers(groupId)['members']['member']
    count = 0
    t0 = time()
    for member in members:
        photos = service.getPhotos(member['nsid'])['photos']['photo']
        for photo in photos:
            info = service.getPhotoInfo(photo['id'])
            model.savePhotoInfo(info)
            model.savePhotoUrl(photo)
            count+=1
        print('%d photos saved, %ds used...' % (count, time()-t0))

presetUsersId = ['128950283@N02', '128161560@N07', '127180464@N07', '61500992@N03', '44542478@N03']
service.auth()
result = presetUsersId
while True:
    if model.getPeople():