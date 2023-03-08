## Alpes POC 

1. La arquitectura debe seguir los principios de microservicios basados en eventos. Por tal motivo, la
comunicación entre los servicios debe hacerse usando comandos y eventos.
2. Sea claro en la definición de los eventos de acuerdo al escenario de calidad que desea satisfacer ¿Evento
de integración o con carga de estado? ¿Por qué? Elabore en el diseño del esquema, desde la tecnología
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

### Servicios

- Client - Fake de datos
- Ordenes - Maneja las ordenes de compra
- Pagos - Maneja los pagos de las ordenes
- Reporting - Genera reportes de las ordenes

### Tecnologías

- Python
- Docker
- Docker Compose
- Apache Pulsar 
- Apache Protobuf

### Diagrama de arquitectura 

![alpes poc](https://user-images.githubusercontent.com/31944043/223587671-b1b5bcc1-a850-45b9-bcec-9d6e758f72aa.png)


### Arrancar los servicios

**Ordenes**

```shell
  docker-compose up -d order
```

**Pagos**

```shell
  docker-compose up -d pagos
```

**Reportes**

```shell
  docker-compose up -d reporting
```

**Cliente - Fake de datos**

Entre al servicio y configure en la linea 40 de main.py el numero de ordenes que desea generar

```python
    for i in range(0, 100): # <- Aquí
```

```shell
  docker-compose up -d client
```

### Esquemas de datos

Para este proyecto se usó el esquema clasico CRUD para cada servicio y de manera descentralizada, es decir, cada servicio tiene su propia base de datos.
La razón de ello es que es más fácil de probar y llegar a una posible de replicación de datos, usando los patrones vistos en clase outbox y cdc.

### Esquemas

**Orden - Comando**

```protobuf
   message Order {
     string id = 1;
     int32 client_id = 2;
     string address = 3;
     string status = 4;
     float created_at = 5;
   }
```

**Orden Creada - Evento**

```protobuf
   message OrdenCreada {
     string id = 1;
     int32 client_id = 2;
     string address = 3;
     string status = 4;
     float created_at = 5;
     string service = 6;
   }
```

**Transacción Procesada - Evento**

```protobuf
   message TransaccionProcesada {
     string order_id = 1;
     string status = 2;
   }
```

En este caso se usa los dos tipos de eventos, el de integración y el de carga de estado, 
ya que el evento de integración es usado para notificar que una orden fue creada y el evento de carga de estado es usado para notificar que una transacción fue procesada.
En dicho caso, la orden creada nos da los datos necesarios para calcular el pago de la transacción y el de carga de estado nos da el estado de la transacción y el id de la orden.

### Generar los protos

```shell
  python -m grpc_tools.protoc -I. --python_out=. schemas/event.proto
```

### Errores comunes

1. Si durante la generacion de protos presenta un error con grpcio-tools de que el modulo no fue encontrado ejecute `pip install grpcio-tools`

### Escenarios de calidad

- Desempeño: El sistema debe ser capaz de atender 1000 ordenes por minuto manteniendo un desempeño constante
- Modificabilidad: agregar otros formatos de reportes con facilidad y sin impactar la funcionalidad
- Escalabilidad: El sistema debe ser capaz de soportar una alta demanda de ordenes, en caso que el contenedor se estrese en cuanto a memoria, cpu o disco, se debe poder escalar el servicio de manera horizontal.

### Video de la entrega

https://uniandes-my.sharepoint.com/:v:/g/personal/a_aldanam_uniandes_edu_co/ETegtSsfRwVEgRKHbcQ9fFABDP2M8Zv1M_X1cLFZvjEfbg?e=UYkqIF