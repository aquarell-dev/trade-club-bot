from enum import Enum


class Button(str, Enum):
    JOIN_TEAM = 'Вступить в клуб'
    REGISTER = 'Регистрация'
    CHECK_UID = 'Прислать UID'
    ALREADY_AFFILIATE = 'Я уже партнер'
