## Flask / SQLAlchemy App

### Installing Dependencies

```
pip install -r requirements.txt
```

### Running the App

To run the app, first run the `models.py` file directly to create the database tables:

```
$ python models.py
```

You only need to do this once, unless you change your model definitions (see below).

Then run the app itself:

```
$ flask run
```