from django.db import models

# Modelo para EPS
class eps(models.Model):
    codigo = models.CharField(max_length=20)
    nombre_eps = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_eps

# Modelo para Paciente
class paciente(models.Model):
    nombre_paciente = models.CharField(max_length=100)
    apellido_paciente = models.CharField(max_length=100)
    tipo_identificacion = models.CharField(max_length=100)
    numero_identificacion = models.BigIntegerField(default=0) 
    edad_paciente = models.IntegerField()
    genero_paciente = models.CharField(max_length=10)
    direccion_paciente = models.CharField(max_length=100)
    telefono_paciente = models.CharField(max_length=20)
    correo_paciente = models.EmailField(null=True, blank=True)
    tipo_sangre = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

# Modelo para EPS-Paciente con estado
class eps_paciente(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    eps = models.ForeignKey(eps, on_delete=models.CASCADE)

    ESTADOS = [
        ('activo', 'Usuario Activo'),
        ('inactivo', 'Usuario Inactivo'),
        ('bloqueado', 'Usuario Bloqueado'),
        
        ]
    
    estado = models.CharField(max_length=20,choices=ESTADOS,default='activo')
    
class historia_clinica(models.Model):   
    numero_historia = models.CharField(max_length=70, unique=True)
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    motivo_ingreso= models.CharField(max_length=500)
    motivo_salida = models.CharField(max_length=500, blank=True, null=True)
    
    
    def __str__(self):
        return self.numero_historia
    
