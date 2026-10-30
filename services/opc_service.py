from asyncua import Server


class OPCService:

    def __init__(self):

        self.server = Server()

        self.locations = {}

    async def start(self):

        await self.server.init()

        self.server.set_endpoint(
            "opc.tcp://0.0.0.0:4840"
        )

        idx = await self.server.register_namespace(
            "http://lab-opcua"
        )

        self.idx = idx

        self.root = await self.server.nodes.objects.add_object(
            idx,
            "Locations"
        )

        await self.server.start()

        print("Servidor OPC-UA arrancado")

    async def create_location(
        self,
        name
    ):

        if name in self.locations:
            return

        city = await self.root.add_object(
            self.idx,
            name
        )

        temp = await city.add_variable(
            self.idx,
            "Temperatura",
            0.0
        )

        humedad = await city.add_variable(
            self.idx,
            "Humedad",
            0
        )

        presion = await city.add_variable(
            self.idx,
            "Presion",
            0.0
        )

        viento = await city.add_variable(
            self.idx,
            "Viento",
            0.0
        )

        await self.server.historize_node_data_change(
            temp,
            period=None,
            count=100
        )

        await self.server.historize_node_data_change(
            humedad,
            period=None,
            count=100
        )

        await self.server.historize_node_data_change(
            presion,
            period=None,
            count=100
        )

        await self.server.historize_node_data_change(
            viento,
            period=None,
            count=100
        )

        self.locations[name] = {
            "temp": temp,
            "humedad": humedad,
            "presion": presion,
            "viento": viento
        }

    async def update_location(
        self,
        name,
        temperatura,
        humedad,
        presion,
        viento
    ):

        if name not in self.locations:
            return

        await self.locations[name]["temp"].write_value(
            temperatura
        )

        await self.locations[name]["humedad"].write_value(
            humedad
        )

        await self.locations[name]["presion"].write_value(
            presion
        )

        await self.locations[name]["viento"].write_value(
            viento
        )

    async def stop(self):

        await self.server.stop()