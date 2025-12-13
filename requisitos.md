\# Evaluación 3 Backend – Requisitos

\# Evaluación 3 Backend – Requisitos



Proyecto: Sistema de liquidaciones de sueldo

Alumno: Jorge López

Continuación de Evaluación 2.



\## 1. Consideraciones generales



\- Reutilizar el proyecto de la Evaluación 2 (modelos, BD, lógica de liquidaciones).

\- Base de datos MySQL/MariaDB.

\- Crear superusuario:

&nbsp; - usuario: Eva3

&nbsp; - contraseña: Evaluacion3

\- Mantener funcionamiento actual de:

&nbsp; - AFP

&nbsp; - Trabajadores

&nbsp; - Descuentos

&nbsp; - Liquidaciones (cálculo automático en el modelo)



\## 2. Nueva app para la API



\- Crear una nueva app Django llamada \*\*Eva3Api\*\*.

\- Esta app contendrá:

&nbsp; - Serializers de Django REST Framework.

&nbsp; - Vistas API para exponer datos en JSON.

&nbsp; - Manejo de autenticación por token.



\## 3. Requisitos de la API REST



Usar \*\*Django REST Framework\*\*:



\- Configurar DRF en `settings.py`.

\- Crear serializers para:

&nbsp; - Trabajador

&nbsp; - Liquidaciones



Autenticación:



\- Implementar \*\*Token Authentication\*\* (DRF TokenAuth).

\- Las APIs deben requerir token.



Endpoints mínimos:



1\. \*\*Datos personales del trabajador por RUT\*\*

&nbsp;  - Método: GET

&nbsp;  - URL sugerida: `/api/trabajador/<rut>/`

&nbsp;  - Devuelve datos del trabajador y su AFP.



2\. \*\*Liquidación de un mes específico\*\*

&nbsp;  - Método: GET

&nbsp;  - URL sugerida: `/api/liquidacion/<rut>/<anio>/<mes>/`

&nbsp;  - Devuelve la liquidación (si existe) del trabajador, año y mes especificados.



3\. \*\*Historial de liquidaciones\*\*

&nbsp;  - Método: GET

&nbsp;  - URL sugerida: `/api/liquidacion/historial/<rut>/?desde=AAAA-MM\&hasta=AAAA-MM`

&nbsp;  - Devuelve lista de liquidaciones del rango de meses/años.



Requisitos generales:



\- Respuestas en formato JSON.

\- Manejar errores:

&nbsp; - Trabajador no encontrado.

&nbsp; - Liquidación no encontrada.

&nbsp; - Rango de fechas inválido.

&nbsp; - Token inválido o ausente.



\## 4. Consumo de API externa



\- Consumir API de indicadores económicos (ej: `https://mindicador.cl/api/dolar`).

\- Crear vista que consulte el valor del dólar del día.

\- Exponer esta información:

&nbsp; - En una vista web (template simple) y/o

&nbsp; - En un endpoint JSON dentro de Eva3Api.



\## 5. Cliente de escritorio en Python



\- Aplicación de escritorio (por ejemplo, Tkinter).

\- Debe permitir:

&nbsp; 1. Consultar datos del trabajador por RUT.

&nbsp; 2. Consultar liquidación de un mes/año específico.

&nbsp; 3. Consultar historial de liquidaciones.

\- Debe consumir la API Django usando `requests`.

\- Debe usar autenticación por token.

\- Manejar errores y mostrar mensajes claros al usuario.



\## 6. Entregables



\- Proyecto Django completo.

\- Script SQL de la base de datos.

\- Cliente de escritorio en Python.

\- Archivo `requirements.txt` actualizado.

\- Manual breve de instalación y ejecución.

\- Video (6–15 minutos) explicando:

&nbsp; - Estructura del proyecto.

&nbsp; - Configuración BD.

&nbsp; - Uso de la API con Postman.

&nbsp; - Funcionamiento del cliente de escritorio.



Proyecto: Sistema de liquidaciones de sueldo

Alumno: Jorge López

Continuación de Evaluación 2.



\## 1. Consideraciones generales



\- Reutilizar el proyecto de la Evaluación 2 (modelos, BD, lógica de liquidaciones).

\- Base de datos MySQL/MariaDB.

\- Crear superusuario:

&nbsp; - usuario: Eva3

&nbsp; - contraseña: Evaluacion3

\- Mantener funcionamiento actual de:

&nbsp; - AFP

&nbsp; - Trabajadores

&nbsp; - Descuentos

&nbsp; - Liquidaciones (cálculo automático en el modelo)



\## 2. Nueva app para la API



\- Crear una nueva app Django llamada \*\*Eva3Api\*\*.

\- Esta app contendrá:

&nbsp; - Serializers de Django REST Framework.

&nbsp; - Vistas API para exponer datos en JSON.

&nbsp; - Manejo de autenticación por token.



\## 3. Requisitos de la API REST



Usar \*\*Django REST Framework\*\*:



\- Configurar DRF en `settings.py`.

\- Crear serializers para:

&nbsp; - Trabajador

&nbsp; - Liquidaciones



Autenticación:



\- Implementar \*\*Token Authentication\*\* (DRF TokenAuth).

\- Las APIs deben requerir token.



Endpoints mínimos:



1\. \*\*Datos personales del trabajador por RUT\*\*

&nbsp;  - Método: GET

&nbsp;  - URL sugerida: `/api/trabajador/<rut>/`

&nbsp;  - Devuelve datos del trabajador y su AFP.



2\. \*\*Liquidación de un mes específico\*\*

&nbsp;  - Método: GET

&nbsp;  - URL sugerida: `/api/liquidacion/<rut>/<anio>/<mes>/`

&nbsp;  - Devuelve la liquidación (si existe) del trabajador, año y mes especificados.



3\. \*\*Historial de liquidaciones\*\*

&nbsp;  - Método: GET

&nbsp;  - URL sugerida: `/api/liquidacion/historial/<rut>/?desde=AAAA-MM\&hasta=AAAA-MM`

&nbsp;  - Devuelve lista de liquidaciones del rango de meses/años.



Requisitos generales:



\- Respuestas en formato JSON.

\- Manejar errores:

&nbsp; - Trabajador no encontrado.

&nbsp; - Liquidación no encontrada.

&nbsp; - Rango de fechas inválido.

&nbsp; - Token inválido o ausente.



\## 4. Consumo de API externa



\- Consumir API de indicadores económicos (ej: `https://mindicador.cl/api/dolar`).

\- Crear vista que consulte el valor del dólar del día.

\- Exponer esta información:

&nbsp; - En una vista web (template simple) y/o

&nbsp; - En un endpoint JSON dentro de Eva3Api.



\## 5. Cliente de escritorio en Python



\- Aplicación de escritorio (por ejemplo, Tkinter).

\- Debe permitir:

&nbsp; 1. Consultar datos del trabajador por RUT.

&nbsp; 2. Consultar liquidación de un mes/año específico.

&nbsp; 3. Consultar historial de liquidaciones.

\- Debe consumir la API Django usando `requests`.

\- Debe usar autenticación por token.

\- Manejar errores y mostrar mensajes claros al usuario.



\## 6. Entregables



\- Proyecto Django completo.

\- Script SQL de la base de datos.

\- Cliente de escritorio en Python.

\- Archivo `requirements.txt` actualizado.

\- Manual breve de instalación y ejecución.

\- Video (6–15 minutos) explicando:

&nbsp; - Estructura del proyecto.

&nbsp; - Configuración BD.

&nbsp; - Uso de la API con Postman.

&nbsp; - Funcionamiento del cliente de escritorio.



