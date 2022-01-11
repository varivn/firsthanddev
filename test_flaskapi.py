import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from fhmapi import create_app
from models import setup_db


class ProducerTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fhmarket_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
        #     # create all tables
            self.db.create_all()
        
        self.new_producer = {"name":"Mauricio Cordoba", "country":"Guatemala", "products":["Aguacate","Lentejas"]}

        self.wrongformat_newproducer = {"name":"", "country":"", "products":""}

        self.update_producer = {"name":"Mauricio Cordoba", "country":"Guatemala", "products":["Aguacate","Lentejas", "Frijoles", "Arroz"]}
    
    '''TESTING PRODUCERS CRUD'''
    # Testing retrieve producers
    def test_get_producers(self):
      res = self.client().get('/producers?page=1')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['producers_data'])
      self.assertTrue(data['producers_count'])

    # Testing beyond page limit no producers results 404 http status code
    def test_404_getproducers(self):
        res = self.client().get('/producers?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['error'], '404')

    # Testing post a new producers
    # def test_post_producers(self):
    #     res = self.client().post('/producers', json=self.new_producer)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['newlycreated_producer'])

    # Testing post a new producer FAILS cause missing data
    def test_422_postproducer(self):
        res = self.client().post('/producers', json=self.wrongformat_newproducer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['error'], '422')
    
    # def test_delete_producers(self):
    #     res = self.client().delete('/producers/6')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['deleted_record'])

    # Test update an existen producer
    def test_update_producer(self):
        res = self.client().patch('/producers/5', json=self.update_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_producer'])
    
    # Test deleteting an unexistence producer 404 http status code
    def test_delete404_unexistence_producer(self):
        res = self.client().delete('/producers/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['error'], '404')

class SaleTestCase(unittest.TestCase):
    def setUp(self):
        '''Define test variables and initialize app'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fhmarket_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
        # create all tables
            self.db.create_all()

        self.producer_token = os.getenv('PRODUCER_TOKEN')
        self.producer_wrongpermission_token = os.getenv('PRODUCER_WRONGPERMISSIONS_TOKEN')        
        
        self.buyer_token = os.getenv('BUYER_TOKEN')
        self.buyer_wrongpermission_token = os.getenv('BUYER_WRONGPERMISSIONS_TOKEN')
    
    def tearDown(self):
        """Executed after each test"""
        pass        

    def test_get_sales(self):
        res = self.client().get('/sales?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_sales'])
        self.assertTrue(data['total_sales'])
    
    def test_404_get_sales(self):
        res = self.client().get('/sales?page=10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['error'], '404')

    # Test retrieve sales made by a producer
    def sales_by_producer(self):
        res = self.client().get('/producers/2/sales', headers = {"Authorization": "Bearer {}".format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_sales'])
        self.assertTrue(data['total_sales'])
    
    # Test non authorization header in request to retrieve sales by producer 401 http status code
    def sales_by_producer(self):
        res = self.client().get('/producers/2/sales')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    # Test wrong permissions in request to retrieve sales by producer 403 http status code
    def sales_by_producer(self):
        res = self.client().get('/producers/2/sales', headers = {"Authorization": "Bearer {}".format(self.producer_wrongpermission_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    # Test retrieve the purchases(sales) made by a buyer
    def sales_by_buyer(self):
        res = self.client().get('/buyers/1/sales', headers = {"Authorization": "Bearer {}".format(self.buyer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['sale_buyer_id'])
        self.assertTrue(data['buyer_name'])
        self.assertTrue(data['total_purchases'])
    
    # Test non authorization header in request to retrieve purchases by buyer 401 http status code
    def sales_by_buyer(self):
        res = self.client().get('/buyers/1/sales')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    # Test wrong permissions in request to retrieve purchases by buyer 403 http status code
    def sales_by_buyer(self):
        res = self.client().get('/buyers/1/sales')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

class BuyerTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fhmarket_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_buyer = {"name":"Julio Vargas Solano", "country":"Bolivia", "products":["Mariscos","Pescado entero fresco"]}

        self.wrongformat_newbuyer = {"name":"", "country":"", "products":""}

        self.updated_buyer = {"name":"Mauricio Cordoba", "country":"Guatemala", "products":["Aguacate","Lentejas"]}
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_buyer(self):
        res = self.client().get('/buyers?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['current_buyers'])

    # Test request buyers beyand pagination
    def test_404_buyer(self):
        res = self.client().get('/buyers?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['error'], '404')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()