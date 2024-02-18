"""
Sistema de hoteles
"""
import json
import shlex


class Hotel:
    """
    Hotel
    """
    def __init__(self, hotel_id, name, address, rooms):
        """
        init
        """
        reservations = None
        self.hotel_id = hotel_id
        self.name = name
        self.address = address
        self.rooms = rooms
        self.reservations = reservations if reservations is not None else []

    def display_information(self):
        """
        mostrar info
        """
        print(f"Hotel ID: {self.hotel_id}")
        print(f"Name: {self.name}")
        print(f"Address: {self.address}")
        print(f"Available Rooms: {self.rooms}")
        print("Reservations:")
        for reservation in self.reservations:
            print(f"- {reservation}")

    def modify_information(self, name=None, address=None, rooms=None):
        """
        modificar
        """
        if name:
            self.name = name
        if address:
            self.address = address
        if rooms:
            self.rooms = rooms

    def reserve_room(self, customer, num_rooms):
        """
        reservar
        """
        if num_rooms <= self.rooms:
            self.rooms -= num_rooms
            reservation = f"{customer.name} - {num_rooms} rooms"
            self.reservations.append(reservation)
            return True
        print("Not enough rooms available.")
        return False


def cancel_reservation(customer_id, hotel_id):
    """
    cancelar reservacion
    """
    reservations = load_from_file("reservations.json")
    customer_id_str = str(customer_id)
    hotel_id_str = str(hotel_id)

    if customer_id_str in reservations:
        cus_reservations = reservations[customer_id_str]["reservations"]

        # Busca la reserva por hotel_id y elimínala
        updated_reservations = [r for r in cus_reservations
                                if r["hotel_id"] != hotel_id_str]

        # Actualiza el diccionario de reservaciones y guarda en el archivo
        reservations[customer_id_str]["reservations"] = updated_reservations
        save_to_file("reservations.json", reservations)
        print(f"Reserva para el cliente {customer_id} en" +
              "el hotel {hotel_id} cancelada con éxito.")
    else:
        print("No se encontraron reservaciones" +
              f"para el cliente con ID {customer_id}.")


class Customer:
    """
    Cliente
    """
    def __init__(self, customer_id, name, email):
        """
        init
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """
        to_dict
        """
        return {"customer_id": self.customer_id,
                "name": self.name, "email": self.email}

    def display_information(self):
        """
        display
        """
        print(f"Customer ID: {self.customer_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")

    def modify_information(self, name=None, email=None):
        """
        modificar
        """
        if name:
            self.name = name
        if email:
            self.email = email


class Reservation:
    """
    Reservaciones
    """
    def __init__(self, customer, hotel_id):
        """
        init
        """
        self.customer = customer
        self.hotel_id = hotel_id

    def cancel_reservation(self):
        """
        cancelar
        """
        self.hotel_id.cancel_reservation(self.customer, 1)

    def metodo(self):
        """
        print
        """
        print(self)


def create_hotel(hotel_id, name, address, rooms):
    """
    crear hotel
    """
    hotels = load_from_file("hotels.json")

    # Verifica si el hotel ya existe
    if str(hotel_id) in hotels:
        print(f"El hotel con ID {hotel_id} ya existe.")
        return

    hotel = Hotel(int(hotel_id), name, address, int(rooms))
    hotels[str(hotel_id)] = hotel.__dict__
    save_to_file("hotels.json", hotels)
    print(f"Hotel '{name}' creado con éxito.")


def delete_hotel(hotel_id):
    """
   eliminar hotel
    """
    hotels = load_from_file("hotels.json")
    hotel_id_str = str(hotel_id)

    if hotel_id_str in hotels:
        del hotels[hotel_id_str]
        save_to_file("hotels.json", hotels)
        print(f"Hotel con ID {hotel_id} eliminado con éxito.")
    else:
        print(f"No se encontró ningún hotel con el ID {hotel_id}.")


def display_hotel_information(hotel_id):
    """
    Mostrar información de un hotel dado su ID
    """
    hotels_data = load_from_file("hotels.json")
    hotel = hotels_data.get(str(hotel_id))
    
    if hotel:
        hotel_instance = Hotel(hotel_id=int(hotel_id), name=hotel['name'], address=hotel['address'], rooms=hotel['rooms'])
        hotel_instance.display_information()
    else:
        print(f"Hotel con ID {hotel_id} no encontrado.")


def modify_hotel(hotel_id, name, address, rooms):
    """
    modificar informacion de hotel
    """
    hotels = load_from_file("hotels.json")
    hotel_id_str = str(hotel_id)

    if hotel_id_str in hotels:
        hotels[hotel_id_str]["name"] = name
        hotels[hotel_id_str]["address"] = address
        hotels[hotel_id_str]["rooms"] = int(rooms)
        save_to_file("hotels.json", hotels)
        print(f"Información del hotel con ID {hotel_id} modificada con éxito.")
    else:
        print(f"No se encontró ningún hotel con el ID {hotel_id}.")


def reserve_room(hotel_id, customer_id, num_rooms):
    """
    reservar cuarto
    """
    hotel = load_from_file("hotels.json").get(str(hotel_id))
    customer = load_from_file("customers.json").get(str(customer_id))
    if hotel and customer:
        hotel_instance = Hotel(**hotel)
        customer_instance = Customer(**customer)
        success = hotel_instance.reserve_room(customer_instance,
                                              int(num_rooms))
        if success:
            save_to_file("hotels.json", hotel_instance.__dict__)
            print(f"{num_rooms} habitaciones" +
                  "reservadas en hotel {hotel_instance.name}.")
    else:
        print("Hotel o cliente no encontrado.")


def create_customer(customer_id, name, email):
    """
    crear  cliente
    """
    customers = load_from_file("customers.json")

    # Verifica si el cliente ya existe
    if str(customer_id) in customers:
        print(f"El cliente con ID {customer_id} ya existe.")
        return

    customer = {"customer_id": customer_id, "name": name, "email": email}
    customers[str(customer_id)] = customer
    save_to_file("customers.json", customers)
    print(f"Cliente '{name}' creado con éxito.")


def delete_customer(customer_id):
    """
    eliminar  cliente
    """
    customers = load_from_file("customers.json")
    customer_id_str = str(customer_id)
    if customer_id_str in customers:
        del customers[customer_id_str]
        save_to_file("customers.json", customers)
        print(f"Cliente con ID {customer_id} eliminado con éxito.")
    else:
        print(f"No se encontró ningún cliente con el ID {customer_id}.")


def display_customer_information(customer_id):
    """
    mostrar informacion de cliente
    """
    customer = load_from_file("customers.json").get(str(customer_id))
    if customer:
        customer_instance = Customer(**customer)
        customer_instance.display_information()
    else:
        print(f"Cliente con ID {customer_id} no encontrado.")


def modify_customer(customer_id, name, email):
    """
    modificar reservacion
    """
    customers = load_from_file("customers.json")
    customer_id_str = str(customer_id)

    if customer_id_str in customers:
        customers[customer_id_str]["name"] = name
        customers[customer_id_str]["email"] = email
        save_to_file("customers.json", customers)
        print("Información del cliente con" +
              f"ID {customer_id} modificada con éxito.")
    else:
        print(f"No se encontró ningún cliente con el ID {customer_id}.")


def create_reservation(customer_id, hotel_id):
    """
    crear reservacion
    """
    customers = load_from_file("customers.json")
    hotels = load_from_file("hotels.json")

    customer_id_str = str(customer_id)
    hotel_id_str = str(hotel_id)

    if customer_id_str in customers and hotel_id_str in hotels:
        cus = Customer(**customers[customer_id_str])
        reservations = load_from_file("reservations.json")
        # Verifica si ya hay reservaciones para el cliente
        if customer_id_str in reservations:
            cus_reservations = reservations[customer_id_str]
            ["reservations"]
        else:
            cus_reservations = []
        # Agrega la nueva reserva al cliente
        reservation = {
            "hotel_id": hotel_id, "reservation_id": len(cus_reservations) + 1
        }
        cus_reservations.append(reservation)
        reservations[customer_id_str] = {
            "customer": cus.to_dict(), "reservations": cus_reservations
        }
        save_to_file("reservations.json", reservations)
        print("Reservación creada con éxito.")
    else:
        print("Cliente o hotel no encontrado.")


def delete_reservation(reservation_hash):
    """
    eliminar reservacion
    """
    reservations = load_from_file("reservations.json")
    if reservation_hash in reservations:
        del reservations[reservation_hash]
        save_to_file("reservations.json", reservations)
        print("Reserva eliminada con éxito.")
    else:
        print("Reserva no encontrada.")


# Funciones de utilidad para E/S de archivos

def save_to_file(file_path, data):
    """
    Función para guardar datos
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


def load_from_file(file_path):
    """
    Función para cargar datos de file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            data = json.loads(content)
        return data
    except FileNotFoundError:
        return {}


def parse_arguments(tokens):
    """
    Función para analizar los argumentos y manejar comillas correctamente.
    """
    args = []
    current_arg = ""
    in_quotes = False

    for token in tokens:
        if token.startswith('"'):
            current_arg = token
            in_quotes = True
        elif token.endswith('"'):
            current_arg += " " + token
            args.append(current_arg.strip('"'))
            current_arg = ""
            in_quotes = False
        elif in_quotes:
            current_arg += " " + token
        else:
            args.append(token)

    return args

# Bucle interactivo del programa


def main():
    """
    Main
    """
    print("Bienvenido al sistema de gestión de hoteles." +
          "Ingrese 'help' para ver la lista de comandos disponibles.")
    print("Comandos disponibles:")
    print("create_hotel <hotel_id> <name> <address> <rooms>")
    print("delete_hotel <hotel_id>")
    print("display_hotel <hotel_id>")
    print("modify_hotel <hotel_id> <name> <address> <rooms>")
    print("create_customer <customer_id> <name> <email>")
    print("delete_customer <customer_id>")
    print("display_customer <customer_id>")
    print("modify_customer <customer_id> <name> <email>")
    print("create_reservation <customer_id> <hotel_id>")
    print("cancel_reservation <hotel_id> <customer_id> <num_rooms>")
    print("exit")

    while True:
        user_input = input("Ingrese un comando: ")
        tokens = shlex.split(user_input)

        command = tokens[0].lower()
        if command == 'exit':
            break

        if command == 'create_hotel':
            input_args = parse_arguments(tokens[1:])
            create_hotel(input_args[0], input_args[1],
                         input_args[2], input_args[3])

        elif command == 'delete_hotel':
            input_args = parse_arguments(tokens[1:])
            delete_hotel(input_args[0])

        elif command == 'display_hotel':
            input_args = parse_arguments(tokens[1:])
            display_hotel_information(input_args[0])

        elif command == 'modify_hotel':
            input_args = parse_arguments(tokens[1:])
            modify_hotel(input_args[0], input_args[1],
                         input_args[2], input_args[3])

        elif command == 'create_customer':
            input_args = parse_arguments(tokens[1:])
            create_customer(input_args[0], input_args[1], input_args[2])

        elif command == 'delete_customer':
            input_args = parse_arguments(tokens[1:])
            delete_customer(input_args[0])

        elif command == 'display_customer':
            input_args = parse_arguments(tokens[1:])
            display_customer_information(input_args[0])

        elif command == 'modify_customer':
            input_args = parse_arguments(tokens[1:])
            modify_customer(input_args[0], input_args[1], input_args[2])

        elif command == 'create_reservation':
            input_args = parse_arguments(tokens[1:])
            create_reservation(input_args[0], input_args[1])

        elif command == 'cancel_reservation':
            input_args = parse_arguments(tokens[1:])
            cancel_reservation(input_args[0], input_args[1])


main()
