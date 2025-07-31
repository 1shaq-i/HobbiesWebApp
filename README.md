# Project Information

## Group Members

1.> `Siddharth Bahl`:- Was assigned to do back-end development and did back end along with the tests creation with a bit of front-end.

2.> `Mohammed Asif Ahmed`:- Was assigned to do back-end and did back-end.

3.> `Mohamed Ishaq Ahmed`:- Was assigned to do front-end and did back-end and front-end both.

4.> `Mohammed Faruk Patel`:- Was assigned to do front-end and did front-end.

## URL of the deployed application

The application can be found [through this link](https://group30-web-apps-ec22425.apps.a.comp-teach.qmul.ac.uk/).

## Username and password for the admin user

username :- admin 

password :- admin

## The username and passwords of 5 of the test users

We have created users ranging from `test1`, `test2`, `test3`, ..., `test20`. All of them have the password of `$$test$$12`, except for the user `test12`, which has the password of `$$test$$23`.

## Developed tests information

The three tests we have developed are located in `/api/tests/`. And they are:

1.> `test_filtered_friend_request_and_acceptance`: This tests the logging in of a user, filtering other users of similar hobbies by age and sending a friend request to the first resultant user. Futhermore, the user is then logged out and we login using the credentials of the user which has received the friend request and we accept it and assert some things.

2.> `test_profile_change`: This tests the logging in of a user and updating the profile in a `profile page` and asserting the presence of a `success` message. Furthermore, the user is then logged out and logged back in with the updated details.

3.> `test_signup_and_login`: This tests the creation of a new user and logging in with the newly created account.


## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Download this repo as a zip and add the files to your own private repo.

3. Install Pyhton dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

4. Create a development database:

    ```console
    $ python manage.py migrate
    ```

5. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

7. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

8. Open your browser and go to http://localhost:5173, you will be greeted with a template page.

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).

npm install pinia

pip install django-cors-headers

