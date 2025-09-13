from django.http import HttpResponse

def bienvenida(request):
    nombre=None
    apellido=None
    edad=None
    curso=None
    html="<h1>Bienvenido a la aplicación de gestión de clientes</h1>" \
    "<p>Esta es una aplicación CRUD para gestionar clientes.</p>" \
    "<table style='border:1px solid'>" \
    "<tr><th>Acción</th><th>Descripción</th></tr>" \
    "<tr><td>Crear</td><td>Agregar un nuevo cliente a la base de datos.</td></tr>" \
    "<tr><td>Leer</td><td>Ver la lista de clientes existentes.</td></tr>" \
    "<tr><td>Actualizar</td><td>Modificar la información de un cliente existente.</td></tr>" \
    "<tr><td>Eliminar</td><td>Eliminar un cliente de la base de datos.</td></tr>" \
    "</table>" \
    "<br>" \
    "<form method='get'>" \
    "<input type='text' name='nombre' placeholder='Saludar a...'/>" \
    "<input type='text' name='apellido' placeholder='Apellido'/>" \
    "<input type='number' name='edad' placeholder='Edad'/>" \
    "<input type='text' name='curso' placeholder='Curso'/>" \
    "<button type='submit'>Enviar datos</button>" \
    "</form>" \
    "<a href='/despedida'><button>Ir a despedida de APP</button></a>"
    return HttpResponse("¡Bienvenido a la aplicación de gestión de clientes!" + html)

def despedida(request):
    html="<h1>Gracias por usar la aplicación de gestión de clientes</h1>" \
    "<p>Esperamos que haya tenido una experiencia positiva.</p>" \
    "<a href='/saludo'><button>Volver al inicio</button></a>"
    return HttpResponse(html) 

def enviar_datos(request, nombre, apellido, edad, curso):
    html=f"<h1>Datos recibidos:</h1>"\
    f"<p>Nombre: {nombre}</p>" \
    f"<p>Apellido: {apellido}</p>"\
    f"<p>Edad: {edad}</p>"\
    f"<p>Curso: {curso}</p>"\
    
    return HttpResponse(html)

