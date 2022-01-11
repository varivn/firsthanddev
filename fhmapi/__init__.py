import json
from unittest.suite import TestSuite
from flask import Flask, request, abort
from flask.json import jsonify
from flask_cors import CORS

from models import db, setup_db, Producer, Buyer, Sale
from .auth.auth import AuthError, requires_auth


RESULTS_PER_PAGE = 8
# categories_dic = {}
# current_category = None

def paginate_results(request, selection):

    page = request.args.get("page", 1, type=int)
    start = (page-1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    results = [result.format() for result in selection]
    current_results = results[start:end]
    
    return current_results

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Controll-Allow-Origin','*')
        response.headers.add('Access-Controll-Allow-Headers', 'Content-Type, Authorization, True' )
        response.headers.add('Access-Controll-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def project_starting():
        return jsonify({'message':'Landing page goes here!!!'})

    @app.route('/producers', methods=['GET', 'POST'])
    def get_post_producers():

        if request.method == 'GET':
            try:
                all_producers = Producer.query.order_by(Producer.id).all()

                current_producers = paginate_results(request, all_producers)

                if len(current_producers) == 0:
                    abort(404)

                return jsonify({
                'success':True,
                'producers_count':len(current_producers),
                'producers_data':current_producers
                })

            except Exception as e:
                print(e)
                abort(404)            
        
        if request.method == 'POST':
            
            request_body = request.get_json()

            try:
                new_producer_name = request_body.get('name', None)
                new_producer_country = request_body.get('country', None)
                new_producer_products = request_body.get('products', None)

                if new_producer_name == "":
                    abort(422)
                elif new_producer_country == "":
                    abort(422)
                elif new_producer_products == "":
                    abort(422)
                else:
                    new_producer = Producer(name=new_producer_name, country=new_producer_country, products=new_producer_products)

                    new_producer.insert()

                    return jsonify({
                    'success': True,
                    'newlycreated_producer': new_producer.format()
                    })

            except Exception as e:
                print(e)
                abort(422)            

    @app.route('/producers/<int:producer_id>', methods=['PATCH'])
    def update_producer(producer_id):
        try:
            producer = Producer.query.filter(Producer.id==producer_id).one_or_none()

            request_body = request.get_json()

            new_name = request_body.get('name', producer.name)
            new_country = request_body.get('country', producer.country)
            new_products = request_body.get('products', producer.products)

            if producer.name != new_name:
                producer.name = new_name
            if producer.country != new_country:
                producer.country = new_country
            if producer.products != new_products:
                producer.products = new_products

            producer.update()

            return jsonify({
            'success':True,
            'updated_producer':producer.format()
        })
        except Exception as e:
            print(e)
            abort(422)
        
        
    @app.route('/producers/<int:producer_id>', methods=['DELETE'])
    def delete_producer(producer_id):
        try:
            producer = Producer.query.filter(Producer.id==producer_id).one_or_none()

            if producer == None:
                abort(404)
            
            producer.delete()

            return jsonify({
            'success':True,
            'deleted_record':producer.format()
            })
        
        except Exception as e:
            print(e)
            abort(404)
        
    '''
    HANDLING BUYER'S MODEL CRUD OPERATIONS 
    '''
    @app.route('/buyers')
    def retrieve_buyers():
        try:
            all_buyers = Buyer.query.order_by(Buyer.id).all()

            current_buyers = paginate_results(request, all_buyers)

            if len(current_buyers) == 0:
                abort(404)

            return jsonify({
            'success':True,
            'current_buyers':current_buyers
        }) 

        except Exception as e:
            print(e)
            abort(404)
        
    @app.route('/buyers', methods=['POST'])
    def add_newbuyer():
        request_body = request.get_json()
        try:
            name = request_body.get('name', None)
            products = request_body.get('comercialized_products', None)
            
            new_buyer = Buyer(name=name, comercialized_products=products)
            new_buyer.insert()
            
            return jsonify({
            'success':True,
            'the_new_buyer':new_buyer.format()
            })
        except Exception as e:
            print(e)
            abort(422)
        
    
    @app.route('/buyers/<int:buyer_id>', methods=['PATCH'])
    def update_buyer(buyer_id):

        try:
            buyer = Buyer.query.filter(Buyer.id==buyer_id).one_or_none()
            request_body = request.get_json()

            new_name = request_body.get('name', buyer.name)
            new_products = request_body.get('comercialized_products', buyer.comercialized_products)

            if new_name != buyer.name:
                buyer.name = new_name

            if new_products != buyer.comercialized_products:
                buyer.comercialized_products = new_products

            buyer.update()

            return jsonify({
            'success':True,
            'data': buyer.format()
            })

        except Exception as e:
            print(e)
            abort(422)
     
    @app.route('/buyers/<int:buyer_id>', methods=['DELETE'])
    def delete_buyer(buyer_id):
        try:
            buyer = Buyer.query.filter(Buyer.id==buyer_id).one_or_none()

            if buyer == None:
                abort(404)

            buyer.delete()

            return jsonify({
            'success':True,
            'data': buyer.format()
            })
        
        except Exception as e:
            print(e)
            abort(422)        

# ------------------------------------------------------------------------------------
#  Sale Model-------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
    '''
    Endpoint for register a new sale and retrieve all sales
    Accepts GET AND POST request methods
    '''
    @app.route('/sales', methods=['GET', 'POST'])
    def getandpost_sales():

        if request.method == 'GET':
        
            try:
                all_sales = Sale.query.all()

                current_sales = paginate_results(request, all_sales)

                if len(current_sales) == 0:
                    abort(404)

                return jsonify({
                    'success':True,
                    'total_sales': len(all_sales),
                    'current_sales': current_sales
                })
            except Exception as e:
                print(e)
                abort(404)
        
        if request.method == 'POST':
            try:
                request_body = request.get_json()
                p_id = request_body.get('producer_id', None)
                b_id = request_body.get('buyer_id', None)

                if p_id | b_id == None:
                    abort(422)

                new_sale = Sale(producer_id=p_id, buyer_id=b_id)

                new_sale.insert()

                return jsonify({
                    'success':True,
                    'the_new_sale': new_sale.format()
                })
            except Exception as e:
                print(e)
                abort(422)

    # Retrieve Sale Details
    @app.route('/sales/<int:sale_id>')
    def sale_detail(sale_id):
        try:
            sale = Sale.query.filter(Sale.id == sale_id).one_or_none()

            if sale is None:
                print('Sale is a None result query')
                abort(404)
            else:
                return jsonify({
                'success':True,
                'sale': sale.format()
            })
        except Exception as e:
            print(e)
            abort(404)

    # Retrieve sales by producer / Esta ruta puede sólo ser accesada por producers
    @app.route('/producers/<int:p_id>/sales')
    @requires_auth('get:sales')
    def sales_by_producer(payload, p_id):
        try:
            # sales_by_p = Sale.query.filter('producer_id' == p_id).all()
            sales_by_p = db.session.query(Sale, Producer).join(Producer).filter(Producer.id == p_id).all()           

            if len(sales_by_p) == 0:
                abort(404)

            for sale, producer in sales_by_p:
                pass
                   
            return jsonify({
                'success':True,
                'sale_buyer_id': sale.producer_id,
                'producer_name': producer.name,
                'producer_products':producer.products,
                'total_sales': len(sales_by_p)
            })

        except Exception as e:
            print(e)
            abort(404)
    
    # Retrieve sales by buyer / Esta ruta puede ser accesada sólo por Buyers
    @app.route('/buyers/<int:b_id>/sales')
    @requires_auth('get:purchases')
    def sales_by_buyer(payload, b_id):
        try:
            purchases_by_b = db.session.query(Sale, Buyer).join(Buyer).filter(Buyer.id == b_id).all()

            if len(purchases_by_b) == 0:
                abort(404)

            for purchase, buyer in purchases_by_b:
                purchase_buyerid = purchase.buyer_id
                buyer_name = buyer.name                

            return jsonify({
                'success': True,
                'sale_buyer_id': purchase_buyerid,
                'buyer_name': buyer_name,
                'total_purchases': len(purchases_by_b)
            })

        except Exception as e:
            print(e)
            abort(404)

    '''
    Handling 400 error
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success':False,
            'error':'400',
            'message':'Bad request'
        }), 400

    '''
    Handling 404 error
    '''
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success':False,
            'error':'404',
            'message':'Page not found'
        }), 404
    '''
    Handling 405 error
    '''
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success':False,
            'error':'405',
            'message':'Method not allowed by the endpoint'
        }), 405
    
    '''
    Handling 422 error
    '''    
    @app.errorhandler(422)
    def unproccessable_request(error):
        return jsonify({
            'success':False,
            'error':'422',
            'message':'Unproccessable entity'
        }), 422
    '''
    Error handler for AuthError
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        return jsonify({
            'success':False,
            'error':e.status_code,
            'message':e.error
        }),e.status_code

    '''
    Handling 401 error
    '''
    @app.errorhandler(401)
    def auth_error(error):
        return jsonify({
            'success':False,
            'error':401,
            'message':'Unauthorized'
        }),401

    '''
    Handling 403 error
    '''
    @app.errorhandler(403)
    def auth_error(error):
        return jsonify({
            'success':False,
            'error':403,
            'message':'Forbidden'
        }),403

    return app