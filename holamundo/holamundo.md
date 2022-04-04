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

Vamos a incluir funciones de autenticación empleando el modelo incluido con Django - en la siguiente aplicacion veremos como usar un modelo de autenticación custom. Las funciones que emplearemos son:

- login
- logout
- sing-up

Añadimos a las urls del proyecto las rutas de la app `accounts`:

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),  # new
    path("", include("blog.urls")),
]
```

Creamos en la app `accounts` una vista para registrar un usuario, usando una vista generísca `CreateView`, indicando que se use el formulario estandar `UserCreationForm` - con esto indirectamente estamos ya indicando que se use el modelo de autenticacion -, y especificando la ruta a la que navegar después de que un usuario se registre - se usa `reverse_lazy` en todas las vistas `django.views.generic`:

```py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
```

y la url:

```py
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
```

El template se define de la misma manera que hemos definido el resto de templates:

```html
{% extends "base.html" %}

{% block content %}
<h2>Sign Up</h2>
<form method="post">{% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign Up</button>
</form>
{% endblock content %}
```

Para hacer el login :

_As the LoginView documentation notes, by default Django will look within a templates directory called registration for a file called login.html for a log in form. So we need to create a new directory called registration and the requisite file within it._

Esto es, tenemos que colocar un template en `registration\login.html`:

```html
{% extends "base.html" %}

{% block content %}
<h2>Log In</h2>
<form method="post">{% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Log In</button>
</form>
{% endblock content %}
```

En el template que usamos en todas las pantallas, incluimos los links para hacer login, logount, y podemos validar si el usuario esta o no logeado:

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

## Static Files

Previously, we configured our static files by creating a dedicated static folder, pointing STATICFILES_DIRS to it in our config/settings.py file, and adding {% load static %} to our base.html template. But since Django won’t serve static files in production, we need a few extra steps now.

The first change is to use Django’s collectstatic command which compiles all static files throughout the project into a singe directory suitable for deployment. Second, we must set the STATIC_ROOT configuration, which is the absolute location of these collected files, to a folder called staticfiles. And third, we need to set STATICFILES_STORAGE, which is the file storage engine used by collectstatic.

```py
# config/settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles')) # new
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' # new
```

and in the CLI run:

```ps
python manage.py collectstatic
```

If you look at your project folder now you’ll see there’s a new staticfiles folder that contains admin and css folders. The admin is the built-in admin’s static files, while the css is the one we created.

While there are multiple ways to serve these compiled static files in production, the most common approach–and the one we will use here–is to introduce the WhiteNoise package.

## Tests

Para definir los tests creamos una clase que herede de `TestCase` - hay otra clase, SimpleTestCase, que podemos usar en aquellos casos en los que no haya base de datos.

Para inicializar los tests usamos el método estático `setUpTestData`:

```py
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )

        cls.post = Post.objects.create(
            title="A good title",
            body="Nice body content",
            author=cls.user,
        )
```

En este test estamos creando datos en la base de datos que usaremos para la prueba, y que serán eliminados - automáticamente - al concluir el test:

- `get_user_model()` accede al modelo _built-in_ de usuarios
- `get_user_model().objects.create_user` crea un usuario en la base de datos de usuarios
- `Post.objects.create` crea un objeto en el modelo `Posts` que hemos definido en `models.py`

Cada caso de prueba se define en un mátodo que se llamara con el prefijo `test_`. A continuación podemos ver un resume de operaciones típicas a incluir en un caso de test:

- Assertions

```py
self.assertEqual(self.post.title, "A good title")
self.assertEqual(self.post.get_absolute_url(), "/post/1/")
```

- Llamadas get, usando una uri o utilizando el nombre de la url - con `reverse`. También podemos ver como pasar argumentos: 

```py
response = self.client.get("/")
self.assertEqual(response.status_code, 200)

response = self.client.get(reverse("home"))
self.assertContains(response, "Nice body content")
self.assertTemplateUsed(response, "home.html")

response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
```

- Llamadas post, pasando un payload, o un payload y argumentos:

```py
response = self.client.post(
    reverse("post_new"),
    {
        "title": "New title",
        "body": "New text",
        "author": self.user.id,
    },
)
response = self.client.post(
    reverse("post_edit", args="1"),
    {
        "title": "Updated title",
        "body": "Updated text",
    },
)
```

## Mixin

Con los mixin implementamos herencia múltiple en Django. Tenemos mixins incluidos en las librerías de Django, pero tambien podemos crear nuuestros propios mixins. Por ejemplo, si en la definición de las vistas incluimos `LoginRequiredMixin`, lo que estamos obligando es que esa vista solo se pueda acceder a la vista si estamos logeados:

```py
class ArticleDetailView(LoginRequiredMixin, DetailView):  # new
    model = Article
    template_name = "article_detail.html"
```

Con esta medida podemos cambiar nuestro modelo, y en lugar de especificar al crear un articulo quien es su autor, podemos informar el atributo automáticamente con los datos del usuario logeado:

```py
class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
```

En este mixin hemos definido la lógica que cheuquee que el usuario este autenticado. Indicar que el mro va de izquierda a derecha, así que los mixin los colocaremos a la derecha de la declaración. Otro mixin que vamos a utilizar es `UserPassesTestMixin`. Este le usaremos para aplicar la autorización a nuestra aplicación.

```py
class UserPassesTestMixin(AccessMixin):
    """
    Deny a request with a permission error if the test_func() method returns
    False.
    """

    def test_func(self):
        raise NotImplementedError(
            '{} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
        )
```

El método `test_func` tiene que ser _sobre-escrito_. Por ejemplo, para evitar que solo el autor de un articulo pueda modificarlo, bastaría con hacer:

```py
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # new
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user
```

Nótese como solo hemos tenido que _sobreescribir_ el método.

## Extender el modelo

Vamos a incluir una nueva entidad a nuestro modelo - _Comments_ - de modo que podamos añadir comentarios a los artículos. 

```py
class Comment(models.Model):  # new
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
```

Un comentario tiene dos foreign keys, una al autor del comentario, y la otra a los árticulos.

Para poder administrar los datos de este modelo, __añadimos el modelo a la aplicación de administración__:

```py(admin.py)
admin.site.register(Comment)
```

Si queremos mostrar con cada árticulo todos los comentarios relacionados, podemos hacerlo con _inlines_. Esta es una feature administrativa, que podemos usar en la vista de administración. Hay dos tipos de inlines atendiendo a como se visualiza la información:

- Tabular

```py
class CommentInline(admin.TabularInline):  # new
    model = Comment
```

- Stack

```py
class CommentInline(admin.StackedInline): # new
    model = Comment
```

Los inlines los especificamos en el modelo administrativo:

```py
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
```

Por último, hay que especificar este modelo administrativo cuando registremos el modelo de artículos:

```py
admin.site.register(Article, ArticleAdmin)
```

### Templates

Para que la información relacionada se incluya en las plantillas hacemos referencia a los comentarios relacionados con `article.comment_set.all`:

```html
<hr>
<h4>Comments</h4>
{% for comment in article.comment_set.all %}
  <p>{{ comment.author }} &middot; {{ comment }}</p>
{% endfor %}
<hr>
```
