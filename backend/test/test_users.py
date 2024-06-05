import unittest, requests, os, json, string, random


ust_root = os.environ['URL_ROOT_BACKEND']



class UserTestCase(unittest.TestCase):
    user_token = None
    apitoken_data = None
    xapi_data = None

    def setUp(self):
        self.apikey_data = json.dumps({
            "api_name": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        })
        self.supplier_data = json.dumps({
            "supplier_name": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        })
        self.user_data = {
            "email": f"test_{random.randint(0, 200)}@gmail.com",
            "password": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        }
        
    def tearDown(self):
        self.apikey_data = None
        self.user_data = None
        self.supplier_data = None

    def test_create_apikey(self):
        response = requests.post(f'{ust_root}/api/apikey/store', self.apikey_data)
        if response.status_code == 200:
            apitoken_data = json.loads(self.apikey_data)
            apitoken_data['api_key'] = json.loads(response.content.decode())['data']['api_key']
            self.__class__.apitoken_data = json.dumps(apitoken_data, indent=4)
            
        self.assertEqual(response.status_code, 200)

    def test_get_api_token(self):
        response = requests.post(f'{ust_root}/api/apikey/token', self.__class__.apitoken_data)
        self.assertEqual(response.status_code, 200)

    def test_create_supplier(self):
        response = requests.post(f'{ust_root}/api/apikey/token', self.__class__.apitoken_data)
        self.__class__.xapi_data = {'x-api-key':f"{json.loads(response.content.decode())['data']['access_token']}"}
        response = requests.post(f'{ust_root}/api/supplier/create', self.supplier_data, headers=self.__class__.xapi_data)
        # Confirm that the request-response cycle completed successfully.
        if response.status_code == 200:
            self.user_data['supplier_id'] = json.loads(response.content.decode())['data']['supplier_id']
            self.user_data = json.dumps(self.user_data)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = requests.post(f'{ust_root}/api/supplier/create', self.supplier_data, headers=self.__class__.xapi_data)
        self.user_data['supplier_id'] = json.loads(response.content.decode())['data']['supplier_id']
        self.user_data = json.dumps(self.user_data)
        response = requests.post(f'{ust_root}/api/users/create', self.user_data, headers=self.__class__.xapi_data)
        self.assertEqual(response.status_code, 200)

    def test_create_user_existed(self):
        response = requests.post(f'{ust_root}/api/supplier/create', self.supplier_data, headers=self.__class__.xapi_data)
        self.user_data['supplier_id'] = json.loads(response.content.decode())['data']['supplier_id']
        self.user_data = json.dumps(self.user_data)
        requests.post(f'{ust_root}/api/users/create', self.user_data, headers=self.__class__.xapi_data)
        response = requests.post(f'{ust_root}/api/users/create', self.user_data, headers=self.__class__.xapi_data)
        self.assertEqual(response.status_code, 406)

    def test_login(self):
        response = requests.post(f'{ust_root}/api/supplier/create', self.supplier_data, headers=self.__class__.xapi_data)
        self.user_data['supplier_id'] = json.loads(response.content.decode())['data']['supplier_id']
        requests.post(f'{ust_root}/api/users/create', json.dumps(self.user_data), headers=self.__class__.xapi_data)
        self.user_data.pop('supplier_id', None)
        response = requests.post(f'{ust_root}/api/users/login', json.dumps(self.user_data), headers=self.__class__.xapi_data)
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()