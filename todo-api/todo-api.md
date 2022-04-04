## Setup

Además del paquete de Django, el paquete tradicional que se ha usado para construir aplicaciones web, necesitamos instalar un framework REST:

```ps
pip install djangorestframework
```

Hay que instalar como una APP el restframework:

```py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # new
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",  # new
    "corsheaders",  # new
    # Local
    "todos.apps.TodosConfig",  # new
]
```

El restframework se configura añadiendo propiedades a `REST_FRAMEWORK`:

```py
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
}
```

Podemos ver la lista completa de opciones [aquí](https://www.django-rest-framework.org/api-guide/settings/).

## Crear APIs

### URLs

Para configurar la api no necesitamos ni templates ni views.  Necesitamos configurar `urls.py`, `views.py`, y `serializers.py`. Los archivos `views.py`, y `serializers.py` los crearemos manualmente.

En urls especificaremos las rutas como haríamos con una aplicación Django tradicional.

```py
urlpatterns = [
    path("<int:pk>/", DetailTodo.as_view(), name="todo_detail"),
    path("", ListTodo.as_view(), name="todo_list"),
]
```

### Serializador

El serializer es el componente que se encarga de transformar la información del modelo a un json - que devolverá la api; No devolvemos páginas/templates. El serializer es una clase que hereda de `serializers.ModelSerializer`, en el que especificamos el modelo que deseamos serializar y los atributos que queremos retornar (el id se crea automáticamente or Django, no hay que definirlo explicitamente en el modelo):

```py
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            "id",
            "title",
            "body",
        )
```

### Views

Finalmente las views. Las views que usaremos en este caso son las definidas en el _restframework_, y juegan un papel equivalente al que jugaban las vistas en el Django "normal": son el puente entre la url y el modelo.

```py
class ListTodo(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class DetailTodo(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
```

Con estas vistas podemos administrar los datos del modelo. Por un lado se exponen endpoints que permiten listar datos del modelo - lo que produce el queryset que se haya especificado, que en nuestro caso no tiene restricciones -, y actualizar/borrar datos.

### CORS

Usaremos `django-cors-headers` para implementar _CORS_. Es un middleware, y como tal tenemos que incorporarlo a la lista de APPs y de MIDDLEWARES:

```py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # new
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",  # new
    "corsheaders",  # new
    # Local
    "todos.apps.TodosConfig",  # new
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # new
    "corsheaders.middleware.CorsMiddleware",  # new
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

Añadimos tambien la configuración propiamente dicha de CORS:

```py
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8000',
)
```
