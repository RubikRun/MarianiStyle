class PacketsHandler:
    # Returns the packets from given database
    def get_packets_map(database):
        packets = database.packets

        packets_map = {}
        for vrow, packet in enumerate(packets):
            packets_map[vrow] = packet

        return packets_map
