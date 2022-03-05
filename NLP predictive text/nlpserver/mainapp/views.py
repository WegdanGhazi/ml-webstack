from django.http import HttpResponse
import json
from django.core import serializers
from mainapp.models import PredictionFeedback
from nlpmodel.combined_prediction import predict_combined


def index(request):
    """ Parse post request and return the result """
    if request.method == 'POST':
        # Return the result
        result = json.loads(request.body.decode('utf-8'))["message"]
        text_prediction, topic_detection, sentiment = predict_combined(result)
        print(text_prediction)
        print(topic_detection)
        print(sentiment['label'])

        """ return json http response """
        return HttpResponse(json.dumps(
            {
                "answer": text_prediction,
                "topic": topic_detection,
                "sentiment" : sentiment["label"]
            }), content_type="application/json")
    else:
        return HttpResponse('Please use a POST request')


def receive_feedback(request):
    """ Parse post request and return the result """
    if request.method == 'POST':
        # Return the result
        request_json = json.loads(request.body.decode('utf-8'))
        feedback_object = PredictionFeedback.objects.create(**request_json)
        PredictionFeedback.save(feedback_object)

        """ return json http response """
        return HttpResponse(json.dumps("saved"), content_type="application/json")
    elif request.method == 'GET':
        objects_as_json = serializers.serialize('json', PredictionFeedback.objects.all())
        return HttpResponse(objects_as_json, content_type='application/json')
    else:
        return HttpResponse('Please use a POST or GET request')