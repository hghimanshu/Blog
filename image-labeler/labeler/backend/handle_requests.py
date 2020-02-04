from labeler.mongodb.mongo import (fetchData, insertData, 
                                    groupingData, updateData)

COLL = "Image-Data"

def isLabelInDb(label, image_path):
    query = {"label": label}
    res = fetchData(COLL, query)
    alreadyPresent = False
    if res.count() == 0:
        insert_q = {"label": label, "image_path": image_path}
        insertData(insert_q, COLL)
        
    else:
        alreadyPresent = True
    return alreadyPresent

def getAllImages():
    group_q = {"$group": {"_id": "$label", "image_path": {"$push": "$image_path"}}}
    project_q = {"$project": {"label": 1, "image_path":1}}
    pipeline = [group_q, project_q]

    res = groupingData(COLL, pipeline)
    return res

def getRequiredImages(label):
    query = {"label": label}
    res = fetchData(COLL, query)
    totalImages = []

    if res.count() != 0:
        for i in res:
            image_name = i['image_path']
            # image_name = i['image_path'].split('/')[-1]
            totalImages.append(image_name)
    return totalImages

def updateInfo(image_path, curr_label, new_label):
    curr_label_q = {"label": curr_label}
    new_label_q = {"$set": {"label": new_label}}

    updateData(curr_label_q, new_label_q, COLL)