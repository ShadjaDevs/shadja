## Shadja

### Setup

This app has been set up according to [digitalocean's setup guide for Flask and Nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04). This decision was made to get quickly started with development on a VM, but in future we might move to a app service like DigitalOcean's Apps.

The `nginx` server is set up to serve `shadja.py`'s `app` object. So follow any Flask development model, but let the `app` object in `shadja.py` be the app.

To restart the server with any changes you have made to the app, run

```
sudo systemctl restart shadja
```

### Plan
Refer to our [issue board](https://github.com/sddhrthrt/shadja/issues).