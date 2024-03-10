from enum import Enum


class Text(str, Enum):
    WELCOME = 'Приветсвие'
    JOIN_TEAM = 'Вступление'
    CHECK_UID = (
        'Введите айди\n'
        'инструкция где <b><i>его взять</i></b> и т.<i>д</i>.'
    )
    ALREADY_AFFILIATE = (
        'Инструкция как сменить партенство\n'
        'hfp ldf nhb'
        'sqweqwr'
    )
    INVALID_UID_FORMAT = ('Неправильный формат айди юзера\n'
                          'Введите заново')
    SUCCESSFUL_CHECK = '<b>Проверка</b> <i>пройдена</i> успешно\nВаша ссылка: {}'
    UNSUCCESSFUL_CHECK = 'Проверка не пройдена'
    AFFILIATE_NOT_FOUND = 'Вы не партнер или данные не успели обновиться'
    NOT_ENOUGH_TRADING_VOLUME = 'ваш объем недостаточный, а нужен {}'
    NOT_ENOUGH_DEPOSIT = 'ваш депозит недостаточный, а нужен {}'
    REQUEST_UID_ERROR = 'ошибка при выполнении запроса'
