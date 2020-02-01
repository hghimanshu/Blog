import sys
from searchapp.mongodb.mongo import fetchData, insertData


def isLabelInDb(label, image_path):
    coll = "Image-Data"
    query = {"label": label}
    res = fetchData(coll, query)
    alreadyPresent = False
    if res.count() == 0:
        ## means the given label is not in the db
        ## so create the label
        insert_q = {"label": label, "image_path": image_path}
        insertData(coll, insert_q)
    else:
        alreadyPresent = True
    return alreadyPresent