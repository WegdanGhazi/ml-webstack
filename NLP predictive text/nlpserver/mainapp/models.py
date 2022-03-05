from django.db import models

# Create your models here.

class PredictionFeedback(models.Model):
    """
    Model for storing the feedback of the user
    """
    prediction_text = models.TextField()
    prediction_type = models.CharField(max_length=10)
    is_correct = models.BooleanField(default=False)
    is_trained = models.BooleanField(default=False)
    correct_prediction = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prediction_text + " " + self.prediction_type
