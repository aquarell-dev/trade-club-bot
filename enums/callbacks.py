from enum import Enum


class Callback(str, Enum):
    CHECK_UID = 'check_uid'
    ALREADY_AFFILIATE = 'already_affiliate'
