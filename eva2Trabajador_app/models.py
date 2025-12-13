from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum


# -------------------------------------------------
# Validación RUT (Módulo 11)
# -------------------------------------------------
def validar_rut_mod11(value):
    # Asegura que es string y elimina espacios
    rut = str(value).strip().replace(".", "").upper()

    # Debe venir con guion
    try:
        cuerpo, dv = rut.split("-")
    except ValueError:
        raise ValidationError("Formato RUT inválido. Debe incluir guion y dígito verificador.")

    # Solo números en el cuerpo
    if not cuerpo.isdigit():
        raise ValidationError("Formato RUT inválido. El cuerpo debe ser numérico.")

    # Calcular DV con módulo 11
    reversed_digits = list(map(int, reversed(cuerpo)))
    factors = [2, 3, 4, 5, 6, 7]

    s = 0
    fi = 0
    for d in reversed_digits:
        s += d * factors[fi]
        fi = (fi + 1) % len(factors)

    resto = s % 11
    dv_calc = 11 - resto

    if dv_calc == 11:
        dv_esperado = "0"
    elif dv_calc == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_calc)

    # Comparar DV esperado con DV ingresado
    if dv_esperado != dv:
        raise ValidationError("RUT inválido según módulo 11.")



# -------------------------------------------------
# Modelo AFPs
# -------------------------------------------------
class Afps(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    # rúbrica: porcentaje de descuento sobre sueldo base/bruto
    descuento = models.DecimalField(max_digits=5, decimal_places=2)  # Ej: 11.45

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "afps"


# -------------------------------------------------
# Modelo Trabajador (AFP como CharField, NO FK)
# -------------------------------------------------
class Trabajador(models.Model):
    # rúbrica: sin puntos, con guion y dígito verificador
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    base = models.IntegerField()
    # rúbrica: campo texto, validado contra tabla Afps
    afp = models.CharField(max_length=50)

    def clean(self):
        # Validar RUT
        validar_rut_mod11(self.rut)

        # Validar existencia de AFP
        from .models import Afps  # Importar aquí para evitar dependencia circular
        if not Afps.objects.filter(nombre=self.afp).exists():
            raise ValidationError("La AFP indicada no existe en el sistema.")
    def __str__(self):
        return f"{self.rut} - {self.nombre}"

    class Meta:
        db_table = "trabajador"


# -------------------------------------------------
# Modelo Descuentos
# -------------------------------------------------
class Descuentos(models.Model):
    rut = models.CharField(max_length=10)
    fecha = models.DateField()
    concepto = models.CharField(max_length=100)
    monto = models.IntegerField()

    def clean(self):
        # Validar existencia del trabajador asociado
        if not Trabajador.objects.filter(rut=self.rut).exists():
            raise ValidationError("El RUT indicado no pertenece a ningún trabajador.")

    def __str__(self):
        return f"{self.rut} - {self.concepto}"

    class Meta:
        db_table = "descuentos"


# -------------------------------------------------
# Modelo Liquidaciones
# -------------------------------------------------
class Liquidaciones(models.Model):
    rut = models.CharField(max_length=10)
    mes = models.IntegerField()
    anio = models.IntegerField()

    sbase = models.IntegerField(default=0)
    sbruto = models.IntegerField(default=0)
    desc_afp = models.IntegerField(default=0)
    descuentos = models.IntegerField(default=0)
    descuentos_totales = models.IntegerField(default=0)
    sueldo_liquido = models.IntegerField(default=0)

    class Meta:
        unique_together = ("rut", "mes", "anio")

    def calcular_campos(self):
        from .models import Trabajador, Afps, Descuentos

        # 1. Validar existencia de trabajador
        try:
            t = Trabajador.objects.get(rut=self.rut)
        except Trabajador.DoesNotExist:
            raise ValidationError({"rut": "El RUT no existe en la tabla Trabajador."})

        self.sbase = t.base
        self.sbruto = t.base  # En la pauta el sueldo bruto = base

        # 2. AFP
        try:
            afp = Afps.objects.get(nombre=t.afp)
        except Afps.DoesNotExist:
            raise ValidationError({"rut": "La AFP asociada al trabajador no existe en Afps."})

        porcentaje = float(afp.descuento)
        self.desc_afp = int(self.sbase * (porcentaje / 100))

        # 3. Descuentos del mes y anio
        total_desc = Descuentos.objects.filter(
            rut=self.rut,
            fecha__year=self.anio,
            fecha__month=self.mes
        ).aggregate(total=Sum("monto"))["total"] or 0

        self.descuentos = int(total_desc)
        self.descuentos_totales = self.desc_afp + self.descuentos
        self.sueldo_liquido = self.sbruto - self.descuentos_totales

    def save(self, *args, **kwargs):
        self.calcular_campos()
        super().save(*args, **kwargs)
