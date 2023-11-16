# Prediction of TV Show Popularity based on Sentiment Analysis
TV show popularity prediction using Sentiment analysis is one of the most interesting and challenging tasks

## Functional Requirements

- Admin Panel:
    a) Login: Admin need to login into the system by inputting the login credentials.
    b) Add Pages: Admin will add page details such as page name and page link (details of TV shows).
    c) Graphical Representation: Admin can generate 5 graph (Pie Chart & Bar Chart) based on Age, Gender, Location, Comment's Sentiment based on peoples review on each TV Show. This will help the users to know about the popular/trending TV shows.

- User Panel:
    a) User login’s to the system/application by using his/her user ID and password.
    b) User can edit his/her profile details along with display picture.
    c) User will post comments on the uploaded TV shows posted by the admin.
    d) User can also view comment of other users posted on different/uploaded TV shows.
    e) Users should be able to comment on stored TV shows only once. The system stores each comments of the users for further processing and find out the sentiments and their weightage and store it in database.
    f) The stored comments of the users will be analyzed by the system with the help of sentiwordnet dictionary and will rate/rank the show accordingly.
    g) User can easily decide whether the uploaded TV shows by the admin/ system are good, bad or worst based on sentiment classification.

### Installation Instructions
- Clone the project
- Install dependencies & activate virtualenv
- Create a virtualenv(optional)
- pip install -r requirements.txt

### Apply migrations
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### Create SuperUser/Admin 
```bash
python manage.py createsuperuser
```
### Running
```bash
python manage.py runserver
```
