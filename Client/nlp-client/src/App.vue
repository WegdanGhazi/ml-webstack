<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <span>NLP Prediction model</span>
    </v-app-bar>

    <v-main>
      <!-- centered v-container -->
      <v-container fluid fill-height>
        <v-layout align-center justify-center column>
          <v-card width="500">
            <v-card-text>
              <v-container>
                <v-row>
                  <v-text-field v-model="text" label="Text"> </v-text-field
                ></v-row>
                <v-row class="d-flex justify-center">
                  <v-btn color="primary" fab dark small @click="predict">
                    <v-icon>mdi-text-search</v-icon>
                  </v-btn></v-row
                >
              </v-container>
            </v-card-text>
          </v-card>
          <v-card width="500" class="mt-5">
            <v-card-text>
              <v-container>
                <v-row v-if="!prediction && !loading">
                  <span class="font-italic">
                    Enter text to predict the next word.
                  </span>
                </v-row>
                <v-row v-else-if="!loading">
                  <v-card
                    outlined
                    style="width: 100%; margin-top: 10px"
                    height="100px"
                  >
                    <v-card-text
                      style="
                        height: 100px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                      "
                    >
                      <v-container class="d-flex justify-space-between py-0">
                        <span class="d-flex align-center">sentiment</span>
                        <v-btn color="green" fab dark x-small @click="showDialog('SENTIMENT_ANALYSIS')">
                          <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                      </v-container>
                      <p class="d-flex justify-center text-button">
                        {{ sentiment }}
                      </p>
                    </v-card-text>
                  </v-card>
                  <v-card
                    outlined
                    color="outlined"
                    style="width: 100%; margin-top: 10px"
                    height="100px"
                  >
                    <v-card-text
                      style="
                        height: 100px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                      "
                    >
                      <v-container class="d-flex justify-space-between py-0">
                        <span class="d-flex align-center">prediction</span>
                        <v-btn color="green" fab dark x-small @click="showDialog('TEXT_PREDICTION')">
                          <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                      </v-container>
                      <p class="d-flex justify-center text-button">
                        {{ prediction }}
                      </p>
                    </v-card-text>
                  </v-card>
                  <v-card
                    outlined
                    style="width: 100%; margin-top: 10px"
                    height="100px"
                  >
                    <v-card-text
                      style="
                        height: 100px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                      "
                    >
                      <v-container class="d-flex justify-space-between py-0">
                        <span class="d-flex align-center">topic</span>
                        <v-btn color="green" fab dark x-small @click="showDialog('TOPIC_DETECTION')">
                          <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                      </v-container>
                      <p class="d-flex justify-center text-button">
                        {{ topic }}
                      </p>
                    </v-card-text>
                  </v-card>
                </v-row>
                <v-row v-else>
                  <v-progress-linear
                    indeterminate
                    color="cyan"
                  ></v-progress-linear>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-layout>
      </v-container>
    <FeedbackDialog ref="dialogModal"/>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";
import FeedbackDialog from "./components/FeedbackDialog.vue"

export default {
  name: "App",
  components: {
      FeedbackDialog
    },
  data: () => ({
    text: "",
    prediction: "",
    topic: "",
    sentiment: "",
    emotion: {
      icon: "mdi-emoticon-happy",
      color: "green darken-2",
    },
    loading: false,
  }),
  methods: {
    predict() {
      // send http request to backend
      this.loading = true;
      axios
        .post("http://localhost:8000/predict/", { message: this.text })
        .then(
          (response) => {
            this.prediction = response.data.answer;
            this.topic = response.data.topic;
            this.sentiment = response.data.sentiment;
          },
          (response) => {
            console.log(response);
          }
        )
        .finally(() => {
          this.loading = false;
        });
    },
    showDialog(type){
      this.$refs.dialogModal.open(type, this.text);
    }
  },
};
</script>