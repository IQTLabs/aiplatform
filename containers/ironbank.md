# Iron Bank

<a href="https://p1.dso.mil/#/products/iron-bank/">
  <img align="right" alt="ironbank logo" src="https://p1.dso.mil/img/Iron_Bank_Logo_LIGHT.468ac210.png" height="128" />
</a>

Platform One's repository for hardened & approved container images ( [product](https://p1.dso.mil/#/products/iron-bank/) | [pages](https://ironbank.dso.mil/) ).

It is 100% free but requires Platform One (P1) SSO account to make use of.

&nbsp;

## Create an Account

Register for a P1 SSO account here: https://login.dso.mil/register .

&nbsp;


## Web Login

Iron Bank is currently backed by an instance of the [Harbor](https://goharbor.io) registry.  To login, point your brower to the Iron Bank Harbor UI here: https://registry1.dso.mil/harbor .

Once there, click the `Login via OIDC Provider` button & use [your P1 SSO account](#create-an-account) to authenticate.

After that you're free to take the UI for a spin & browse available images.

&nbsp;


## Registry One Login

### 1. Lookup your CLI-specific credentials

<img align="right" alt="harbor credentials" src="../.images/harbor-credentials.png" width="384" />

Docker desktop is a CLI tool and so needs an automated (read: non-UI) way to login & pull images. Harbor provides authenticated users with a second, separate credential for doing just that: the "CLI secret".

In order to figure out what your personal "CLI secret" is you first need to log into the Iron Bank Harbor Web UI (as [above](#web-login)).

Then, pop open your "User Profile" and copy down your `Username`.

> _**Take note**_
>
> You need your **Username** specifically&mdash;trying to log docker into Iron Bank using Email will not work!

&nbsp;

### 2. Have Docker cache your credentials

Once you've pulled your credentials from the Harbor UI, docker can be granted access (in your name!) with a command like this:

```sh
docker login "registry1.dso.mil" -u <YOUR_USERNAME>
```

When prompted for your password, copy and paste your "CLI Secret". Docker will dump an auth file into your user home directory&mdash;`$HOME/.docker/config.json`&mdash;in a format that will be familiar to you if you've ever used [docker login](https://docs.docker.com/engine/reference/commandline/login/) before.

> _**Beware!**_
>
> The configuraitonf file may contain your personal credentials for interacting with Iron Bank and, if so, _could be used to impersonate you_.  Make sure to keep this file safe!

For details of how docker stores your credentials, see the docker [credentials store documentation](https://docs.docker.com/engine/reference/commandline/login/#credentials-store).

### 3. Have Docker erase your credentials

Docker will erase your credentials with a command like this:

```sh
echo "registry1.dso.mil" | docker-credential-desktop erase
```
