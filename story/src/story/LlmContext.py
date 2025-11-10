from dataclasses import dataclass
import json
import lmstudio as lms
import asyncio

@dataclass
class ConnectionInfo():
    host = 'localhost'
    port = '1234'

    def __init__(self, host, port, model=None):
        self.host = host
        self.port = port
        self.model_key = model

    @property
    def api_url(self):
        return f'{self.host}:{self.port}'
    
    def __repr__(self):
        return json.dumps({
            "type": self.__class__.__name__,
            "host": self.host,
            "port": self.port,
            "model_key": self.model_key
        })

class LlmContext():
    _connection_info: ConnectionInfo = None
    client: lms.AsyncClient | None = None

    @staticmethod
    def CreateDefault():
        connection_info = ConnectionInfo("192.168.0.28", "1234", "teknium.openhermes-2.5-mistral-7b@q8_0")
        return LlmContext(connection_info)

    def __init__(self, connection_info: ConnectionInfo):
        self._connection_info = connection_info

    async def __aenter__(self):
        self.client = await lms.AsyncClient(self._connection_info.api_url).__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        return False
    
    async def get_available_models(self):
        return [model for model in await self.client.list_downloaded_models()]

    async def is_connected(self):
        try:
            return self.client is not None and await self.client.is_valid_api_host(self.connection_info.api_url)
        except:
            return False
        
    async def complete_stream(self, text):
        try:
            model = await self.client.llm.model(self.connection_info.model_key)
            stream = await model.respond_stream(text)
            async for fragment in stream:
                yield fragment.content

        except Exception as err:
            raise err
        
    async def complete_block(self, text):
        # try:
        result = []
        async for val in self.complete_stream(text):
            result.append(val)
        return ''.join(result)
    

    @property
    def connection_info(self):
        return self._connection_info

    @connection_info.setter
    def connection(self, connection: ConnectionInfo):
        self._connection_info = connection

    def __repr__(self):
        return json.dumps({
            "type": self.__class__.__name__,
            "connection": repr(self.connection_info),
        })