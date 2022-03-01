## Modelo de Usuario Custom

Crearemos una app, `accounts` para gestionar el login, logout y singup.

### Modelo

Para crear nuestro modelo vamoa a extender `AbstractUser`. Simplemente añadimos los campos extras que queremos que tenga nuestra definición de usuario:

```py
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
```

`null=True` indica que en la base de datos admitiremos nulos en este campo. `blank=True` indica que en el formulario admitiremos que no se informe este campo.

### Vistas

Definimos la vista de `singup`, y reusamos las de login y logout. La vista se define como:

```py
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
```

- Usaremos un formulario en nuestra vista, que definiremos en `CustomUserCreationForm`
- En caso de exito derivamos al usuario a la url de _login_
- La plantilla que usamos es `registration/signup.html`

#### Formulario

Usamos los formularios estandard `UserCreationForm` y `UserChangeForm` como base, y los extendemos con los campos `username, email y age`. Notese como en el formulario se indica cual es el modelo - que sería nuestro modelo custom de usuarios. Por este motivo, al crear la vista, no se explicito el modelo, porque ya viene indicado en el formulario:

```py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            "username",
            "email",
            "age",
        )  # new


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "age",
        )  # new
```

### Plantillas

La plantilla tiene una definición _estandard_:

```html
{% extends "base.html" %}
{% load crispy_forms_tags %}
{% block title %}Sign Up{% endblock title%}

{% block content %}
<h2>Sign Up</h2>
<form method="post">{% csrf_token %}
    {{ form|crispy }}
    <button class="btn btn-success" type="submit">Sign Up</button>
  </form>
{% endblock content %}
```

- Usa un template `base.html`
- incluye el token _CSRF_
- incluye el _{{form}}_ en el bloque de contenido

### urls

Definimos la url para hacer el `singup` - pero no las de login, o logout, que se guiran definidas en la app estandard de django:

```py
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
```

### Administración

La administración de usuarios, además de poder hacerse en las vistas de la app, se puede hacer en las páginas de administración. Para que las páginas de administración _apunten_ a nuestro modelo tendremos que hacer alguna configuración en `admin.py`:

```py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "age",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),)


admin.site.register(CustomUser, CustomUserAdmin)
```

-  `admin.site.register(CustomUser, CustomUserAdmin)`. Indicamos que el modelo `CustomUser` se tiene que administrar con la clase `CustomUserAdmin`
- `class CustomUserAdmin(UserAdmin)`. La clase `CustomUserAdmin` hereda de `UserAdmin`, que es la clase base que administra usuarios en django
- Extendemos la clase indicando:
    - ``. El formulario que se tiene que usar
    
    ```py
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    ```

    - ``. El modelo que se tiene que emplear

    ```py
    model = CustomUser
    ```

    - ``. Los campos del modelo que se tienen que mostrar 

    ```py
    list_display = [
        "email",
        "username",
        "age",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("age",)}),)
    ```

### Configuración del proyecto

En la configuración del proyecto en `settings.py`, además de incluir la app que se encarga de la autenticación, indicamos cuales son las urls a las que derivar al usuario cuando se logee o se deslogee:

```ps
LOGIN_REDIRECT_URL = "home"  # new
LOGOUT_REDIRECT_URL = "home"  # new
```

Finalmente en el `urls.py` del proyecto, indicamos que la url de `accounts` pase a ser nuestr app `accounts`. Notese que la resolución se hace de arriba a bajo, de modo que la configuración por defecto, la que nos deriva a `django.contrib.auth` solo se usa si la de `accounts.urls` no resuelve la _request_. Cuando hacemos login o logout seguiremos usando `django.contrib.auth` y cuando hagamos singup `accounts.urls`:

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("pages.urls")),  # new
]