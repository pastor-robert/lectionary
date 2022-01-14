from flask import Flask, abort
from flask_restx import Resource, Api, reqparse
from flask_restx import inputs, fields

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return ['hello', 'world']


@api.route('/lects/<int:lect_id>', endpoint='goober')
class Lect(Resource):
    model = api.model('Lection', {
        'id': fields.String,
        'season': fields.String,
        'short_name': fields.String,
        'long_name': fields.String,
        'note': fields.String,
        'first_reading': fields.String,
        'psaslm': fields.String,
        'second_reading': fields.String,
        'gospel': fields.String,
        })

    listModel = api.model('LectionList', {
        'lections': fields.List(fields.Nested(model)),
        })

    @api.marshal_with(listModel)
    def get(self, lect_id):
        parser = reqparse.RequestParser()
        parser.add_argument(
                'rate', type=int, help='Flow rate for the whozinator')
        parser.add_argument(
                'start_date',
                type=inputs.date,
                help='Beginning of time',
                default='1970-01-01')
        parser.add_argument(
                'end_date', type=inputs.date, help='End of time')
        args = parser.parse_args()
        if lect_id == 13:
            abort(400, description="Don't give me a thirteen")
        return {
                'lections':
                [ 
                    {
                        'id': lect_id,
                        'rate': args.rate,
                        'start_date': str(args.start_date),
                        'end_date': str(args.end_date),
                        'note': 'This is a note!',
                    }
                ]
            }
               

if __name__ == '__main__':
    app.run(debug=True)
