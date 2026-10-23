import os
from urllib.parse import quote, quote_plus, urlencode

import requests

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, session, url_for

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
APP_ENV = os.getenv("APP_ENV", "dev")

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

# Configuración del cliente OAuth de Auth0
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


@app.context_processor
def variables_globales():
    # Hace que {{ entorno }} esté disponible en todos los templates
    return {"entorno": APP_ENV}


@app.route("/")
def home():
    return render_template("home.html", user=session.get("user"))


@app.route("/login")
def login():
    # Redirige al Universal Login de Auth0
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback")
def callback():
    # Auth0 vuelve aquí con un código; lo cambiamos por los tokens
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    params = {
        "returnTo": url_for("home", _external=True),
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
    }
    return redirect(
        f"https://{AUTH0_DOMAIN}/v2/logout?" + urlencode(params, quote_via=quote_plus)
    )


# ---- Aquí irán las funciones y rutas de los Pasos 3 y 4 ----
def token_management():
    """Pide a Auth0 un token para usar la Management API (credenciales M2M)."""
    respuesta = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "client_id": os.getenv("M2M_CLIENT_ID"),
            "client_secret": os.getenv("M2M_CLIENT_SECRET"),
            "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
            "grant_type": "client_credentials",
        },
        timeout=10,
    )
    respuesta.raise_for_status()
    return respuesta.json()["access_token"]


def url_usuario():
    """URL del usuario logueado en la Management API."""
    user_id = session["user"]["userinfo"]["sub"]  # ej: auth0|65ab...
    # quote() codifica el carácter | para que la URL sea válida
    return f"https://{AUTH0_DOMAIN}/api/v2/users/{quote(user_id, safe='')}"


@app.route("/perfil")
def perfil():
    if "user" not in session:
        return redirect(url_for("login"))

    # Leer el usuario completo desde la Management API
    headers = {"Authorization": f"Bearer {token_management()}"}
    respuesta = requests.get(url_usuario(), headers=headers, timeout=10)
    respuesta.raise_for_status()
    meta = respuesta.json().get("user_metadata", {})

    return render_template("perfil.html", user=session["user"]["userinfo"], meta=meta)


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=(APP_ENV == "dev"))
