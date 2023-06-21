from app.factory.controller import ControllerFactory
from app.factory.service import ServiceFactory
from app.interfaces.factory.controller import IControllerFactory
from app.interfaces.factory.service import IServiceFactory

service_factory: "IServiceFactory" = ServiceFactory()
controller_factory: "IControllerFactory" = ControllerFactory(service_factory)
