from src.app import ns, kb
from flask_restplus import Resource, fields


problem_description_model = ns.model('ProblemDescription', {'problemDescription': fields.String})
recommendation_model = ns.model('Recommendation', {'recommendation': fields.String})
feedback_model = ns.model(
    'Feedback',
    {
        'problemDescription': fields.String,
        'recommendation': fields.String,
        'didHelp': fields.Boolean
    }
)

complement_input_model = ns.model(
    'ProblemRecommendation',
    {
        'problemResume': fields.String,
        'recommendation': fields.String
    }
)


@ns.route('/GetRecommendations')
class GetRecommendation(Resource):
    @ns.doc(body=problem_description_model, required=True)
    @ns.response(200, 'Success', recommendation_model)
    def post(self):
        recommendations = kb.infer(ns.payload['problemDescription'])
        return [{'recommendation': r} for r in recommendations]


@ns.route('/LeaveFeedback')
class LeaveFeedback(Resource):
    @ns.doc(body=feedback_model, required=True)
    @ns.response(204, 'Success', None)
    @ns.response(400, 'Error', None)
    def post(self):
        data = ns.payload
        status = kb.rate_recommendation(
            data['problemDescription'],
            data['recommendation'],
            data['didHelp']
        )

        if status == 1:
            return 'Specified recommendation does not exist', 400
        else:
            return '', 204


@ns.route('/AddRecommendation')
class AddRecommendation(Resource):
    @ns.doc(body=recommendation_model, required=True)
    @ns.response(204, 'Success', None)
    @ns.response(400, 'Error', None)
    def post(self):
        status = kb.add_recommendation(ns.payload['recommendation'])

        if status == 1:
            return 'Recommendation already exists', 400
        else:
            return '', 204
