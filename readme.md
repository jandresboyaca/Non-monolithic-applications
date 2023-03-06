 
1. La arquitectura debe seguir los principios de microservicios basados en eventos. Por tal motivo, la
comunicación entre los servicios debe hacerse usando comandos y eventos.
2. Sea claro en la definición de los eventos de acuerdo al escenario de calidad que desea satisfacer ¿Evento
de integración o con carga de estado?¿Por qué? Elabore en el diseño del esquema, desde la tecnología
hasta la evolución de los mismos ¿Avro o Protobuf? ¿Event Stream Versioning? Justifique sus decisiones.
3. Para probar las capacidades de escalado, los ingenieros esperan que usted desarrolle al menos 4
microservicios. Cabe aclarar que NO se espera tener los microservicios completamente desarrollados,
solo los comandos, consultas e infraestructura necesaria (tablas, tópicos, repositorios, etc) para satisfacer
los escenarios de calidad.
4. Dada la naturaleza de la comunicación por comandos y eventos, usted debe usar un Broker de eventos.
Los ingenieros de EDA desean que usted use Apache Pulsar.

5. En su experimentación debe ser claro que patrones y tácticas para el almacenado de los datos sus
microservicios van a usar: ¿descentralizado o híbrido? ¿Por qué?
6. En términos de patrones para el almacenamiento, decida si va usar un modelo clásico CRUD o Event
Sourcing. Recuerde que no necesariamente todos los servicios deben usar el mismo patrón de
almacenamiento. Es su decisión definir que servicios pueden usar una u otra
 


### Para generar clases
 python -m grpc_tools.protoc -I. --python_out=. schemas/event.proto


### Errores comunes
1. Si durante la generacion de protos presenta un error con grpcio-tools de que el modulo no fue encontrado ejecute
   ```pip install grpcio-tools```
2. 