# polo_pigpong_var
Poloniex, Bot para autotrader en USDT_BTC
Este Bot está preparado para trabajar en Python 2.7. No funciona en Python 3.6 o superior
Utilizarlo bajo vuestra responsabilidad !!!!

No me hago responsable de posibles fallos, pérdidas o operaciones incorrectas que pueda realizar el Bot

Para instalarlo, antes hay que instalarse las librerias de Poloniex del siguiente link:

https://github.com/s4w3d0ff/python-poloniex

Antes de ejecutar el programa, hay que editarlo y modificar la línea donde se pide los datos del API.
Si no los tenemos creados, antes hay que ir a la web de Poloniex y crear una llave de API.

Para ejecutarlo poner:

python polo_pingpong_var.py

Una vez ejecutado, nos pedirá el márgen de beneficio que queremos en cada operación. Cuanto más grande sea, tardará más en cerrar las operaciones, pero más beneficio tendremos.
El bot funcionrá mientras tengamos saldo.
Para su correcto funcionamiento, necesitamos tener saldo de USDT y de BTC, y ninguna operacion abierta en el par USDT_BTC. 
Si hay 2 o más operaciones abiertas, esperará a que se cierren. Si hay una, la cerrará.

Evidentemente, para que el bot funcione, se necesita tenerlo siempre funcionando y una conexión a internet.
Los datos los consulta cada 5 minutos, por lo que no consume ancho de banda.
