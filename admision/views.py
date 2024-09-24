from datetime import datetime
from django.shortcuts import render,get_object_or_404,redirect
from . models import paciente,eps,eps_paciente,historia_clinica

# Create your views here.

def listado_pacientes(request):
    pacientes = paciente.objects.all()
    return render(request, 'ventanas/paciente_listado.html', {'pacientes': pacientes})


def detalle_paciente(request, id):
    paciente_obj = get_object_or_404(paciente, id=id)
    return render(request, 'ventanas/paciente_detalle.html', {'paciente': paciente_obj})

def generar_numero_historia():
    # Obtener el último número de historia clínica
    ultimo_historia = historia_clinica.objects.order_by('-id').first()
    
    if ultimo_historia:
        numero_actual = ultimo_historia.numero_historia
    else:
        numero_actual = "AC001"  # Valor inicial

    # Validar que el número actual tenga al menos 3 caracteres
    if len(numero_actual) < 3:
        prefijo = "AC"
        numero = 1
    else:
        try:
            prefijo = numero_actual[:2]
            numero = int(numero_actual[2:]) + 1
        except (ValueError, IndexError):
            prefijo = "AC"
            numero = 1  # Valor por defecto si falla la conversión

    # Cambiar de prefijo si se llega al límite
    if numero > 999:
        numero = 1
        prefijo = siguiente_prefijo(prefijo)

    nuevo_numero = f"{prefijo}{numero:03}"
    return nuevo_numero

def siguiente_prefijo(prefijo):
    letras = list(prefijo)
    for i in reversed(range(len(letras))):
        if letras[i] == 'Z':
            letras[i] = 'A'
        else:
            letras[i] = chr(ord(letras[i]) + 1)
            break
    return ''.join(letras)

def agregar_paciente(request):
    if request.method == 'POST':
        # Obtener datos del formulario usando .get()
        num_historia = generar_numero_historia()
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        tipoid = request.POST.get('tipoid', '')
        numeroid = request.POST.get('numeroid', '')
        edad = request.POST.get('edad', '')
        genero = request.POST.get('genero', '')
        direccion = request.POST.get('direccion', '')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')
        tiposangre = request.POST.get('tiposangre', '')
        fecha = request.POST.get('fecha', '')
        eps_nombre = request.POST.get('eps', '') 
        motivo_in = request.POST.get('motivo_ingreso', '')
        motivo_sal = request.POST.get('motivo_salida', '')

        # Convertir edad a entero, si es necesario
        try:    
            edad = int(edad)
        except ValueError:
            edad = 0  # O manejar el error de otra manera
            
        # Convertir fecha a datetime
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        


        # Solo crear y guardar el paciente si todos los datos son válidos
        if all([nombre and apellido and tipoid and numeroid and edad and direccion and telefono and email and tiposangre and fecha]):
            pa = paciente(
                nombre_paciente=nombre, 
                apellido_paciente=apellido, 
                tipo_identificacion=tipoid, 
                numero_identificacion=numeroid, 
                edad_paciente=edad, 
                genero_paciente=genero, 
                direccion_paciente=direccion, 
                telefono_paciente=telefono, 
                correo_paciente=email, 
                tipo_sangre=tiposangre, 
                fecha_nacimiento=fecha
            )
            pa.save()
            
            #if numero_historia and motivo_in:
            historia = historia_clinica(
                    numero_historia=num_historia,
                    paciente=pa,
                    fecha_ingreso=datetime.now(),
                    motivo_ingreso=motivo_in,
                    motivo_salida=motivo_sal,
                )
            historia.save()
                
            
            # Crear o buscar la EPS
            if eps_nombre:
                eps_obj, created = eps.objects.get_or_create(nombre_eps=eps_nombre)  # Usamos get_or_create
                ps = eps_paciente(
                    paciente=pa,
                    eps=eps_obj,
                
                )
                ps.save()
            
            else:
                    return render(request, 'ventanas/agregar_paciente.html', {'error': 'El nombre de EPS es requerido.'})
            
            # Verificar si paciente se creó y renderizar la plantilla adecuada
            return render(request, 'ventanas/paciente_agregado.html', {'paciente': pa})
        else:
                # Puedes redirigir o mostrar un mensaje de error si paciente no se creó
                return render(request, 'ventanas/paciente_agregar.html', {'error': 'Error al agregar el paciente'})
    else:
            return render(request, 'ventanas/paciente_agregar.html')

def editar_paciente(request, id):
    paciente_obj = get_object_or_404(paciente, id=id)  # Obtener el paciente o devolver un 404

    if request.method == 'POST':
        # Obtener y validar los campos del formulario
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        try:
            edad = int(request.POST.get('edad', '0'))
            fecha_nacimiento = datetime.strptime(request.POST.get('fecha', ''), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            edad = paciente_obj.edad_paciente  # Mantener el valor anterior si hay error
            fecha_nacimiento = paciente_obj.fecha_nacimiento  # Mantener el valor anterior si hay error
        
        genero = request.POST.get('genero', '')
        tipoid = request.POST.get('tipoid', '')
        numeroid = request.POST.get('numeroid', '')
        direccion = request.POST.get('direccion', '')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')
        tiposangre = request.POST.get('tiposangre', '')
        
        # Actualizar los campos del paciente
        paciente_obj.nombre_paciente = nombre
        paciente_obj.apellido_paciente = apellido
        paciente_obj.edad_paciente = edad
        paciente_obj.genero_paciente = genero
        paciente_obj.tipo_identificacion = tipoid
        paciente_obj.numero_identificacion = numeroid
        paciente_obj.direccion_paciente = direccion
        paciente_obj.telefono_paciente = telefono
        paciente_obj.correo_paciente = email
        paciente_obj.tipo_sangre = tiposangre
        paciente_obj.fecha_nacimiento = fecha_nacimiento
        
        # Guardar los cambios
        paciente_obj.save()

        

    # Renderizar el formulario de edición con los datos del paciente prellenados
    return render(request, 'ventanas/paciente_editar.html', {'paciente': paciente_obj})

def buscar_paciente(request):
    if request.method == 'POST':
        busqueda = request.POST.get('busqueda', '')
        # Usar los nombres de los campos correctos con el modificador __icontains
        pacientes = paciente.objects.filter(
            nombre_paciente__icontains=busqueda
        ) | paciente.objects.filter(
            apellido_paciente__icontains=busqueda
        ) | paciente.objects.filter(
            numero_identificacion__icontains=busqueda
        )  
        return render(request, 'ventanas/paciente_listado.html', {'pacientes': pacientes})
    else:
        return render(request, 'ventanas/paciente_buscar.html')


def home(request):
    return render(request, 'ventanas/home.html')

