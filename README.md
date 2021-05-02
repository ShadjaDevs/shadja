## Shadja

### Setup

This app has been set up according to [digitalocean's setup guide for Flask and Nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04). This decision was made to get quickly started with development on a VM, but in future we might move to a app service like DigitalOcean's Apps.

The `nginx` server is set up to serve `shadja.py`'s `app` object. So follow any Flask development model, but let the `app` object in `shadja.py` be the app.


### Development Workflow

Make any edits wherever you prefer to edit code. Push changes to this repo. Follow Pull Requests workflow - create a Pull Request from your branch to master. Merge after peer review.


### Deployment

To update the server with any changes you have made to the app, either check out your branch on the VM or (if your changes are in master) update master branch in VM. (Essentially, have your code show up in the VM)

Then, run

```
sudo systemctl restart shadja
```

The website is running at http://143.110.252.209/

### Plan
Refer to our [issue board](https://github.com/sddhrthrt/shadja/issues).
