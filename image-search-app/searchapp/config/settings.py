import pymongo
from pymongo import MongoClient

ENV = "Staging"

if ENV.lower() == "staging":

    MONGO_DB_NAME = 'C3_python'
    MONGO_DB_URL = 'localhost'
    SET_API = 'https://c3.nayan.co/data_sets'
    SERVER_ADD = 'http://49.205.180.243/' 
    HEADERS = {
            "Content-Type": "application/json",
            "api-key": "V7FE5j6xFECpQb7kYMTRaEWX"
    }

    LP_TEMPLATES_API = 'https://c3.nayan.co/templates?wf_step_id=8'
    FETCH_RESULTS = 'https://c3.nayan.co/results?'
    COMPLETE_SETS = 'https://c3.nayan.co/data_sets?aasm_state='
    COMPLETE_SETS_PARAMS  = {
        "aasm_state": "finished"
    }
    FETCH_WORKFLOWS = 'https://c3.nayan.co/work_flows'
    FETCH_VEH_CLASSIFY = 'https://c3.nayan.co/ai/training_data'
    SET_UPLOAD_REQUEST = 'https://c3.nayan.co/admin/create_set_upload_request'

elif ENV.lower() == "dev":

    MONGO_DB_NAME = 'C3_python_dev'
    MONGO_DB_URL = 'localhost'
    SET_API = 'https://c3-backend-dev.herokuapp.com/data_sets'
    SERVER_ADD = 'http://49.205.180.243/' 
    HEADERS = {
                "Content-Type": "application/json",
                "api-key": "7V6Ar8NXXHuG3dtGHJ1epp4A"
    }
    LP_TEMPLATES_API = 'https://c3-backend-dev.herokuapp.com/data_sets'
    FETCH_RESULTS = 'https://c3-backend-dev.herokuapp.com/results?'
    COMPLETE_SETS = 'https://c3-backend-dev.herokuapp.com/data_sets?aasm_state='
    COMPLETE_SETS_PARAMS  = {
        "aasm_state": "finished"
    }
    FETCH_WORKFLOWS = 'https://c3-backend-dev.herokuapp.com/work_flows'
    FETCH_VEH_CLASSIFY = 'https://c3-backend-dev.herokuapp.com/ai/training_data'
    SET_UPLOAD_REQUEST = 'https://c3-backend-dev.herokuapp.com/admin/create_set_upload_request'

else:

    MONGO_DB_NAME = 'C3_python_local'
    MONGO_DB_URL = 'localhost'
    SET_API = 'http://localhost:3000/data_sets'
    SERVER_ADD = 'http://49.205.180.243/' 
    HEADERS = {
                "Content-Type": "application/json",
                "api-key": "cXKvb7sNCcs1NJRK3pthmBYV"
    }
    LP_TEMPLATES_API = 'http://localhost:3000/templates?wf_step_id=8'
    FETCH_RESULTS = 'http://localhost:3000/results?'
    COMPLETE_SETS = 'http://localhost:3000/data_sets?aasm_state='
    COMPLETE_SETS_PARAMS  = {
        "aasm_state": "finished"
    }
    FETCH_WORKFLOWS = 'http://localhost:3000/work_flows'
    FETCH_VEH_CLASSIFY = 'http://localhost:3000/ai/training_data'
    SET_UPLOAD_REQUEST = 'http://localhost:3000/admin/create_set_upload_request'

BASE_ADD = '/var/www/html/'
MAX_LIMIT_OF_RECORDS = 1000

CLIENT = MongoClient()
CLIENT = MongoClient(MONGO_DB_URL, 27017)
DB = CLIENT[MONGO_DB_NAME]

REDIS_AUTH = 'RK2lJcwmp7SHJSvySpMuM12Okfoo0N7E8fiAUqnYznRTXzlLSb'