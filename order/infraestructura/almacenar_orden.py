from sqlalchemy_orm import Model, Database

Base = Model()


class Orden(Base):
    id: str
    client_id: int
    address: str
    status: str


db = Database("postgresql://ordenes_user:123@localhost:5432/ordenes_service")
db.create(Orden)


def almacenar_orden(ordenes):
    print("Almacenando orden")
    session = db.session()
    for orden in ordenes:
        db_orden = Orden(id=orden.id, client_id=orden.client_id, address=orden.address, status=orden.status)
        session.create(db_orden)
    session.commit()
