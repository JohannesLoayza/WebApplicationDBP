from .models import Mesa, User, Reservacion
from app import db
import datetime

DEFAULT_RESERVATION_LENGTH = 2 # 2 horas

def create_reservation(form_data):
    user = User.query.filter_by(telefono=form_data.telefono_user.data).first()
    if user is None:
        user = user(nombre=form_data.nombre_user.data, telefono=form_data.telefono_user.data)
        db.session.add(user)

    # check table availability
    capacidad = int(form_data.num_users.data)
    mesas = Mesa.query.filter(Mesa.capacidad >= capacidad).order_by(Mesa.capacidad.desc()).all()
    mesa_ids = [m.id for m in mesas]
    if not mesa_ids:
        # no tables with that size
        return False

    # check reservations
    begin_range = form_data.reservacion_datetime.data - datetime.timedelta(hours=DEFAULT_RESERVATION_LENGTH)
    end_range = form_data.reservacion_datetime.data + datetime.timedelta(hours=DEFAULT_RESERVATION_LENGTH)

    reservaciones = Reservacion.query.join(Reservacion.mesa).filter(Mesa.id.in_(mesa_ids),
                    Reservacion.hora_reservacion >= begin_range, Reservacion.hora_reservacion <= end_range).order_by(Mesa.capacidad.desc()).all()
    if reservaciones:
        if len(mesa_ids) == len(reservaciones):
            # no available tables, sorry
            # still add guest
            db.session.commit()
            return False
        else:
            # get available table
            mesa_id = (set(mesa_ids) - set([r.mesa.id for r in reservaciones])).pop()
            reservacion = Reservacion(user=user, mesa=Mesa.query.get(int(mesa_id)),
                                      num_users=capacidad, hora_reservacion=form_data.reservacion_datetime.data)
    else:
        # we are totally open
        reservacion = Reservacion(user=user, mesa=Mesa.query.get(int(mesa_ids[0])), num_users = capacidad, hora_reservacion=form_data.reservacion_datetime.data)

    db.session.add(reservacion)
    db.session.commit()
    return reservacion