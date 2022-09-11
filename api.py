import requests

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email, password):
        headers = {'email': email, 'password': password}
        response = requests.get(self.base_url + 'api/key', headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        response = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result

    def post_api_pets(self, auth_key, name, animal_type, age, pet_photo):
        headers = {'auth_key': auth_key['key']}
        form_data = {'name': name, 'animal_type': animal_type, 'age': age, 'pet_photo': pet_photo}
        response = requests.post(self.base_url + 'api/pets', headers=headers, params=form_data)
        status = response.status_code
        try:
            result = response.json()
        except Exception:
            result = response.text
        return status, result

    def delete_api_pets_petid(self, auth_key, pet_id):
        headers = {'auth_key': auth_key['key']}
        response = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)
        status = response.status_code
        try:
            result = response.json()
        except Exception:
            result = response.text
        return status, result

    def put_api_pets_pet_id(self, auth_key, pet_id, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        form_data = {'name': name, 'animal_type': animal_type, 'age': age}
        response = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, params=form_data)
        status = response.status_code
        try:
            result = response.json()
        except Exception:
            result = response.text
        return status, result

    def post_api_pets_photo(self, auth_key, pet_id, pet_photo):
        headers = {'auth_key': auth_key['key']}
        form_data = {'pet_photo': pet_photo}
        response = requests.post(self.base_url + f'api/pets/set_photo/{pet_id}', headers=headers, params=form_data)
        status = response.status_code
        try:
            result = response.json()
        except Exception:
            result = response.text
        return status, result

    def post_api_create_pet_simple(self, auth_key, name, animal_type, age):
        headers = {'auth_key': auth_key['key']}
        form_data = {'name': name, 'animal_type': animal_type, 'age': age}
        response = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, params=form_data)
        status = response.status_code
        try:
            result = response.json()
        except Exception:
            result = response.text
        return status, result
