"""SMC API Client Library"""

from smc_api_lib.api.client import SMCClient
from smc_api_lib.schemas import api_schemas

__version__ = "1.0.0"
__all__ = ["SMCClient", "api_schemas"]