from logger import Logger

class ClientsHandler:
    # Returns the clients from given database sorted by name
    def get_clients_sorted_map(database):
        clients = database.clients
        sorted_clients = sorted(clients, key=lambda client : client.name)

        clients_map = {}
        for vrow, client in enumerate(sorted_clients):
            clients_map[vrow] = client

        return clients_map
