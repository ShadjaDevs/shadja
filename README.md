## Shadja

### Setup

This app has been set up according to [digitalocean's setup guide for Flask and Nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04). This decision was made to get quickly started with development on a VM, but in future we might move to a app service like DigitalOcean's Apps.

The app lives in the VM at `/home/ubuntu/src/shadja`. To get access to `ubuntu` user on VM, ask in #infra.

The `nginx` server is set up to serve `shadja.py`'s `app` object. So follow any Flask development model, but let the `app` object in `shadja.py` be the app.


### Development workflow

Make any edits wherever you prefer to edit code. Push changes to this repo. Follow Pull Requests workflow - create a Pull Request from your branch to master. Merge after peer review.

### Running locally

- Install mysql-server, libmysqlclient-dev, libpython3.8-dev
- set up your local mysql.
    - a user `shadja` with `<whatever>` password 
    - a database `shadja_dev`
    - `GRANT ALL PRIVILEGES` to `shadja` on `shadja_dev.*`
- Activate your virtualenv
- pip install -r requirements.txt
- run in shell: `export MYSQL_PASSWORD="<whatever>"`
- run in shell: `flask db init`
- `flask db migrate -m "initial migration"`
- `flask db upgrade`
- ...

This is where I'm at now.
Now, db is created, ideally poller should be able to run off of db and persist
all new found availabilities per pin to db. Should also be able to send 
notifications via email (but email sender is not implemented yet)

### Making changes to the model

If you make changes to the model, we should use database migrations to apply those
changes to models into the database schema. This allows us to keep existing data but
issue `ALTER TABLE` instructions and modify the database to bring it to the new 
schema, but automatically (well almost).

After making changes to model, with `MYSQL_PASSWORD` variable exported, and virtualenv
enabled:
- run `flask db migrate -m 'summary of changes to model'`
- Now look at the new migration generated in `migrations/versions`. The `upgrade` function
takes the existing database before your changes and brings it up to your changes. `downgrade`
function is reverse. Sometimes the automatic migration creater doesn't get all 
the changes accurately, so you may want to tinker around with the upgrade and downgrade functions.
This is especially useful if, for example, you have opinions on what the default value of newly
created column should be, or if you can just alter an existing column and don't have to necessarily
drop and create a column etc. Look up `SQLAlchemy migrations` for more details.
- Once you're confident about your migration, apply it: `flask db upgrade`. 
- Don't worry if it fails, it doesn't mess anything up. 
- You can always `flask db downgrade`, too. 
- `migrations` directory is not included in git history. This is because your local 
env's migration sequence could be different from production, and is different from a new deployment.



### Deployment

To update the server with any changes you have made to the app, 
- either check out your branch on the VM 
- or (if your changes are in master) update master branch in VM. 

Now, your code should be there in the VM at `/home/ubuntu/src/shadja`.

Then, run

```
sudo systemctl restart shadja
```

The website is running at http://143.110.252.209/

### Plan
Refer to our [issue board](https://github.com/sddhrthrt/shadja/issues).
