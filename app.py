from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):              ##kisileri Listelemeyi saglarız.
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')  ##data'yı dict formatına cevirip tekrar data'ya atma.
        return {'data': data}, 200

    def post(self):             ##uygun resource yardımıyla kisi eklemeyi saglarız ve ekleneni yazdırırız.
        name = request.args['name']
        age = request.args['age']
        city = request.args['city']     ##talep edilen parametreleri ilgili args'lara esitleme.

        data = pd.read_csv('users.csv')  ##eklenen veriler ekrana yazıdırlır

        new_data = pd.DataFrame({
            'name': [name],
            'age' : [age],
            'city': [city]
        })  ##yeni eklemeleri new_data'ya ekleme.

        data = data.append(new_data, ignore_index=True)  ##yeniData'yı varsayılan index seklinde data'ya ekle.
        data.to_csv('users.csv', index=False)            ##
        return {'data': new_data.to_dict('records')}, 200

    def delete(self):            ##uygun resource yardımıyle isim bazında kisiyi silmemizi saglar.
        name = request.args['name']
        data = pd.read_csv('users.csv')
        data = data[data['name'] != name]

        data.to_csv('users.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200


class Cities(Resource):
    def get(self):               ##uygun resource yardımıyla tum sehirleri listeleriz. Aslında index bazında sütun listelenir.
        data = pd.read_csv('users.csv', usecols=[2])
        data = data.to_dict('records')

        return {'data': data}, 200


class Name(Resource):
    def get(self, name):      ##isim araması yaparız.
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200
        return {'message': 'No entry found with this name !'}, 404


api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')
##class bazında ilgili resource baslıkları.

if __name__ == "__main__":
    app.run()
