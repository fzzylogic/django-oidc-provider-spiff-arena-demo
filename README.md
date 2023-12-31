# Demo using Django as SSO for Spiff-Arena

- [Django 5.0](https://www.djangoproject.com/)
- [django-oidc-provider](https://github.com/juanifioren/django-oidc-provider)
- Demo of SSO to [Spiff-Arena](https://github.com/sartography/spiff-arena)

## Quickstart

Set up test project:

    git clone https://github.com/fzzylogic/django-oidc-provider-spiff-arena-demo
    cd django-oidc-provider-spiff-arena-demo
    python -m venv lenv
    source lenv/bin/activate
    pip install --upgrade pip setuptools
    pip install -r requirements.txt
    cd mysite

Use an explicit IP to avoid a caveat when running the demo on actual
localhost but Spiff in Docker. The issue is that one needs to specify
'host.docker.internal' for Docker to know to reference the external
localhost, but Spiff will also then attempt to re-direct to
'host.docker.internal' for login, which won't work.

Add <YOUR_IP> into ALLOWED_HOSTS list in settings.py.

    python manage.py runserver <YOUR_IP>:8010

Browse to <YOUR_IP>:8010 and login with admin/admin.

Adjust docker-compose.yml / "SPIFFWORKFLOW_BACKEND_OPEN_ID_SERVER_URL"
to refer to <YOUR_IP> where Django is hosted.

Launch Docker based on docker-compose.yml config:

    docker-compose pull
    docker-compose up -d

    # If changes are made to docker-compose.yml
    docker compose stop
    docker-compose up --build -d

## Approximate Reproduction Steps

- Set up Django tutorial example: https://docs.djangoproject.com/en/5.0/intro/tutorial01/
- Set up django-oidc-provider: https://django-oidc-provider.readthedocs.io/en/master/sections/installation.html
  - Modified mysite/mysite/settings.py (all new settings added at
    bottom of file).
  - Added mysite/polls/oidc_provider_settings.py. This allows
    adjustments to django-oidc-provider defaults.
- Added basic manual login/logout. Built-in admin login/logout would
  also work. (views.py, urls.py, basic templates)

- Adjusted docker-compose.yml to use django-oidc-provider:

      SPIFFWORKFLOW_BACKEND_OPEN_ID_CLIENT_ID: "445155"
      SPIFFWORKFLOW_BACKEND_OPEN_ID_CLIENT_SECRET_KEY: "74c231a96717ef53063932c2900d4abc9953b2bf0d7542a2164d3495"
      SPIFFWORKFLOW_BACKEND_OPEN_ID_SERVER_URL: "http://<YOUR_IP>:8010/openid"

### File map (* means added or changed)

    │   db.sqlite3*
    │   manage.py
    │
    ├───mysite
    │   │   asgi.py
    │   │   settings.py*
    │   │   urls.py*
    │   │   wsgi.py
    │   │   __init__.py
    │
    └───polls
        │   admin.py
        │   apps.py
        │   models.py
        │   oidc_provider_settings.py*
        │   tests.py
        │   urls.py
        │   views.py*
        │   __init__.py
        │
        ├───migrations
        │       __init__.py
        │
        ├───templates
        │       index.html*
        │       login.html*
        │       logout.html*

## Issues

- Don't know how to apply perms to users. OpenID users can log in and
  are able to see some menu items, but I can't figure out how to grant
  Spiff group based perms to these users. Using 'sample-administration'
  from 'spiff-demo-process-models' repo and associating the username
  (returned by 'sub') with a group doesn't work. One guess is that
  this has to do with 'iss', since apparently taking it together with
  'sub' is the only reliable stable identifier (OID connect Spec 5.7),
  but I'm unclear about how to handle authorization for external
  providers.

- Currently can't log out of Spiff-Arena, because from Django 4.1+
  GET is deprecated as a logout method (django-oidc-provider.views.EndSessionView
  inherits from Django's LogoutView, as does Django admin logout and
  the example logout view) which is why clicking 'logout' in Spiff
  won't work (can confirm GET based logout works on Django 3.2).
  Ref: https://github.com/juanifioren/django-oidc-provider/issues/416

## Worked around issues

- Spiff-Arena requires 'claims' to include either 'preferred_username',
  'name' or 'given_name' (UserService.getPreferredUsername), however
  django-oidc-provider returns only 'nickname' by default when claims
  are enabled with setting OIDC_IDTOKEN_INCLUDE_CLAIMS. So
  'preferred_username' is added in the custom function referenced by
  setting OIDC_USERINFO.

- Spiff-Arena returns an error when any 'email' is specified,
  so set email to None in the OIDC_USERINFO function, overriding any
  email specified in the Django user.
