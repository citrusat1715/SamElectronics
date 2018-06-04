#for updating 

##1. service supervisor restart Sam
##2. service nginx restart 

#code base location: cd /home/projects/Sam/src

# pulling new code : git pull origin master

# mysql 
##user : root
##mysql pass : this1sm3
##database name: Sam

#log files: /home/projects/Sam/logs

#production(server) database on settings.py file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Sam',
        'USER': 'root',
        'PASSWORD': 'this1sm3',
        'HOST': 'localhost',
        'PORT': '',
    }
}

