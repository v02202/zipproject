import unittest, requests, os, json, string, random, zipfile
from tempfile import NamedTemporaryFile, TemporaryDirectory
ust_root = os.environ['URL_ROOT_BACKEND']



class UserTestCase(unittest.TestCase):
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
        
        
        with open("A.txt","w") as a:
            a.write('this is A')
        with open("B.txt","w") as b:
            b.write('this is B')
        with open("C.txt","w") as c:
            c.write('this is C')

        with zipfile.ZipFile("./ab.zip", 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write("./A.txt", 'A.txt')
            archive.write("./B.txt", 'B.txt')
        with zipfile.ZipFile("./ac.zip", 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.write("./A.txt", 'A.txt')
            archive.write("./C.txt", 'C.txt')
        
    def tearDown(self):
        if os.path.exists("A.txt"):
            os.remove("A.txt")
        if os.path.exists("B.txt"):
            os.remove("B.txt")
        if os.path.exists("ab.zip"):
            os.remove("ab.zip")
        if os.path.exists("ac.zip"):
            os.remove("ac.zip")
        if os.path.exists("C.txt"):
            os.remove("C.txt")

    def test_upload_file(self):
        # store apikey
        apitoken_data = json.loads(self.apikey_data)
        response = requests.post(f'{ust_root}/api/apikey/store', self.apikey_data)#
        # get api token
        apitoken_data['api_key'] = json.loads(response.content.decode())['data']['api_key']
        response = requests.post(f'{ust_root}/api/apikey/token', json.dumps(apitoken_data))
        x_api_token = {'x-api-key':f"{json.loads(response.content.decode())['data']['access_token']}"}
        # create supplier
        response = requests.post(f'{ust_root}/api/supplier/create', self.supplier_data, headers=x_api_token)
        self.user_data['supplier_id'] = json.loads(response.content.decode())['data']['supplier_id']
        # create users
        response = requests.post(f'{ust_root}/api/users/create', json.dumps(self.user_data), headers=x_api_token)
        self.user_data.pop('supplier_id', None)
        response = requests.post(f'{ust_root}/api/users/login', json.dumps(self.user_data), headers=x_api_token)
        print('response: ', response)
        user_token = json.loads(response.content.decode())['data']['acs_token']
        # Add Auth header
        x_api_token['Authorization']=f"Bearer {user_token}"
        
        # upload file
        multipart_form_data = {
            'upload_file': open('./ab.zip', 'rb'),
        }
        response = requests.post(f'{ust_root}/api/upload/zip', files=multipart_form_data, headers=x_api_token)
        self.assertEqual(response.status_code, 200)

    def test_upload_file_wrong_file(self):
        # store apikey
        apitoken_data = json.loads(self.apikey_data)
        response = requests.post(f'{ust_root}/api/apikey/store', self.apikey_data)#
        # get api token
        apitoken_data['api_key'] = json.loads(response.content.decode())['data']['api_key']
        response = requests.post(f'{ust_root}/api/apikey/token', json.dumps(apitoken_data))
        x_api_token = {'x-api-key':f"{json.loads(response.content.decode())['data']['access_token']}"}
        # create supplier
        response = requests.post(f'{ust_root}/api/supplier/create', self.supplier_data, headers=x_api_token)
        self.user_data['supplier_id'] = json.loads(response.content.decode())['data']['supplier_id']
        # create users
        response = requests.post(f'{ust_root}/api/users/create', json.dumps(self.user_data), headers=x_api_token)
        self.user_data.pop('supplier_id', None)
        print("self.user_data: ", self.user_data)
        response = requests.post(f'{ust_root}/api/users/login', json.dumps(self.user_data), headers=x_api_token)
        print('response: ', response)
        user_token = json.loads(response.content.decode())['data']['acs_token']
        # Add Auth header
        x_api_token['Authorization']=f"Bearer {user_token}"
        
        # upload file
        multipart_form_data = {
            'upload_file': open('./ac.zip', 'rb'),
        }
        response = requests.post(f'{ust_root}/api/upload/zip', files=multipart_form_data, headers=x_api_token)
        self.assertEqual(response.status_code, 406)


if __name__ == '__main__':
    unittest.main()