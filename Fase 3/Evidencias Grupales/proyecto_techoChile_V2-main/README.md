# proyecto_techoChile_V2
# Sistema de Gestión Techo Chile

## Descripción
Aplicación web desarrollada en Django para la gestión de proyectos, viviendas, beneficiarios, constructoras, incidencias y usuarios en el contexto de Techo Chile. Permite administrar el ciclo completo de proyectos habitacionales, desde la creación hasta el seguimiento de observaciones y postventa.

## Funcionalidades principales
- **Gestión de Proyectos:** Alta, edición, consulta y desactivación de proyectos habitacionales.
- **Gestión de Viviendas:** Registro y administración de viviendas asociadas a proyectos y beneficiarios.
- **Gestión de Beneficiarios:** Alta, edición y búsqueda de beneficiarios por RUT, nombre y otros filtros.
- **Gestión de Constructoras:** Administración de empresas constructoras, con campos de contacto y región/comuna.
- **Gestión de Usuarios:** Creación y administración de usuarios con roles y permisos diferenciados.
- **Gestión de Roles:** Panel maestro para definir y asignar roles con distintos niveles de acceso.
- **Gestión de Observaciones/Incidencias:** Registro, filtrado y seguimiento de observaciones en viviendas, con adjuntos y prioridades.
- **Panel Maestro:** Dashboard administrativo con acceso rápido a todas las entidades y acciones principales.
- **Modo Oscuro/Claro:** Interfaz adaptable a preferencias de visualización.
- **Diseño Responsivo:** Optimizado para móviles, tablets y escritorio.

## Roles y permisos
- **Administrador:** Acceso total a todas las funciones, puede crear, editar y desactivar cualquier entidad.
- **Constructora:** Acceso limitado a proyectos y viviendas asociadas a su empresa, puede registrar observaciones.
- **Supervisor:** Acceso a reportes, seguimiento de incidencias y gestión de beneficiarios.
- **Postventa:** Acceso a observaciones y gestión de incidencias post entrega.


## Instalación y ejecución
1. Clona el repositorio:
	```bash
	git clone https://github.com/Rfaundezv/proyecto_techoChile_V2.git
	```
2. Instala dependencias:
	```bash
	python -m venv venv
	venv\Scripts\activate
	pip install -r requirements.txt
	```
3. Aplica migraciones:
	```bash
	python manage.py migrate
	```
4. Crea un superusuario (opcional):
	```bash
	python manage.py createsuperuser
	```
5. Ejecuta el servidor:
	```bash
	python manage.py runserver
	```

## Uso básico
- Accede a `http://localhost:8000/` y entra con un usuario de prueba.
- El Panel Maestro permite navegar entre proyectos, viviendas, beneficiarios, constructoras, usuarios, roles y observaciones.
- Utiliza los filtros y formularios para buscar, crear y editar entidades.
- El sistema muestra alertas y mensajes para confirmar acciones importantes.

## Observaciones y adjuntos
- Las observaciones pueden tener archivos adjuntos (fotos, documentos).
- Se pueden filtrar por estado, prioridad, proyecto, vivienda y beneficiario.
- El historial de observaciones permite seguimiento de incidencias y postventa.

## Personalización y configuración
- Puedes modificar los roles y permisos desde el Panel Maestro > Roles.
- El modo oscuro/claro se activa desde la barra superior.
- Los estilos y plantillas se encuentran en la carpeta `templates/` y los archivos estáticos en `static/`.

## Recomendaciones
- Realiza backups periódicos de la base de datos `db.sqlite3`.
- Usa contraseñas seguras para los usuarios administradores.
- Revisa los logs y mensajes del sistema para detectar incidencias.

## Contacto y soporte
Para dudas o soporte, contacta a Rfaundezv vía GitHub o correo institucional.
# 🏠 TECHO CHILE - Sistema de Seguimiento de Incidentes

## 📋 Descripción General
Plataforma web desarrollada en Django para la gestión y seguimiento de observaciones en proyectos de vivienda. Permite la comunicación entre familias, constructoras, TECHO y SERVIU para resolver incidencias de manera eficiente y transparente.

## 👥 Roles y Permisos

### 🏛️ **ADMINISTRADOR**
**Acceso:** Completo al sistema
- ✅ Gestionar todos los módulos del sistema
- ✅ Crear, editar y eliminar proyectos, viviendas y observaciones
- ✅ Administrar usuarios y roles
- ✅ Cambiar estados de observaciones
- ✅ Generar reportes completos
- ✅ Acceso al panel maestro

**Usuario de ejemplo:**
- **Email:** admin@techo.cl
- **Contraseña:** admin123
- **Nombre:** Administrador Sistema

### 🏢 **TECHO**
**Acceso:** Gestión operativa y supervisión
- ✅ Ver todos los proyectos asignados
- ✅ Crear y gestionar observaciones
- ✅ Cambiar estados de observaciones
- ✅ Asignar constructoras a proyectos
- ✅ Generar reportes de seguimiento
- ❌ No puede eliminar proyectos

**Usuario de ejemplo:**
- **Email:** coordinador@techo.cl
- **Contraseña:** techo123
- **Nombre:** María González Coordinadora

### 🏗️ **CONSTRUCTORA**
**Acceso:** Gestión de observaciones de sus proyectos
- ✅ Ver proyectos asignados a su empresa
- ✅ Responder a observaciones
- ✅ Subir evidencias de reparaciones
- ✅ Cambiar estado a "En proceso" o "Cerrada"
- ❌ No puede crear nuevas observaciones
- ❌ Solo ve sus proyectos asignados

**Usuario de ejemplo:**
- **Email:** supervisor@constructora.cl
- **Contraseña:** const123
- **Nombre:** Carlos Mendoza Supervisor
- **Empresa:** Constructora Ejemplo S.A.

### 🏛️ **SERVIU**
**Acceso:** Solo lectura y reportes
- ✅ Ver todos los proyectos y observaciones
- ✅ Descargar reportes de estado
- ✅ Consultar métricas y estadísticas
- ❌ No puede crear observaciones
- ❌ No puede cambiar estados
- ❌ Solo consulta y descarga de información

**Usuario de ejemplo:**
- **Email:**inspector@serviu.cl 
- **Contraseña:** serviu123
- **Nombre:** Ana Rodríguez Inspector SERVIU

### 👨‍👩‍👧‍👦 **FAMILIA**
**Acceso:** Dashboard personal y reporte de observaciones
- ✅ Ver información de su vivienda
- ✅ Crear nuevas observaciones
- ✅ Ver historial de sus observaciones
- ✅ Subir fotos de problemas detectados
- ❌ No puede cambiar estados de observaciones
- ❌ Solo ve información de su vivienda

**Usuario de ejemplo:**
- **Email:** familia@beneficiario.cl
- **Contraseña:** familia123
- **Nombre:** Juan Pérez Familia
- **RUT:** 12345678-9


Puedes iniciar sesión con estos usuarios para probar el sistema y ver los distintos dashboards y permisos.

## 🎯 Objetivos del Sistema
- Centralizar el reporte y seguimiento de observaciones en viviendas
- Facilitar la comunicación entre todos los actores involucrados
- Mejorar los tiempos de respuesta y resolución de incidencias
- Generar reportes y métricas para la toma de decisiones
- Transparentar el proceso de gestión de calidad de las viviendas

## 🚀 Funcionalidades Principales
- Dashboard personalizado por rol
- Registro y gestión de proyectos y viviendas
- Sistema de observaciones con fotos, estados y prioridades
- Flujo de trabajo automatizado entre familia, TECHO y constructora
- Reportes y métricas en tiempo real
- Exportación de reportes a Excel/PDF
- Gestión de usuarios y roles desde el panel maestro
- Modo oscuro/claro y diseño responsivo

## 🛠️ Instalación y Ejecución
1. Clona el repositorio:
	```bash
	git clone https://github.com/Rfaundezv/proyecto_techoChile_V2.git
	```
2. Instala dependencias:
	```bash
	python -m venv venv
	venv\Scripts\activate
	pip install -r requirements.txt
	```
3. Aplica migraciones:
	```bash
	python manage.py migrate
	```
4. Ejecuta el servidor:
	```bash
	python manage.py runserver
	```

## 💻 Acceso y Uso
- Accede a `http://127.0.0.1:8000/` y entra con uno de los usuarios de prueba.
- El sistema redirige automáticamente según el rol:
  - Familia → Dashboard "Mi Vivienda"
  - Otros roles → Dashboard de gestión
- Panel Maestro para administración avanzada de usuarios, roles, proyectos, viviendas y observaciones.
- Filtros y formularios para búsqueda y edición de entidades.

## 📋 Flujo de Trabajo
1. Familia reporta observación con fotos
2. TECHO valida y asigna a constructora
3. Constructora responde y sube evidencia
4. TECHO verifica y cierra observación
5. SERVIU monitorea y descarga reportes

## 📈 Reportes y Métricas
- KPIs en tiempo real
- Reportes por proyecto, constructora o período
- Métricas de tiempo de resolución y calidad
- Exportación a Excel/PDF

## 🧩 Generación de PDF (WeasyPrint en Windows)
Para exportar actas y reportes a PDF usamos WeasyPrint. En Windows requiere dependencias del stack GTK (Cairo, Pango, GDK-PixBuf).



## ⚙️ Configuración y Administración
- Gestión de usuarios y roles en `/admin/` y Panel Maestro
- Registro de constructoras y tipologías
- Definición de recintos y elementos
- Backup automático de base de datos

## 📞 Soporte y Contacto
- Email: soporte@techo.cl
- Teléfono: +56 2 2345 6789

*Sistema desarrollado para TECHO CHILE - Versión 2025*
*Última actualización: Octubre 2025*

