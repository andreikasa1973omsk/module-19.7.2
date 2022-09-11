import os

from api import PetFriends
from settings import valid_email, valid_password

pf: PetFriends = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert result['key'] == '9883d332b206b1e39e65df3724e16dd3343b383676d41fd629936b93'


def test_get_api_key_for_not_valid_email(email='123', password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, _ = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_api_key_for_not_valid_password(email=valid_email, password=''):
    """ Проверяем что запрос api ключа возвращает статус 403"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, _ = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список."""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем, что запрос моих питомцев возвращает пустой или заполненный список."""

    # Запрашиваем ключ api и сохраняем в переменую auth_key"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


# Не добавляется новый питомец, невозможно провести тест
def test_post_api_pets_with_valid_data(name='Гога', animal_type='попугай', age='1',
                                       pet_photo='images\попугай_гога.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] == pet_photo


# API должна возвращать 400, а она возвращает 200
def test_post_api_pets_with_invalid_photo(name='Гога', animal_type='попугай', age='1',
                                          pet_photo='images\invalid_photo.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_delete_api_pets_pet_id():
    '''Проверяем, что можно удалить питомца'''
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        status, _ = pf.post_api_create_pet_simple(auth_key, "Мася", "таракан", "1")
        assert status == 200, 'New pet is not added'
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_api_pets_petid(auth_key, pet_id)
    assert status == 200


# API должна возвращать 404, а она возвращает 200
def test_delete_api_pets_invalid_pet_id():
    '''Проверяем, что можно удалить питомца с невалидным id'''
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Берём невалидный id питомца и отправляем запрос на удаление
    pet_id = 'hello'
    status, _ = pf.delete_api_pets_petid(auth_key, pet_id)

    # Проверяем что статус ответа равен 404 и в списке питомцев нет питомца с невалидным id
    assert status == 404


def test_post_api_pets_photo_no_photo(pet_photo=None):
    '''Проверяем, что можно добавить фото животного не прикрепляя фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        status, _ = pf.post_api_create_pet_simple(auth_key, "Мася", "таракан", "1")
        assert status == 200, 'New pet is not added'
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на обновление фото
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.post_api_pets_photo(auth_key, pet_id, pet_photo)
    assert status == 400


def test_successful_update_self_pet_info(name='Варанчик', animal_type='ящерица', age='2'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список пустой, то пробуем добавить новое животное
    if len(my_pets['pets']) == 0:
        status, _ = pf.post_api_create_pet_simple(auth_key, "Мася", "таракан", "1")
        assert status == 200, 'New pet is not added'
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.put_api_pets_pet_id(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


# API должна возвращать 400, а она возвращает 200
def test_update_self_pet_invalid_age(name='Варанчик', animal_type='ящерица', age=-100):
    """Проверяем возможность обновления информации о питомце некорректным возрастом"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список пустой, то пробуем добавить новое животное
    if len(my_pets['pets']) == 0:
        status, _ = pf.post_api_create_pet_simple(auth_key, "Мася", "таракан", "1")
        assert status == 200, 'New pet is not added'
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, _ = pf.put_api_pets_pet_id(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # Проверяем что статус ответа = 400
    assert status == 400


def test_put_api_pet_invalid_pet_id(pet_id='hello', name='Варанчик', animal_type='ящерица', age=1):
    '''Проверяем, что можно обновить питомца с невалидным id'''
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Берём невалидный id питомца и отправляем запрос на удаление
    status, _ = pf.put_api_pets_pet_id(auth_key, pet_id, name, animal_type, age)

    # Проверяем что статус ответа равен 400 и в списке питомцев нет питомца с невалидным id
    assert status == 400


def test_post_api_create_pet_simple_with_valid_data(name='Гога', animal_type='попугай', age='1'):
    """Проверяем что можно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age


# API должна возвращать 400, а она возвращает 200
def test_post_api_create_pet_simple_with_invalid_age(name='Гога', animal_type='попугай', age='age'):
    """Проверяем что можно добавить питомца с некорректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
