## CLI

Crea un proyecto. Crea el directorio con todo los archivos del proyecto:

```ps
django-admin startproject prueba
```

si queremos crear el proyecto, pero ya estamos dentro del directorio donde queremos que se cree:

```ps
django-admin startproject prueba .
```

Una vez tenemos un proyecto, podemos crear aplicaciones:

```ps
python .\manage.py startapp miapp
```

Podemos crear un escript de migracion - un script que traslada los cambios en nuestro modelo a la base de datos que estemos usando:

```ps
python .\manage.py makemigrations
```

con el escript creado podemos trasladar los cambios a la base de datos:

```ps
python .\manage.py migrate
```

podemos arrancar nuestro proyecto - en este ejemplo, lo arrancamos en el puerto `8080`:

```ps
python .\manage.py runserver 8080
```

podemos crear un usuario admisitrador de la ![consola de Django](http://127.0.0.1:8000/admin/):

```ps
python manage.py createsuperuser
```

si queremos ver más opciones de `manage.py` podemos hacer:

```ps
python .\manage.py help
```

## Project Setting

Creamos una app con:

```ps
python .\manage.py startapp miapp
```

Para que el proyecto reconozca la app tenemos que registrarla en la configuración del proyecto en `settings.py`:

```py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # new
    "django.contrib.staticfiles",
    "blog.apps.BlogConfig",  # new
    "accounts.apps.AccountsConfig",  # new
]
```

aqui hemos registrado las aplicaciones `blog` y `accounts`. Django procesa las aplicaciones de esta lista de _arriba a abajo_.

Tambien podemos encontrar dentro de las configuraciones:

- Hostname aceptados:

```py
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]  # new
```

- Middlewares. Aquí hemos añadido `whitenoise.middleware.WhiteNoiseMiddleware`:

```py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # new
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

- Donde encontrar la configuración de rutas del proyecto:

```py
ROOT_URLCONF = "django_project.urls"
```

- Ubicación de los templates que vamos a usar. Estamos indicandolo en `"DIRS": [str(BASE_DIR.joinpath("templates"))],`. En este caso estamos diciendo que hay un directorio llamado `templates` en el proyecto donde iremos a buscar las plantillas:

```py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR.joinpath("templates"))],  # new
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

- Base de datos. Indicamos que motor de base de datos, y los parametros asociados. En este caso estamos especificando `sqllite` y la ruta del archivo de `sqllite`:

```py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

- Configuración de archivos constantes/estáticos. Estamos indicando aquí cual es el directorio raiz y en que directorios poder encontrarlos - `STATIC_ROOT` y `STATICFILES_DIRS`. Tambien indicamos con que url estaremos diciendole a Django que tiene que recuperar un archivo estático - STATIC_URL`; Todos los archivos que en su url se refieran con `/static/` se buscarán aquí:

```py
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))  # new
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # new
```

- Como generar los autonumbers del modelo:

```py
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

- Las paginas a las que redirigir al usuario despues de hacer login y logout respectivamente:

```py
LOGIN_REDIRECT_URL = "home"  # new
LOGOUT_REDIRECT_URL = "home"  # new
```

## Project URLs
`
Incluimos la rutas de las dos aplicaciones que tiene nuestro proyecto, _accounts_ y _blog_. Usamos `include` para cargar las rutas:

```py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),  # new
    path("", include("blog.urls")),
]
```

## App URLs (Blog)

Definimos las URLs de la aplicación.

```py
from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,  # new
)

urlpatterns = [
    path("post/new/", BlogCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),  # new
    path("", BlogListView.as_view(), name="home"),
]
```

Vamos a destacar lo siguiente:

- Estamos usando una clase para definir la vista, en lugar de una función. Usamos el método `as_view()` para obtener la vista

- Cada url tiene un nombre, `name`, que podremos referenciar desde un template o página cuando queramos derivar la petición a esa ruta

- En alguna de las rutas estamos pasando parametros, especificamente estamos pasando un integer con el _id_ o primary key, _pk_: `<int:pk>`

Veamos como se han definido las vistas a las que nos estamos refiriendo en las urls.

## Views

Para crear las vistas vamos a usar clases, y especificamente clases incluidas en django:

- `ListView`. Lista un modelo. Especificamos el modelo y el nombre de la plantilla

```py
class BlogListView(ListView):
    model = Post
    template_name = "home.html"
```

- `DetailView`. Detalle de un modelo. Especificamos el modelo y el nombre de la plantilla. Cuando navegamos a esta vista especificamos el id del registro que queremos consultar, indicando _id_ o _pk_

```py
class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
```

- `CreateView`. Para crear una registro en la base de datos. Además de indicar el modelo y el nombre del template, especificamos con la propiedad `fields` los campos que se mostrarán en la vista. También hay que indicar que en este tipo de vista es la página a la que redirigir al usuario si al guardar el registro se produce un error o no. En este caso al no indicarlo explicitamente se redigirá al usuario al resultado del método `def get_absolute_url(self)` definido en el modelo:

```py
class BlogCreateView(CreateView):
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body"]
```

- `UpdateView`. Similar al caso anterior. Para navegar a esta vista tenemos que especificar el _id_ o el _pk_. Como en el caso anterior tenemos que indicar la vista a la que dirigir al usuario en caso de exito o fracaso. En este caso lo definimos de forma explicita:

```py
class BlogUpdateView(UpdateView):
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]
```

- `DeleteView`. La última de las vistas. Aquí estamos indicando explicitamente la ruta a la que derivar al usuario, pero en este caso usamos `reverse_lazy("home")`. 

```py
class BlogDeleteView(DeleteView):  # new
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
```

Cuando usamos un formulario _out-of-the-box_ de django - por ejemplo `UserCreationForm` -, estamos indicando indirectamente cual es el modelo - así que no se indica de forma explicita -, y la vista por defecto se tiene que cargar de forma _lazy_:

```py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
```

## Plantillas

Hemos configurado en el proyecto que todas las plantillas se guarden en un directorio a nivel de proyecto, `templates`. En las vistas que acabamos de ver, además de indicar el modelo, se ha indicado también el nombre de la plantilla.

Si vemos alguna de las plantillas

```html
{% extends "base.html" %}

{% block content %}
  {% for post in post_list %}
  <div class="post-entry">
    <h2><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></h2>
    <p>{{ post.body }}</p>
  </div>
  {% endfor %}
{% endblock content %}
```

- Podemos ver como extienden de una plantilla base:

```html
{% extends "base.html" %}
```

- define un bloque de contenido llamado `content`:

```html
{% block content %}

{% endblock content %}
```

- Podemos usar scripting y acceder a los datos dle modelo - que se especificara en la vista. En este ejemplo listamos el titulo de cada post, e incluimos un link a la url `post_detail` pasandole como argumento el _pk_ del post:

```html
  {% for post in post_list %}
  <div class="post-entry">
    <h2><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></h2>
```

En la base podemos:

```html
{% load static %}
<html>
  <head>
    <title>Django blog</title>
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400"
      rel="stylesheet">
    <link href="{% static 'css/base.css' %}" rel="stylesheet"s>
  </head>
  <body>
    <div>
      <header>
        <div class="nav-left">
          <h1><a href="{% url 'home' %}">Django blog</a></h1>
        </div>
        <div class="nav-right">
          <a href="{% url 'post_new' %}">+ New Blog Post</a>
        </div>
      </header>
      {% if user.is_authenticated %}
        <p>Hi {{ user.username }}!</p>
        <p><a href="{% url 'logout' %}">Log out</a></p>
      {% else %}
        <p>You are not logged in.</p>
        <a href="{% url 'login' %}">Log In</a> |
        <a href="{% url 'signup' %}">Sign Up</a>
      {% endif %}
    {% block content %}
    {% endblock content %}
    </div>
  </body>
</html>
```

- Importamos el contenido estático

```html
{% load static %}
```

- y lo utilizamos:

```html
<link href="{% static 'css/base.css' %}" rel="stylesheet"s>
```

- Incluimos links a otras urls

```html
<a href="{% url 'post_new' %}">+ New Blog Post</a>
```

- y definimos un lugar donde poder incluir el contenido 

```html
{% block content %}
{% endblock content %}
```

- Podemos usar scripting para controlar que se pinta, y acceder a información contenida en el modelo:

```html
{% if user.is_authenticated %}
    <p>Hi {{ user.username }}!</p>
    <p><a href="{% url 'logout' %}">Log out</a></p>
{% else %}
    <p>You are not logged in.</p>
    <a href="{% url 'login' %}">Log In</a> |
    <a href="{% url 'signup' %}">Sign Up</a>
{% endif %}
```

En las plantillas en las que se editan datos - posts - es una mejor práctica utilizar un token _anti cross site request forgery_:

```html
{% extends "base.html" %}

{% block content %}
<h1>New post</h1>
<form action="" method="post">{% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Save">
</form>
{% endblock content %}
```

Por último comentar que la instrucción `{{ form.as_p }}` lo que hace es pintar todos los datos de la vista en `<p\>` tags.

## Modelo

Django implementa un ORM para mapear el modelo que definamos a tablas en la base de datos. El modelo es una subclase de `models.Model`:

```py
class Post(models.Model):
    #Class atributes con los campos de la entidad
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
```

Hay dos métodos que tienen, como mejor práctica, que incluirse en todos los modelos:

- `__str__`. Proporciona una representación de un item del modelo
- `get_absolute_url`. Proporciona la ruta a la que dirigir al usuario por defecto. Este método se usa en las vistas estandard que proporciona Django - ver sección anterior - para dirigir al usuario tras realizar una acción - post - en un item. En este ejemplo usamos el método `reverse` para indicar el nombre de la vista/url a la que dirigirnos. Podemos pasar opcionalmente algún argumento - en el ejemplo pasamos un argumento llamado `pk` con el valor del atributo _pk_

En el modelo se definen los atributos de un item - al que añadiremos el atributo _pk_ o _id_, que contiene el _primary key_ de la entidad.

Cuando se hacen cambios en el modelo, para que estos cambios se trasladen _físicamente_ a la base de datos tenemos que en primer lugar trasladar los cambios a un script:

```ps
python .\manage.py makemigrations
```

con el escript creado podemos trasladar los cambios a la base de datos:

```ps
python .\manage.py migrate
```

### Configuración del pk

En `apps.py` tenemos parametros de configuración de la app. Por defecto se incluye esta configuración:

```py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
```

Lo que esta configuración hace es definir como `pk` o `id` en el modelo `blog` un campo que será autonumérico.

## Configuración de la App dentro del proyecto

En `admin.py` indicamos como se tiene que administrar la app dentro del proyecto. Aquí simplemente indicamos que la app se tiene que registrar en la vista administrativa de django:

```py
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```
![consola](./imagenes/consola.png)

## User Accounts

## Tests
