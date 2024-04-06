from database.data_io import DataIO
from logger import Logger

class Client:
    def __init__(self, id, name, phone, packet_instances, vouchers):
        self.id = id
        self.name = name
        self.phone = phone
        self.packet_instances = packet_instances
        self.vouchers = vouchers

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "issII")
        if data is None:
            return None

        if data[0] is None or data[0] < 1:
            Logger.log_error("Client has invalid ID. It will be created with ID = 1")
            data[0] = 1

        client = Client(data[0], data[1], data[2], data[3], data[4])
        return client

    def serialize(self):
        decl = DataIO.create_declaration([self.id, self.name, self.phone, self.packet_instances, self.vouchers], "issII")
        return decl

    def get_view(self):
        if len(self.phone) < 1:
            return self.name
        return "{} ({})".format(self.name, self.phone)

    def get_packet_instances_views(self, database):
        views = []
        for packet_instance_id in self.packet_instances:
            packet_instance = database.get_packet_instance(packet_instance_id)
            if packet_instance is None:
                views.append("")
            else:
                views.append(packet_instance.get_view(database))
        return views

    def get_vouchers_remaining_sum(self, database):
        rsum = 0
        for voucher_id in self.vouchers:
            voucher = database.get_voucher(voucher_id)
            if voucher is not None and not voucher.is_expired(database):
                rsum += voucher.price - voucher.spent
        return rsum

    def use_amount_from_vouchers(self, amount, database):
        if self.get_vouchers_remaining_sum(database) < amount:
            return False
        asum = 0
        todelete_voucher_ids = []
        for voucher_id in self.vouchers:
            voucher = database.get_voucher(voucher_id)
            if voucher is None:
                continue
            voucher_amount = voucher.price - voucher.spent
            if asum + voucher_amount <= amount:
                asum += voucher_amount
                voucher.spent = voucher.price
                todelete_voucher_ids.append(voucher.id)
            else:
                aremaining = amount - asum
                voucher.spent += aremaining
                asum += aremaining

            if asum == amount:
                if len(todelete_voucher_ids) > 0:
                    # We did it, but now we need to delete vouchers that reached 0 remaining from database and delete their IDs from client
                    self.vouchers = [voucher_id for voucher_id in self.vouchers if voucher_id not in todelete_voucher_ids]
                    database.vouchers = [voucher for voucher in database.vouchers if voucher.id not in todelete_voucher_ids]
                return True
            elif asum > amount:
                Logger.log_error("Taking money from vouchers of user but mistakenly took more than needed. Logic error.")
                return True
        return False

    def get_packet_instance_from_view(self, database, packet_instance_view):
        for packet_instance_id in self.packet_instances:
            packet_instance = database.get_packet_instance(packet_instance_id)
            if packet_instance is None:
                return None
            if packet_instance.get_view(database) == packet_instance_view:
                return packet_instance