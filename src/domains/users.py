from dataclasses import dataclass

from src.common.interfaces.objects import IUserObject


@dataclass
class UserObject(IUserObject):
    user_id: str
    name: str
    email: str
    snapshot_id: str
