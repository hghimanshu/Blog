import sys
from searchapp.mongodb.mongo import (fetchData, insertData, 
                                    groupingData, updateData)

COLL = "Image-Data"

def isLabelInDb(label, image_path):
    query = {"label": label}
    res = fetchData(COLL, query)
    alreadyPresent = False
    if res.count() == 0:
        ## means the given label is not in the db
        ## so create the label
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
            totalImages.append(i['image_path'])
    return totalImages

def updateLabel(image_path, curr_label, new_label):
    curr_label_q = {"label": curr_label}
    new_label_q = {"$set": {"label": new_label}}

    updateData(curr_label_q, new_label_q)