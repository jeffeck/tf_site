from django.test import Client, TestCase

from .forms import UploadFileForm
from .models import Iris

class IrisTestCase(TestCase):

    def setup(self):
        file = './static/tf_site/datasets/iris.csv'


    def test_pages(self):
        """ 
        This tests that webpages are available and returning 200 status codes
        1xx: Informational 
        2xx: Success
            200: OK
            201: Created
            204: No Content
        3xx: Redirection
        4xx: Client Error
            400: Bad Request
            401: Unauthorized
            403: Forbidden
            404: Not Found
            409: Conflict
        5xx: Server Error
            500: Internal Server Error
        """
        for link in ['/', 
                     '/iris/', 
                     '/iris/upload/', 
                     '/iris/upload/success/', 
                     '/iris/browse/',
                    ]:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)


    def check_pk(self):
        """
        Creates an Iris object, default pk value is 1
        Checks the url that the individual detail link is accessible
        Checks that a pk reference not in table is redirected
        """
        iris = Iris(1, 2, 3, 4, 'test')
        response = self.client.get('/iris/1')
        self.assertEqual(response.status_code, 200)
        bad_response = self.client.get('/iris/2')
        self.assertEqual(response.status_code, 301)


    def test_bad_page(self):
        """
        Tests that a bad url returns a 404 response
        """
        response = self.client.get('/does-not-exist/')
        self.assertEqual(response.status_code, 404)
        

    def test_verbose_name(self): 
        """
        Tests that the meta setting is in place
        """
        self.assertEqual(str(Iris._meta.verbose_name_plural), 'Irises')
    

    def test_upload_good_file(self):
        """
        Upload a file,
        Test that redirect works
        """
        c = Client()
        with open('C:/Users/jeffe/Google Drive/Programming/docker/tf_site/tf_site/iris/static/tf_site/datasets/iris.csv') as f: 
            response = c.post('/iris/upload/', {'title': 'test_upload.csv', 'file': f}, follow=True)
        print('response: ', response)

        # Successful upload redirects to /iris/upload/success (if using follow=False)
        # self.assertEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 200) # using follow=True, successful page get should be 200

        # Verify that the url is in the right place: /iris/upload/success: <h1>File was successfully uploaded</h1>
        self.assertContains(response, 'success', status_code=200) 


    def test_upload_bad_file(self):
        """
        Attempt to upload file that does not exist
        """
        c = Client()
        # how can you open() a file that doesn't exist?
        #   fail to provide a file (required field) <-- validated on form`
        response = c.post('/iris/upload/', {
            'title': 'bad file upload', 
            'file': ''
            # 'file': open('C:/Users/jeffe/Google Drive/Programming/docker/tf_site/tf_site/iris/statis/tf_site/datasets/iris2.csv')
        })
        print('resp2: ', response)
    
    
    def test_upload_duplicate_filename(self):
        """
        Attempt to upload a file that already exists with that name
        """
        pass 

    def test_upload_noload(self):
        """
        Upload a file that does not load to model
        """
        pass 

    def test_upload_load_append(self):
        """
        Upload a file that appends data to model 
        """
        pass

    def test_upload_load_replace(self):
        """
        Upload a file that replaces existing model data
        """
        pass




