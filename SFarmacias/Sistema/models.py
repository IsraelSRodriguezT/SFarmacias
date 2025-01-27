from django.db import models
from enum import Enum
from django.utils.timezone import now

# Enumeradores:
class Rol(Enum):
    ADMINISTRATIVO = "administrativo"
    FARMACEUTICO = "FARMACEUTICO"

class TipoPago(Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"

# Clases:
class Persona(models.Model):
    # Atributos:
    cedula = models.CharField(max_length=10, unique=True, verbose_name='Cedula:')
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    class Meta:
        abstract = True

class Empleado(Persona):
    # Atributos:
    identificacion = models.CharField(max_length=7, unique=True, editable=False, null=True)
    salario = models.FloatField()
    rol = models.CharField(max_length=50, choices=[(tag.value, tag.name) for tag in Rol])
    # Metodos:
    def save(self, *args, **kwargs):
        if not self.identificacion:
            letra_nombre = self.nombre[0].upper()
            empleados = Empleado.objects.filter(identificacion__startswith=f"11F").count() + 1
            self.identificacion = f"11F{letra_nombre}{empleados:04d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nombre + ' | ' + self.rol

class Cliente(Persona):
    registro = models.OneToOneField('Registro',editable=False,null=True, unique=True, on_delete=models.CASCADE,
                                    related_name='cliente' )
    # Metodos:
    def save(self, *args, **kwargs):
        if not self.registro:
            self.registro = Registro.objects.create()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nombre + ' | ' + self.cedula

class Farmacia(models.Model):
    #Atributos:
    correo = models.CharField(max_length=100,unique=True)
    nombre = models.CharField(max_length=100)
    # Metodos:
    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    # Atributos:
    calle_principal = models.CharField(max_length=100, verbose_name="Calle PPrincipal")
    calle_secundaria = models.CharField(max_length=100, verbose_name="Calle secundaria")
    referencia = models.CharField(max_length=100, verbose_name="Referencia")
    class Meta:
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'
    # Metodos:
    def __str__(self):
        return f"Direccion: {self.calle_principal} y {self.calle_secundaria} | {self.referencia}"

class Sucursal(models.Model):
    #Atributos:
    numero = models.IntegerField(editable=False, unique=True, null=True)
    telefono = models.CharField(max_length=10)
    direccion = models.OneToOneField(Direccion, on_delete=models.CASCADE, related_name='sucursal')
    farmacia = models.ForeignKey(Farmacia, related_name='sucursales', on_delete=models.CASCADE)
    class Meta:
        verbose_name =  'Sucursal'
        verbose_name_plural = 'Sucursales'
    # Metodos:
    def save(self, *args, **kwargs):
        if not self.numero:
            sucursales = Sucursal.objects.count() + 1
            self.numero = sucursales
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.farmacia) + '[' + str(self.numero) + ']' + ' | ' + str(self.direccion)

class Inventario(models.Model):
    #Atributos:
    codigo = models.CharField(max_length=7,unique=True,editable=False)
    sucursal = models.OneToOneField(Sucursal, on_delete=models.CASCADE, related_name="inventario")
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.codigo:
            inventarios = Inventario.objects.count() + 1
            self.codigo = f"{inventarios:06d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.sucursal) + ' | ' + self.codigo

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cantidad = models.PositiveIntegerField()
    codigo = models.CharField(max_length=7,unique=True,editable=False)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    precio = models.FloatField()
    inventario = models.ForeignKey(Inventario, related_name='medicamentos', on_delete=models.CASCADE)
    # Metodos:
    def save(self, *args, **kwargs):
        if not self.codigo:
            medicamentos = Medicamento.objects.count() + 1
            self.codigo = f"{medicamentos:06d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.nombre + ' | ' + str(self.precio) + ' | ' + str(self.inventario)

class Pedido(models.Model):
    cantidad = models.PositiveIntegerField(default=1)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    venta = models.ForeignKey('Venta', related_name='pedidos', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos' )
    sucursal = models.ForeignKey(Sucursal,on_delete=models.CASCADE)
    traer_de_otra_sucursal = models.BooleanField(editable=False,default=False)
    #Metodos:
    def verificar_inventario(self):
        inventario_actual = self.sucursal.inventario
        medicamento = self.medicamento
        if inventario_actual.medicamentos.filter(id=medicamento.id, cantidad__gte=self.cantidad).exists():
            return True, inventario_actual
        otras_sucursales = Sucursal.objects.exclude(id=self.sucursal.id)
        for sucursal in otras_sucursales:
            inventario = sucursal.inventario
            if inventario.medicamentos.filter(id=medicamento.id, cantidad__gte=self.cantidad).exists():
                self.traer_de_otra_sucursal = True
                self.save()
                return False, inventario
        return False, None

    def __str__(self):
        return str(self.cliente) + ' | ' + str(self.venta) + ' | ' + str(self.medicamento)

class Venta(models.Model):
    codigo = models.CharField(max_length=7,unique=True,editable=False)
    fecha = models.DateField(default=now)
    total = models.FloatField(editable=False, null=True)
    tipo_pago = models.CharField(max_length=50, choices=[(tag.value, tag.name) for tag in TipoPago])
    registro = models.ForeignKey('Registro', on_delete=models.CASCADE, related_name='ventas')
    # Metodos:
    def save(self, *args, **kwargs):
        if not self.codigo:
            ventas = Venta.objects.count() + 1
            self.codigo = f"{ventas:06d}"
        self.total = round(self.calcular_total(), 2)
        super().save(*args, **kwargs)

    def calcular_total(self):
        total = 0
        for pedido in self.pedidos.all():
            total += pedido.cantidad * pedido.medicamento.precio
        return total

    def __str__(self):
        return self.codigo + ' | ' + str(self.fecha)

class Registro(models.Model):
    def __str__(self):
        return str(self.cliente)
