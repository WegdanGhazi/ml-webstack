# Generated by Django 3.2.9 on 2022-01-16 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prediction_text', models.TextField()),
                ('prediction_type', models.CharField(max_length=10)),
                ('is_correct', models.BooleanField(default=False)),
                ('is_trained', models.BooleanField(default=False)),
                ('correct_prediction', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]