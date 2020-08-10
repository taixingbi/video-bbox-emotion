
### run pip shell
```
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
```

### run migrate
##### packaging up your model changes
```
python manage.py makemigrations 
```
##### applying those to your database.
```
python manage.py migrate 
```


### run local
```
python manage.py runserver 0.0.0.0:8083
```

### run aws ubuntu 18.04
https://www.digitalocean.com/community/tutorials/how-to-install-the-django-web-framework-on-ubuntu-18-04
```
python3.6 -m venv my_env
source my_env/bin/activate
```

### run docker
```
docker-compose build
docker-compose up 
```

python manage.py runserver 0.0.0.0:8083
http://localhost:8000/
http://3.230.163.203:8083/test


### access container
```
docker exec -it containerId bash   
```

### more docker 
```
docker stop $(docker ps -aq)    
docker rm $(docker ps -aq)    
docker rmi $(docker images -q)
```


### reference
https://hub.docker.com/_/django/   
https://docs.docker.com/compose/django/

### ssh
ssh -i "demo.pem" ubuntu@ec2-3-230-163-203.compute-1.amazonaws.com


### mount
sshfs ubuntu@ec2-3-230-163-203.compute-1.amazonaws.com:/home/ubuntu/transcription-api ~/transcribe-server/local_share -o IdentityFile=~/transcribe-server/demo.pem -o  allow_other 

https://howchoo.com/g/ymmxmzlmndb/how-to-install-sshfs

### run
http://3.81.137.95:8083/


### permit

chmod -R 777 







