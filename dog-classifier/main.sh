conda activate py36
/home/himanshu/anaconda3/envs/py36/bin/python /home/techject/Abhishek/C3/worker.py &
/home/techject/Abhishek/C3-python/run.py
/home/himanshu/anaconda3/envs/py36/bin/gunicorn --bind 0.0.0.0:8000 run --reload --timeout=360