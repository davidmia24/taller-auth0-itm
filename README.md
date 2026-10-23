# taller-auth0-itm

Aplicación web en Flask que usa **Auth0** para el inicio de sesión y la **Management API** de Auth0 para leer y guardar datos adicionales del usuario en su `user_metadata`.

## Funcionalidades

- Login y logout con el Universal Login de Auth0 (OAuth 2.0 / OpenID Connect).
- Página de perfil con un formulario prellenado con el `user_metadata` del usuario.
- Guardado de los datos del formulario en Auth0 mediante la Management API (`PATCH /api/v2/users/{id}`):
  - Tipo de documento
  - Número de documento
  - Dirección
  - Teléfono

## Tecnologías

- Python 3 + Flask
- Authlib (cliente OAuth)
- Requests (llamadas a la Management API)
- python-dotenv (variables de entorno)

## Estructura

```
├── app.py              # Rutas y lógica de la aplicación
├── requirements.txt    # Dependencias
├── .env.example        # Plantilla de variables de entorno
├── static/
│   └── estilos.css
└── templates/
    ├── home.html
    └── perfil.html
```

## Configuración en Auth0

1. **Regular Web Application** (para el login):
   - Allowed Callback URLs: `http://localhost:3000/callback`
   - Allowed Logout URLs: `http://localhost:3000`
2. **Machine to Machine Application** (para la Management API):
   - Autorizada para la API `Auth0 Management API`.
   - Permisos: `read:users`, `update:users`.

## Instalación

```bash
git clone <url-del-repositorio>
cd taller-auth0-itm

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```env
APP_ENV=dev
AUTH0_DOMAIN=tu-tenant.us.auth0.com
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
APP_SECRET_KEY=
M2M_CLIENT_ID=
M2M_CLIENT_SECRET=
```

| Variable | Descripción |
| --- | --- |
| `APP_ENV` | Entorno de ejecución (`dev` activa el modo debug). |
| `AUTH0_DOMAIN` | Dominio del tenant de Auth0. |
| `AUTH0_CLIENT_ID` / `AUTH0_CLIENT_SECRET` | Credenciales de la Regular Web Application. |
| `APP_SECRET_KEY` | Clave para firmar la sesión de Flask. |
| `M2M_CLIENT_ID` / `M2M_CLIENT_SECRET` | Credenciales de la aplicación Machine to Machine. |

> El archivo `.env` está en `.gitignore` y **no debe subirse** al repositorio.

## Ejecución

```bash
python app.py
```

La aplicación queda disponible en http://localhost:3000.

## Rutas

| Ruta | Método | Descripción |
| --- | --- | --- |
| `/` | GET | Página de inicio. |
| `/login` | GET | Redirige al login de Auth0. |
| `/callback` | GET | Recibe la respuesta de Auth0 y guarda la sesión. |
| `/logout` | GET | Cierra la sesión local y en Auth0. |
| `/perfil` | GET | Muestra el formulario con el `user_metadata` actual. |
| `/perfil` | POST | Guarda los datos del formulario en el `user_metadata`. |
