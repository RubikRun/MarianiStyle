from logger import Logger

class Client:
    def __init__(self, name, egn_cifri, packets):
        self.name = name
        self.egn_cifri = egn_cifri
        self.packets = packets

    def serialize(self):
        s = ""
        s += self.name + ";"
        s += self.egn_cifri
        for packet in self.packets:
            s += ";" + packet.name
        return s

    # Deserializes a client from a declaration string. Returns the client.
    def deserialize(decl, all_packets):
        if decl is None or decl == "":
            Logger.log_error("Client declaration is empty. Client will be skipped")
            return None
        decl_parts = decl.split(';')
        if len(decl_parts) < 2:
            Logger.log_error("Client declaration is invalid, should have at least 2 parts. Client will be skipped")
            return None
        name = decl_parts[0].strip()
        if name == "":
            Logger.log_error("Name part of a client is empty. Client will be skipped")
            return None
        egn_cifri = decl_parts[1].strip()
        if egn_cifri == "":
            Logger.log_error("EGN cifri part of a client is empty. Client will be skipped")
            return None
        client_packets = []
        for packet_name in decl_parts[2:]:
            packet_name = packet_name.strip()
            if packet_name == "":
                Logger.log_error("Packet in a client declaration is empty. Packet will be skipped")
                continue
            packet_exists = False
            for p in all_packets:
                if packet_name == p.name:
                    packet = p
                    packet_exists = True
                    break
            if not packet_exists:
                Logger.log_error("Packet in a client declaration does not exist. Packet will be skipped")
                continue
            client_packets.append(packet)

        client = Client(name, egn_cifri, client_packets)
        return client
