from nlpmodel.text_prediction_model.combined_model import predict_sentence
from nlpmodel.sentiment_analysis_model.MacShihabPreds import predict
from nlpmodel.topic_detection_model.automation import predict_topic


def predict_combined(sentence):
    prediction = predict_sentence(sentence)
    topic = predict_topic(sentence)
    sentiment = predict(sentence)
    return prediction, topic, sentiment