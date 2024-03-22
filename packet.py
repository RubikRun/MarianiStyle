from logger import Logger

class Packet:
    def __init__(self, name, price, uses, validity):
        self.name = name
        self.price = price
        self.uses = uses
        self.validity = validity

    def deserialize(decl):
        if decl is None or decl == "":
            Logger.log_error("Packet declaration is empty. Packet will be skipped")
            return None
        decl_parts = decl.split(';')
        if len(decl_parts) != 4:
            Logger.log_error("Packet declaration is invalid, should have 4 parts. Packet will be skipped")
            return None
        name = decl_parts[0].strip()
        if name == "":
            Logger.log_error("Name part of a packet is empty. Packet will be skipped")
            return None
        price_str = decl_parts[1].strip()
        try:
            price = int(price_str)
        except ValueError:
            Logger.log_error("Price part of a packet is not an integer. Packet will be skipped")
            return None
        uses_str = decl_parts[2].strip()
        try:
            uses = int(uses_str)
        except ValueError:
            Logger.log_error("Price part of a packet is not an integer. Packet will be skipped")
            return None
        validity_str = decl_parts[3].strip()
        try:
            validity = int(validity_str)
        except ValueError:
            Logger.log_error("Price part of a packet is not an integer. Packet will be skipped")
            return None

        packet = Packet(name, price, uses, validity)
        return packet

    def serialize(self):
        s = ""
        s += self.name + ";"
        s += str(self.price) + ";"
        s += str(self.uses) + ";"
        s += str(self.validity)

        return s
