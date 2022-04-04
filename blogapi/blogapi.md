## Introducción

Se construya a partir de la base, de los _conceptos_ cubiertos en el proyecto `todo-api`. Vamos a incluir capacidades _CRUD_, _permisos_ y _autenticación_.

Lo que hemos hecho de partida en este proyecto es:
- Hemos creado un proyecto
- Hemos creado una app llamada posts
- Hemos registrado en el proyecto las aplicaciones posts y el rest_framework. Este último lo hemos configurado también - `REST_FRAMEWORK` -  
- Crear un modelo: Post. El modelo incluye un campo con una _foreign key_ a la tabla de usaurios
- Se registra el modelo _Post_ en la página de administración
- Se crean las urls, serializadores y vistas necesarias para exponer un listado de _Post_ y su detalla
- Hemos creado unos tests unitarios

Hemos usado los siguientes comandos. Hemos creado el proyecto, la aplicacion e inicializado la base de datos:

```ps
mkdir blogapi
cd blogapi
django-admin startproject config .
python ./manage.py startapp posts
python ./manage.py migrate
```

Una vez creado el modelo _Posts_, creamos una archivo con los cambios, y los aplicamos:

```ps
python ./migrate.py makemigrations posts
python ./manage.py migrate
```

Creamos un usuario para poder acceder a la aplicación admin - el usuario se crea en la base `Users`:

```ps
python ./manage.py createsuperuser
```

Ejecutamos los tests unitarios:

```ps
python ./manage.py test
```

Arrancamos el proyecto:

```ps
python ./manage.py runserver 8080
```

y accedemos a la url `http://127.0.0.1:8000/admin/`

## Permisos

Podemos añadir más usuarios usando la página administrativa del proyecto `http://127.0.0.1:8000/admin/`. Para extender para hacer login o logout con las apis, incluimos la siguiente ruta al proyecto: 


```py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api-auth/', include('rest_framework.urls')), # administracion del rest framework
]
```

Recordemos que cuando añadimos el rest-framework incluimos esta configuración:

```py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
```

Esto significa que cualquiera tiene acceso a utilizar todos los end-points expuestos (listar, modificar y borrar). Se pueden configurar restricciones a nivel de proyecto, vista o modelo. A nivel de vista:

```py
from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer

#View for retrieving a queryset from a model
class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,) # indicamos que hay que estar autenticado para poder usar esta vista
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#View for retrieving, updating or deleting an entry in the model 
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,) # indicamos que hay que estar autenticado para poder usar esta vista
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

Ahora, es necesario estar autenticado para poder usar los endpoints expuestos en estas dos vistas. A nivel de proyecto el rest framework incorpora una serie de permisos:

Fortunately Django REST Framework ships with a number of built-in project-level permissions settings we can use, including:

- AllowAny - any user, authenticated or not, has full access
- IsAuthenticated - only authenticated, registered users have access
- IsAdminUser - only admins/superusers have access
- IsAuthenticatedOrReadOnly - unauthorized users can view any page, but only authenticated users have write, edit, or delete privileges

```py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # new
    ]
}
```

Siempre se aplica el permiso más restrictivo definido sobre un determinado objeto, independientemente del nivel al que se haya definido.

### Permiso custom

Para crear un permiso tenemos que extender la clase `BasePermission`:

```py
class BasePermission(object):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, 
obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
```

Sobre-escribimos el método `has_object_permission`:

```py
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Todo el mundo tiene permisos de lectura: GET, HEAD y OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo si el usuario es el autor del Post se puede manipular el registro
        return obj.author == request.user
```

Una vez definido el permiso lo podemos utilizar, por ejemplo, en las vistas:

```py
