# Simple Phone API

Simple API to manage phonenumbers and phonecalls

## Requisitos
* Python 2.7
* Pip

## Instalación de dependencias

Primero que nada, hay que contar con Python y Pip para poder instalar todas las dependencias necesarias. Python suele venir en Mac y Ubuntu, pero puede que Pip no venga.

Para instalar Pip en Ubuntu:

```bash
sudo apt-get install python-pip
```

Para instalar Pip en Mac OS:

```bash
sudo easy_install pip
```

Una vez que tenemos instalados Python y Pip, nos dirigimos a la carpeta raíz del proyecto, y ejecutamos lo siguiente
```bash
pip install -r requirements.txt
```


## Cómo correrla
Una vez adentro del repo, los tests se corren así:

```bash
pytest
```

Y la aplicación se enciende así:
```bash
python app.py
```

El servidor correrá en la URL: http://127.0.0.1:5000/

## Uso

La API responde a 4 endpoints, los cuales listaremos a continuación:

1. Creación de una nueva línea `/lines/create`

```bash
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{"phone_number": :phone_number , "name":":name"}' \
     http://127.0.0.1:5000/lines/create
```
Si el phone_number no es válido (tiene letras), si no envío data en el body o si las keys enviadas en data son erroneas, devuelvo 400.
En caso de que se envíe un tipo de dato incorrecto al requerido, la api nos informará que key tiene un tipo inválido y devolverá  422.
Si todo sale bien, devolverá 200 y la nueva columna creada en la base de datos.

2. Consulta de la información de un número de telefono en particular `/lines/:phonenumber`

```bash
curl -i 'http://127.0.0.1:5000/lines/:phone_number'
```
Esta api devolverá 404 en caso de no encontrar el número ingresado (no chequea si el número está bien escrito ya que tenga letras o símbolos raros igualmente le llegaría 404 NOT FOUND.
En caso de encontrarlo, devuelve 200 y el resultado.

Este enpoint, a su vez, también permite eliminar un número de telefono en particular, ejecutando:

```bash
curl -X "DELETE" 'http://127.0.0.1:5000/lines/:phone_number'
```

En este caso, como en el del get, si no encuentra el número que se le pasó, devolverá un 404, y en caso de que si lo encuentre, devolverá un 204 sin contenido.

Por ejemplo:
```bash
curl -i 'http://127.0.0.1:5000/lines/1157639285'
```
```javascript
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 75
Server: Werkzeug/0.14.1 Python/2.7.15
Date: Tue, 18 Sep 2018 18:11:56 GMT

{
    "minutes": 0, 
    "name": "colo", 
    "phone_number": 1157639285
}
```

3. Realizar una llamada de X minutos en una línea en particular `/lines/:phonenumber/phonecall`

```bash
curl -H 'Content-Type: application/json' -X -i PUT \
     -d '{"minutes": 2}' \
     'http://127.0.0.1:5000/lines/:phone_number/phonecall'
```
Si el phone_number no es válido (tiene letras), si no envío data en el body, si las keys enviadas en data son erroneas, si la cantidad de minutos que se le pasaron por body es negativa o si la cantidad de minutos enviada no permite realizar la llamada (minutos restantes - minutos disponibles < 0) devuelvo 400.
En caso de que se envíe un tipo de dato incorrecto al requerido, la api nos informará que key tiene un tipo inválido y devolverá  422.
En caso de que el número de telefono no exista en la base, se envía un 404.
Si todo sale bien, devolverá 200 y la información actualizada de la línea.

Por ejemplo:
```bash
curl -H 'Content-Type: application/json' -X -i PUT \
     -d '{"minutes": 2}' \
     'http://127.0.0.1:5000/lines/:phone_number/phonecall'
```
```javascript
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 75
Server: Werkzeug/0.14.1 Python/2.7.15
Date: Tue, 18 Sep 2018 18:11:56 GMT

{
    "minutes": 5, 
    "name": "colo", 
    "phone_number": 1157639285
}
```
```bash
curl -H 'Content-Type: application/json' -X -i PUT \
     -d '{"minutes": 2}' \
     'http://127.0.0.1:5000/lines/1157639285/phonecall'
```
```javascript
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 75
Server: Werkzeug/0.14.1 Python/2.7.15
Date: Tue, 18 Sep 2018 18:24:42 GMT

{
    "minutes": 3, 
    "name": "colo", 
    "phone_number": 1157639285
}
```

4. Realizar una recarga y que el restante sea X en una línea en particular `/lines/:phonenumber/charge`

```bash
curl -H 'Content-Type: application/json' -X -i PUT \
     -d '{"minutes": 2}' \
     'http://127.0.0.1:5000/lines/:phone_number/charge'
```
Si el phone_number no es válido (tiene letras), si no envío data en el body, si las keys enviadas en data son erroneas o si la cantidad de minutos que se le pasaron por body es negativa, devuelvo 400.
En caso de que se envíe un tipo de dato incorrecto al requerido, la api nos informará que key tiene un tipo inválido y devolverá  422.
En caso de que el número de telefono no exista en la base, se envía un 404.
Si todo sale bien, devolverá 200 y la información actualizada de la línea.

Por ejemplo:
```bash
curl -i 'http://127.0.0.1:5000/lines/1157639285'
```
```javascript
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 75
Server: Werkzeug/0.14.1 Python/2.7.15
Date: Tue, 18 Sep 2018 18:11:56 GMT

{
    "minutes": 5, 
    "name": "colo", 
    "phone_number": 1157639285
}
```
```bash
curl -H 'Content-Type: application/json' \
     -X PUT -d '{"minutes": 12}' \
     'http://127.0.0.1:5000/lines/1157639285/charge' -i
```
```javascript
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 75
Server: Werkzeug/0.14.1 Python/2.7.15
Date: Tue, 18 Sep 2018 18:24:42 GMT

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 76
Server: Werkzeug/0.14.1 Python/2.7.15
Date: Tue, 18 Sep 2018 18:32:11 GMT

{
    "minutes": 12, 
    "name": "colo", 
    "phone_number": 1157639285
}
```

## Diseño y consideraciones

* Seguí la convención que maneja la librería, de tener en un archivo el modelo, en otro la configuración de la base de datos, en un tercero el comportamiento de las api calls y en un archivo principal (app.py), la parte de lanzar la aplicación y el routeo de las diferentes rutas

## Cambios 


## To Do


