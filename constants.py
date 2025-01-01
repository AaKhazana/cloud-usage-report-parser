from enum import Enum

MONTH_31_DAYS = [1, 3, 5, 7, 8, 10, 12]
MONTH_30_DAYS = [4, 6, 9, 11]
MONTH_28_DAYS = [2]

STANDARD_CLOUD_HOURS = 730

HOURS_31_DAYS = 31 * 24
HOURS_30_DAYS = 30 * 24
HOURS_28_DAYS = 28 * 24

class ResourceType(Enum):
    ECS = "ecs"
    EVS = "evs"
    EIP = "eip"
    BANDWIDTH = "bandwidth"
    ELB = "elb"
    NAT = "nat-gateway"
    VPN = "virtual-private-network"


class StorageType(Enum):
    SSD = "ssd"
    HDD = "hdd"


class ServiceTag(Enum):
    CLUSTERED = "clustered"
    DEDICATED = "dedicated"