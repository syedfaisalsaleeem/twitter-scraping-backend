
# Twiter Scraper 

```
backend
├─ .env
├─ .gitignore
├─ app.py
├─ application
│  └─ app
│     ├─ cronjob
│     │  └─ controllers
│     │     ├─ control_cronjob_controller.py
│     │     ├─ cronjob_controller.py
│     │     ├─ test_control_cronjob_controller.py
│     │     └─ test_cronjob_controller.py
│     ├─ notification
│     │  ├─ notification_controller.py
│     │  └─ notification_controller_test.py
│     └─ twitter
│        ├─ cronjob_twitter_scraping_controller.py
│        └─ store_data.py
├─ authentication_controller.py
├─ build
│  ├─ asset-manifest.json
│  ├─ favicon.ico
│  ├─ index.html
│  ├─ logo192.png
│  ├─ logo512.png
│  ├─ manifest.json
│  ├─ robots.txt
│  ├─ static
│  │  ├─ css
│  │  │  ├─ main.c9a96ece.css
│  │  │  └─ main.c9a96ece.css.map
│  │  └─ js
│  │     ├─ 787.cf2e1aca.chunk.js
│  │     ├─ 787.cf2e1aca.chunk.js.map
│  │     ├─ main.a01e69b8.js
│  │     ├─ main.a01e69b8.js.LICENSE.txt
│  │     ├─ main.a01e69b8.js.map
│  │     ├─ main.e08f328c.js
│  │     ├─ main.e08f328c.js.LICENSE.txt
│  │     ├─ main.e08f328c.js.map
│  │     ├─ main.ec1c9fab.js
│  │     ├─ main.ec1c9fab.js.LICENSE.txt
│  │     └─ main.ec1c9fab.js.map
│  ├─ unnamed.png
│  └─ unnamedr.png
├─ controller.py
├─ docker-compose.dev.yml
├─ Dockerfile
├─ extensions.py
├─ installation_text.txt
├─ nginx
│  └─ nginx.dev.conf
├─ Readme.md
├─ requirements.txt
├─ task_queue.py
├─ utility.py
└─ _mongodb.py
```

## .env

This file contains all the environment variables required for this application.

## .gitignore

This file contains all the files which needs to be ignored when we need to push to cloud

## app.py

This file is the main file when we are starting the application. This is where the logic starts of the entire application. All the required imports are made at start. The cronjob time is defined, secret key of the application, json web token expiry, celery backend url, mongo client url which is mongodb url and the db used are defined in this file.
At start of the server we insert the user which is the user that can access the apis . if the user is already there then the user will not be inserted . Similary Cronjob is inserted as default on when the server is started but it will not update again util we hit the api to update the control cron job. The starting cronjob time is also inserted when the server is started.

### Endpoints in app.py 

- /api/twitter (methods = ['POST' and 'GET'])
- /api/login (method = 'POST')
- /api/refresh (method= 'POST')
- /api/notification (methods = ['PUT' and 'GET'])
- /api/cronjob (methods = ['POST', 'GET' and 'DELETE'])
- /api/cronjob (methods = ['PUT' and 'GET'])
- /api/cronjobtime (method= 'GET')

- / (method= 'GET')
- /home (method= 'GET')
- /notifications (method= 'GET')
- /cronjob (method= 'GET')

### Detail about each endpoint

1) /api/twitter (POST METHOD) => this endpoint is responsible for starting the crawling when the post request is made. it contains the taskqueue line which sends the api request to task queue.
The request payload is :
{
    "key_phrases":[],
    "start_date": "string of date time",
    "end_date": "string of date time",
    "method": "scraped",
    "break" : False
}

2) /api/twitter (GET METHOD) => this endpoint is responsible for check the json token is valid or not.

3) /api/login (POST METHOD) => this endpoint is responsible for creating a valid token if the user enter the valid credentials.
The request payload is :
{
    "username":"string",
    "password":"string"
}

4) /api/refresh (POST METHOD) => this endpoint is responsible for refreshing the access token when it's expired.

5) /api/notification (GET METHOD) => this endpoint is responsible for getting all the not notifications whether it's pending, processed and completed. we send the query parameters to get the type of notification.

6) /api/notification (PUT METHOD) => this endpoint is responsible for updating the notification method in the db.
The request payload is :
{
    "method" : "string"
}

7) /api/cronjob (GET METHOD) => this endpoint is responsible for getting all the keyphrases which are in cronjob.

8) /api/cronjob (POST METHOD) => this endpoint is responsible for creating the new keyphrase for cronjob.
The request payload is:
{
    "keyphrases": []
}

9) /api/cronjob (DELETE METHOD) => this endpoint is responsible for deleting the keyphrase in cronjob collection.
the request payload is:
{
    'id':'string'
}

10) /api/controlcronjob (GET METHOD) => this endpoint is responsible for getting the value of control job whether it's true or false.

11) /api/controlcronjob (PUT METHOD) => this endpoint is responsible for updating the cronjob from true to false or either.

12) /api/cronjobtime (GET METHOD) => this endpoint is responsible for getting the cronjob time when the next cronjob is going to start.

13) ['/','/home','/notifications','/cronjob'] (GET METHOD) => this endpoint is responsible for sending the html page to the browser.

## application/app/cronjob/controllers/control_cronjob_controller.py

In this file the 'controlcronjob' collection in mongodb is updated, created, deleted and get. this file is responsible for updating the controlcronjob status to make sure if the status is True the cronjob will be started.

## application/app/cronjob/controllers/cronjob_controller.py

In the file 'cronjobkeywords' collection in mongodb is updated, created, deleted and get. this file contains two classes CronJobController and CronJobTime.

1) CronJobController: 
This class contains the logic of adding the new keywords in cronjob task, get all the cronjob keywords, delete individual keywords. It also updates the location of cronjob keyword where it's stored.

2) CronJobTime:
When first time the cronjob is started it insert the current date time in 'cronjobtime' collection . when the next cronjob is started it updates the cronjob time. the get method is used to get the updated cronjob time form db.

## application/app/cronjob/controllers/test_control_cronjob_controller.py

The unit test file for testing the control cronjob controller functions

## application/app/cronjob/controllers/test_cronjob_controller.py

The unit test file for testing the cron job controller functions.

## application/app/notfication/notification_controller_test.py

The unit test file for testing notification controller functions.

## application/app/notfication/notification_controller.py

This file contains the Notification Controller class which is responsible for getting all the keyphrases in 'notifcation' collection with the status parameter defined to get the pending, processing or completed. In this file we can insert the new keyphrases also when we start the scraping the keyphrases are inserted and when the keyphrases is in progess of scraping the update method is called. The delete method is responsible for deleting the keyphrase when the total records is greater than 50 and delete the completed status record which was in the end in table or collection.

## application/app/twitter/cronjob_twitter_scraping_controller.py

This file contains the cronjob logic of scrapping the given keywords mentioned in cronjob collection. After scraping the result is stored in s3.

## application/app/twitter/store_data.py

This file is responsible for storing the data in s3 with the correct path format.

## build

This file contains all the react build code which is retrieved from the frontend repository after the react code is build using

``` npm run build ```

## authentication_controller.py

This file contains the AuthenticationController class which uses authentication_controller collection. This file coontains the method of checking the user credentials and producing the refresh token on the correct credentials as well in the register method in which we create user only one time with the refresh token.

## controller.py

This file contains the logic of scraping the multiple keywords and calls the function of storing the data into s3 bucket. This file uses snscrape library for scrapping the keywords from the twitter and gets the specific attributes with storing the data first in python list , then storing that data in to compressed csv after that sending that compressed csv to s3.

## docker-compose.dev.yml

This file build the docker image with ngnix server and python flask server.

## Dockerfile

This file contains the linux commands needs to run in docker container.

## extensions.py

This file contains all the necessary library intializations.

## utility.py 

This file contains all the utility functions which is required in all over python code.

## task_queue.py

This file contains all the functions which needs to be queued in redis. such as crawling of twitter keywords and cronjob function. 

## _mongodb.py

This file contains all the updating, inserting of keywords status which are being scraped with snscrape.

## Deployment

1) git clone frontend repo
2) npm install
3) npm run build
4) git clone backend repo
5) copy the build folder to backend repo and replace the necessary files
6) Push the updated code to backend repo
7) ssh into the aws cloud.
8) cd twitter-scraping-backend
9) git pull updated code
10) install requirements.txt
11) start 4 terminals with different ssh into aws.
12) go to first terminal
12) type tmux attach-session mytestapp
13) rerun the python server to reflect changes by ``` python3 app.py ```
14) go to second terminal
15) type tmux attach-session celery
16) press ctrl+C to stop celery and type celery worker -A task_queue.celery --loglevel=info --pool=solo -n one
17) go to third terminal
18) type tmux attach-session celerybeat
19) press ctrl+C to stop celery and type celery beat -A task_queue.celery --loglevel=info
20) go to fourth terminal
21) type tmux attach-session celerybeattask
22) press ctrl+C to stop celery and type celery worker -A task_queue.celery --loglevel=info --pool=solo -Q generic -n two

### Run in local host

1) git clone backend repo
2) install requirements.txt
3) install mongodb
4) 1st terminal run python app.py
5) 2nd terminal run celery worker -A task_queue.celery --loglevel=info --pool=solo -n one
6) 3rd terminal run celery beat -A task_queue.celery --loglevel=info
7) 4rth terminal run celery worker -A task_queue.celery --loglevel=info --pool=solo -Q generic -n two

# Frontend repo Documentation

```
frontend
└─ twitter-scraping-frontend
   ├─ .dockerignore
   ├─ .env
   ├─ docker
   │  ├─ Dockerfile
   │  ├─ nginx.conf
   │  └─ nginxconfig
   │     ├─ general.conf
   │     └─ security.conf
   ├─ docker-compose.dev.yml
   ├─ docker-compose.prod.yml
   ├─ docker-compose.yml
   ├─ Dockerfile
   ├─ nginx
   │  └─ nginx.dev.conf
   ├─ nginx.conf
   ├─ package-lock.json
   ├─ package.json
   ├─ public
   │  ├─ favicon.ico
   │  ├─ index.html
   │  ├─ logo192.png
   │  ├─ logo512.png
   │  ├─ manifest.json
   │  ├─ robots.txt
   │  ├─ unnamed.png
   │  └─ unnamedr.png
   ├─ README.md
   └─ src
      ├─ App.js
      ├─ App.test.js
      ├─ components
      │  ├─ authentication
      │  │  ├─ LoginCard.jsx
      │  │  └─ LoginCard.module.css
      │  ├─ cronjob
      │  │  ├─ AddCronJobKeywordDialog.js
      │  │  ├─ ControlCronjob.js
      │  │  └─ Cronjobbar.js
      │  ├─ home
      │  │  ├─ MultipleChips.jsx
      │  │  └─ ScrappingCard.jsx
      │  ├─ notification
      │  │  ├─ notificationtable.jsx
      │  │  └─ notificationtabs.jsx
      │  └─ TextFieldComponent.jsx
      ├─ index.css
      ├─ index.js
      ├─ logo.svg
      ├─ pages
      │  ├─ Cronjob.js
      │  ├─ Home.js
      │  ├─ Login.js
      │  ├─ Login.module.css
      │  └─ Notification.js
      ├─ reportWebVitals.js
      ├─ setupTests.js
      └─ utility
         ├─ AppBar.jsx
         ├─ DatePickerComponent.jsx
         └─ ProgressShow.jsx

```

## SRC :
 This folder contains all the react code.
### App.js:
 This file has all the routes which we can navigate to
I.e Login Page, Home Page, Notification Page, CronJob Page

### Pages:
 This folder contains all the pages.
- Login.js:
This file is rendered when we hit the /login URL. In this file, we check if the token is present or not, if it's present then it’s valid or not. if the token is not present or not valid we will route to the login component else we will route to the home page.
- Home.js:
This file checks if the token is valid or not. if it’s not valid it will route to the login page else it will route to the home page component.


- Notification.js:
This file checks if the token is valid or not. if it’s not valid it will route to the login page else it will route to the notification page component.
Cronjob.js:
This file checks if the token is valid or not. if it’s not valid it will route to the login page else it will route to the CronJob page component.

### Components:

- Authentication/LoginCard.jsx:

This file contains the login logic component it has two text fields and a login button on click of the login button it checks whether the user has entered the valid login credentials by hitting the backend API of login if it’s valid the token is saved in local storage and the user is routed to home page. If the credentials are not valid the alert is generated.

- cronjob/AddCronJobKeywordDialog.js:
 This file contains the logic of adding the new keyword in the cronjob list of keywords. This file contains the text field and two-button of add and cancel when the add button is clicked the backend API is hit with the text entered and it saves the text in the backend as well as in the cronjob list keyword.

- cronjob/ControlCronjob.js:
This file contains the switch from which we can control the cronjob functionality on and off. it hits the backend update API to update the on and off. it hits one more backend API when the page is rendered it gets the value (on/off) which is set to the switch.

- cronjob/Cronjobbar.js:
This file contains the controlcronjob component and AddCronJobKeywordDialog.js. It hits the backend API of getting all the cronjob keywords from the backend, the second API gets the next cronjob time. These two APIs are hit when the component is rendered first after. This file also contains the add button on which the AddCronJobKeywordDialog.js component is rendered.

- home/MultipleChips.jsx:
This file contains the logic of creating and deleting multiple chips using the text field. When the user presses the enter button on the text field it creates the new chip which is appended in the chip array.

- home/ScrappingCard.jsx:
This file contains the MultipleChips component and two date field components to set the starting date and ending date for scrapping. It also contains the start scrapping button which hits the backend api for starting the scrapping . if it correctly starts the scrapping the notification is also shown.

- notification/NotificationTable.jsx:
This file contains the table in which it hits the backend api on the basis of an array of keywords. The number of values in the array hits the backend api and gets the data and shows that in the table. the api is hit when the component is first rendered.

- notification/NotificationTabs.jsx:
This file contains the logic of two tabs. The pending and completed and it creates the Notification table component inside this file.

### Utility:

- Appbar.jsx:
This file contains the logic of navigating from one page to another i.e home, notification and cronjob.
DatePickerComponent.js:
As the name shows it used to select the date from the calendar.
- ProgressShow.jsx:
	The component is used when the api is hit and it’s returning the response. Before the response is shown the progressshow component is shown.

### .env:
	This contains the server we want to select either the backend on localhost or deployment backend.

### How to run the project on Local System:

1) First install node and npm on system
2) Git clone https://github.com/syedfaisalsaleeem/twitter-scraping-frontend
3) Cd twitter-scraping-frontend
4) Npm install
5) Npm start

### Important Links for installing Docker:

https://www.bmc.com/blogs/mongodb-docker-container/

### Important Links for helping and fixing bugs:

- https://dev.to/efe136/how-to-enable-mongodb-authentication-with-docker-compose-2nbp
- https://www.twilio.com/blog/deploy-flask-python-app-aws

