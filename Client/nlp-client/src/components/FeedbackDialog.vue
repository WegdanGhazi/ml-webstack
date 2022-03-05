<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>
        <span class="text-h6">{{ title }}</span>
      </v-card-title>
      <v-card-subtitle>
        <span class="font-weight-light" v-if="message">{{ message }}</span>
      </v-card-subtitle>
      <v-card-text v-show="!!message">
        <v-container>
          <v-row
            ><div class="text-subtitle-1 font-weight-medium">
              Text: {{ sentence }}
            </div></v-row
          >
          <v-row v-if="predictionType == 'TEXT_PREDICTION'">
            <v-text-field
              v-model="correctAnswer"
              label="Enter correct prediction"
              required
            ></v-text-field>
          </v-row>
          <v-row v-else-if="predictionType == 'SENTIMENT_ANALYSIS'">
            <v-select
              :items="sentimentItems"
              v-model="correctAnswer"
              label="Enter correct prediction"
              required
            ></v-select>
          </v-row>
          <v-row v-else-if="predictionType == 'TOPIC_PREDICTION'">
            <v-select
              :items="topicItems"
              v-model="correctAnswer"
              label="Enter correct prediction"
              required
            ></v-select>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="cancel"> Close </v-btn>
        <v-btn color="blue darken-1" text v-on:click="agree"> Save </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";

export default {
  name: "FeedbackDialog",
  data() {
    return {
      dialog: false,
      resolve: null,
      reject: null,
      predictionType: null,
      message:
        "Enter the correct prediction to save it and help further training",
      title: "Improve this prediction",
      correctAnswer: null,
      sentence: null,
      sentimentItems: ["POSITIVE", "NEGATIVE", "NEUTRAL"],
      topicItems: ["World", "Sports", "Business", "Sci/Tech"],
    };
  },
  methods: {
    open(predictionType, sentence) {
      this.dialog = true;
      this.sentence = sentence;
      this.predictionType = predictionType;
    },
    agree() {
      axios
        .post("http://localhost:8000/predict/feedback/", {
          "prediction_text": this.sentence,
          "prediction_type": this.predictionType,
          "correct_prediction": this.correctAnswer,
        })
        .then((response) => {
          console.log(response);
        })
        .catch((e) => {
          console.log(e);
        })
        .finally(() => {
          this.correctAnswer = "";
          this.dialog = false;
        });
    },
    cancel() {
      this.dialog = false;
    }
  },
};
</script>