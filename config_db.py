import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
SECRET_KEY = os.urandom(32)
cert = {
        "type": "service_account",
        "project_id": "firestore491test",
        "private_key_id": "5e88bfeaa543c68726e84cd605cafc1b739a238e",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxzQxnf6ARarYE\nTnTMUB5ZE0Lf19/qOe9ygj5LC7enZzgMw9+YrQP6O7i/sEcIsjC/RDN8hYblSUTO\n0yHdorat226HgA5UNw8GRQ6JnM+7UVyTSIQrtYp0Ci3ITTeStAgg1iSLk9xjtijI\nlPQNBELESaO1SUMYtG/XikyYhwgEX0WIkq4ZemWEHLgk2fxvUAWxsREQjCtrTqJw\nMr4CqcO2tWs5nf2aYHz+SpHkxIjF5/0TyLlxCrmZUQQDpJDjCuP1mGe+1RSy+vgn\nJa4b0Wjd3HntWqiqnPwMpEtzvPjJ426MebpVO/GBZwxIL2Y4sb51khMjKU+vghce\n5MZ4JH/1AgMBAAECggEACzxfe8zjYyZgsT36AI1RlaRzdezQ8B7QJGbZo+luJiyO\nLLRWFXJdjXsnriloG8MS9ItNS6GuiB/MsttByR1GuQ7kWbi8bxL5ppZHmGep8vbt\nyDrta0uyH6ojAYTrraAl4VlW/uENrNluk1piX840n+3dZA/opw+D/9V0CLGDzq7R\ngSMzQIoNHFqFQNM23g14DfKapHJWJm45ybPjSenQpNn+od6+CKWRA92nPc4sfbMm\neq5kCpS76iEjOAu4Tqbc1EBlCxQY53Ou8aBTy/AKQFI6glXQ3cPkIqzms9wHzy1h\njo6Igq3butKEpk81xZg5373bO3qHCuePDB5nrWpIkQKBgQDrExjrhKV1MeS6XxEG\nzwHhfcSKc8OzYLa8RjQbKPAaEHOlHTLTvy0dRtLWzr51FMB3CXDY9ube9adaZ7+f\nYIXdZYG+efJAyhqxxE8xd7xEke4YdR/3Vp8OJ/imR503A2xZgAh8cohw2p90iCDV\nl0xKGtPRSRUWtxZJpSf29Jh2SQKBgQDBoMtMeN+Xn/jH0a+ikD5vKBuXVG6OL1lc\ngpffOThwNuwp0wXjZVjqXkK4Hx2UHffS0rA5rO8BAMAcMxfy0NuI27v2ecI46N7j\n/bHGRnIJG3iDXs3Lx3loV2TQjJmsX/9tkbTUmrJdWErTAkxvYw7DYoR2nqkJcKw3\nEprbVNGMTQKBgHZUBZ5ABf1pIQaDZhG0T/EOmslKnn8DttgsynvFbp7gGyZI/VXD\nDNWI2gaQySQsTvlcgjZkijA/HX+Pa9CxCJE6UEXuInhkg21qMKbo65bkkiIziuS4\n8JVyn2Ir+EJB8d9XaG4kRPPxyIQjJcv+PcOrn2Xg0MG/ZXOqs+RGmRwpAoGBAJTJ\nsm75Exe4XbtubcBFhzRzZYBL6QhpagmkcH+fwLa5/Y/GEGhEoKa3+Bz0DA6dWKow\nLCqlsKLcqMMCoAx+YbQw5abouU5x45TehZUO3OISsfCBETLd/XUocteuswe6XNUd\neg9FMHp6NkUfJw0Q2W9abN+Z29rdMfi/2y9fZgahAoGAH36dxNOIJiMMqEdr+YI2\nUD6KacA/0qhFUU63Nx6m7YZ58rkRFLTV1F6qNiZn7QVFgtP4TJlB+m4GruF5V6Y/\nOshSHQ7hU7zmUOsO53aJVe04iLhXdbDTwd2aezBPL7cTHhL4AZ73iFvXlySIaXQl\ni8kF+jnJIddr/H7c7SZ2apw=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-7l56g@firestore491test.iam.gserviceaccount.com",
        "client_id": "112284953008835814355",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7l56g%40firestore491test.iam.gserviceaccount.com"
        }   
cred = credentials.Certificate(cert)
firebase_admin.initialize_app(cred)

db = firestore.client()