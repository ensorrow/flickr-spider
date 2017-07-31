def dequeue(queue):# use queue[0] as a pointer
    headIndex = queue[0]
    queue[0]+=1
    return queue[headIndex]

def isEmpty(queue):
    headIndex = queue[0]
    length = len(queue)
    if headIndex == length-1:
        return True
    else:
        return False

def handleContact(contactors):
    doc = {
        "family": [],
        "friend": [],
        "public": []
    }
    if contactors is not None:
        for contact in contactors:
            if not contact.has_key('family'):
                doc['public'].append(contact)
            elif contact['family'] == '1':
                doc['family'].append(contact)
            elif contact['friend'] == '1':
                doc['friend'].append(contact)
            else:
                doc['public'].append(contact)
    return doc