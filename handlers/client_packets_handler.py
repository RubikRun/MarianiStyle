class ClientPacketsHandler:
    # Returns the packet instances of given client
    def get_packets_map(database, client_id):
        client = database.get_client(client_id)
        if client is None:
            return {}

        packet_instances = [packet_instance for packet_instance in database.packet_instances if packet_instance.client_id == client_id]
        packets_map = {}
        for vrow, packet_instance in enumerate(packet_instances):
            packets_map[vrow] = packet_instance

        return packets_map