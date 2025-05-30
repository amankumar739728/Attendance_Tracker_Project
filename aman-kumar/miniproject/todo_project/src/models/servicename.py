from models.schema import SampleResponse

class Mainclass():
    def __init__(self, request,conn):
        pass
        
        
    async def get_sample_response(self,data):
        return SampleResponse(message=f"Hello, {data['fullname']}!", status="success").dict()
