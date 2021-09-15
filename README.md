# Proyecto de Quotas

Poryecto dedicado al control de ancho de quota de ancho de banda para clientes por medio del manejo de iptables



### Manual de instalacion
Son necesarias las siguientes versiones instaladas:
Python 3.8.10
Flask 2.0.1
Werkzeug 2.0.1

1. Instalar dependencias
    
    apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
    pip3 install Flask
    pip3 install ipaddress

2. Descargar la aplicacion de NAS Server

    scp -r root@172.27.1.10:/mnt/pruebaRaid/quota /var/www/quota
    cd /var/www/quota
    nano quota.wsgi

3. Dentro del archivo wsgi escribimos lo siguiente

    import sys
    sys.path.insert(0, "/var/www/quota")
    from app import app as application

4. Editamos sitios disponibles de apache

    cd /etc/apache2/sites-available/
    nano quota.conf

5. Dentro de quota.conf colocar lo siguiente

    <VirtualHost *>
        WSGIScriptAlias / /var/www/quota/quota.wsgi
        WSGIDaemonProcess quota
        <Directory /var/www/quota>
        WSGIProcessGroup quota
        WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

6. Ejecutamos los siguientes 3 comandos

    a2dissite 000-default.conf
    a2ensite quota.conf
    service apache2 reload

7. Permisos

Es necesario permitir correr el comando como sudo sin contraseña, para esto podemos editar ejecutar lo siguiente

    visudo

Dentro del fichero ubicaremos la linea

    %sudo   ALL=(ALL:ALL) ALL

Y la modificamos por

    %sudo   ALL=(ALL:ALL) NOPASSWD:ALL

7. Si todo sale bien el endpoint deberia ser alcanzable el servicio esta en funcionamiento, para debuggear podemos corroboar en el fichero de logs de apache

    tail -f /var/log/apache2/error.log

### Endpoints de la app

#### GET
- /quota/<\clienteIp>

Este endpoint recibe una ip como parametro en el header, devuelve el contador de bytes actuales en su cola

#### POST
- /reset

Este endpoint se encarga de vaciar las reglas de iptables en mangle y crear los archivos quota y counters para los otros endpoints

- /generate

Este endpoint genera los archivos a utilizar por iptables-restore, organizandolos de la forma correcta para optimizar las reglas y saltos

- /apply

Este endpoint aplica las configuracion de los archivos generados por /generate 