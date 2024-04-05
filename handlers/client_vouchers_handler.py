class ClientVouchersHandler:
    # Returns the vouchers of given client
    def get_vouchers_map(database, client_id):
        client = database.get_client(client_id)
        if client is None:
            return {}

        vouchers = [v for v in database.vouchers if v.client_id == client_id]
        vouchers_map = {}
        for vrow, voucher in enumerate(vouchers):
            vouchers_map[vrow] = voucher

        return vouchers_map