import sys
from flask_cors import CORS
from flask import Flask, redirect, request, jsonify, url_for, render_template

from .entities.entity import Session, engine, Base
from .entities.phone_book import PhoneBook, PhoneBookSchema


app = Flask(__name__)

CORS(app)

# generate database schema
Base.metadata.create_all(engine)


@app.route('/', methods=['GET'])
def index():
    return redirect('https://hrhyv2.site/')


@app.route('/phones', methods=['GET'])
def get_phone():
    session = Session()
    phone_objects = session.query(PhoneBook)\
                           .order_by(PhoneBook.id.desc()).all()
    schema = PhoneBookSchema(many=True)
    phones = schema.dump(phone_objects)
    session.close()
    
    return jsonify(phones), 200





@app.route('/addPhone', methods=["POST"])
def add_phone():
    requestData = request.get_json()
    print(requestData)

    _name = requestData.get('name')
    _phone = requestData.get('phone')

    new_phone = PhoneBook(name=_name, phone=_phone, 
                          created_by="HRHYv2")

    session = Session()
    session.add(new_phone)
    session.commit()
    session.close()

    return "OK", 200




@app.route('/updatePhone', methods=["POST"])
def update_phone():
    requestData = request.get_json()
    print(requestData)

    _targetId = requestData.get('targetId')
    _name = requestData.get('name')
    _phone = requestData.get('phone')

    session = Session()

    new_phone = PhoneBook(name=_name, phone=_phone, created_by="HRHYv2")
    new_phone.id = _targetId

    session.merge(new_phone)

    '''
    session.query(PhoneBook).filter_by(id=_targetId)\
           .update({'name':_name, 'phone':_phone})
    '''

    session.commit()
    session.close()



    return 'OK', 200




@app.route('/deletePhone', methods=["POST"])
def delete_phone():
    requestData = request.get_json()
    print(requestData)

    _targetId = requestData.get('targetId')

    session = Session()
    session.query(PhoneBook).filter_by(id=_targetId).delete()
    '''
    select * from phone_book where id = _targetId
    delete from phone_book where id = _targetId
    '''
    session.commit()
    session.close()

    return 'OK', 200
     
if __name__ == '__main__':
# app.run(host='0.0.0.0')
 if len(sys.argv) > 1:
     app.debug = True
     app.jinja_env.auto_reload = True
     app.config['TEMPLATES_AUTO_RELOAD'] = True
     app.run(host='0.0.0.0', port=4000)
 else:
     app.run(host='0.0.0.0')