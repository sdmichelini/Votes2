# Votes #

This is an application that enables users to vote on a topic. A person in charge of the votes will be able to open and close the ballot, along with viewing the results. He will also be able to take attendance at the meeting where the voting will be conducted.

## Getting Started ##

### Prerequisites ###

Follow the _Before you begin_ section located [here](https://cloud.google.com/appengine/docs/python/gettingstartedpython27/creating-guestbook).


### Installing ###

 1. Clone this Repository
```
git clone
```
 2. Install Dependencies

* jQuery
```
bower install jquery
```

* Bootstrap 4
```
bower install bootstrap#v4.0.0-alpha.2
```

## Deployment ##

To run locally use the command `dev_appserver.py ./`

## Testing ##

To run the meeting unit tests run the following command from the root of the project.

```bash
python tests/meeting_test.py
```

## Backend Architecture ##

The backend is written in Python using the webapp2 framework and runs on the Google App Engine. It utilizes App Engine specific APIs for data storage and task queues.

### Models ###

Please refer to the models README in the `model` folder.

### Views ###

The views are Jinja HTML templates combined with jQuery for other operations.  

### Controllers ###

There are three main controller files for the app. There is the `index_controller.py` file for general user interaction, the `admin_controller.py` file for administrator interaction, and finally the `worker.py` file for task queue endpoints. These three files define all the incoming request handlers for the app.

## Authors ##

- sdmichelini

## License ##

This project is licensed under the MIT License.
