from typing import Optional
from Domain.Entities.ExampleFakeApi.FakeApiEntity import FakeApiEntity
from Domain.Interfaces.IFakeApiInfrastructure import IFakeApiInfrastructure
from Domain.Interfaces.IHttpClientInfrastructure import IHttpClientInfrastructure
from Domain.Entities.HttpResponseEntity import HttpResponseEntity
from Infrastructure.ExampleFakeApiInfra.ExampleFakeLogger import ExampleFakeLogger
from Infrastructure.ExampleFakeApiInfra.ExampleFakeStartting import _exampleFakeStartting as ExampleFakeStartting
from Domain.Commons.CoreServices import CoreServices as Services
import logging

class FakeApiCommand (IFakeApiInfrastructure):
    def __init__(self) -> None:
        self.__builder_api_client:IHttpClientInfrastructure = Services.get_dependency(IHttpClientInfrastructure)
        
        self._logger = ExampleFakeLogger.set_logger().getChild(self.__class__.__name__)
    
    async def get_user_async(self,id:int) -> Optional[FakeApiEntity]:    
        self.__builder_api_client.http(ExampleFakeStartting.EXAMPLE_HOST_BASE.value).endpoint(f"todos/{id}")
        
        result:HttpResponseEntity = await self.__builder_api_client.get()

        if result.StatusCode == 500:
            self.__logger.error(f"[{result.StatusCode}] [{result.Url}] : {str(result.Content)}")
            return None

        if result.StatusCode != 200 or not result.Content:
            self.__logger.warning(f"[{result.StatusCode}] [{result.Url}] - {str(result.Content)}")
            return None        

        return FakeApiEntity(
                userId = result.Content.get("userId", 0),
                id = result.Content.get("id", 0),
                title = result.Content.get("title", "No Title"),
                completed = result.Content.get("completed", False)
        )