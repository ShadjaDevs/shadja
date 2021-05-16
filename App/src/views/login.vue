<template>
  <ion-page>
    <form @submit.prevent="handleLogin">
      <ion-card>
        <ion-item>
          <h3>Please Sign In!</h3>
        </ion-item>
        <ion-item>
          <ion-label position="floating">Username</ion-label>
          <ion-input v-model="form.username" id="username" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Password</ion-label>
          <ion-input type="password" v-model="form.password" id="password" required></ion-input>
        </ion-item>

        <ion-item>
          <ion-button type="submit" shape="round">
            Sign In
            <ion-icon slot="end" :icon="logIn"></ion-icon>
          </ion-button>
        </ion-item>
        <ion-item>
          <p>Or</p>
        </ion-item>
        <ion-item>
          <ion-button type="button" shape="round" router-link="/signup">
            Sign Up
            <ion-icon slot="end" :icon="personAdd"></ion-icon>
          </ion-button>
        </ion-item>
      </ion-card>
    </form>
  </ion-page>
</template>

<script>
import { IonPage, IonCard, IonItem, IonLabel, IonButton, IonInput, alertController, IonIcon } from '@ionic/vue'
import { logIn, personAdd } from 'ionicons/icons';
import { mapActions, mapGetters } from "vuex"
import { useRouter } from 'vue-router';
import userDataService from '../services/user.service';
export default {
  name: 'SignIn',
  components: { IonPage, IonCard, IonItem, IonLabel, IonButton, IonInput, IonIcon },
  setup() {
    const router = useRouter();
    const { user } = userDataService();
    return {
      router,
      logIn,
      personAdd,
      user
    };
  },
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  },
  computed: {
    ...mapGetters("auth", [
      "authenticating",
      "authenticationError",
      "authenticationErrorCode"
    ])
  },
  methods: {
    ...mapActions("auth", ["signIn"]),
    async handleLogin() {
      this.signIn(this.form).then((data) => {
        this.form.username = "";
        this.form.password = "";
        this.user.value = data;
        this.router.push("/tabs/tab2");
      }).catch(async (err) => {
        const errorAlert = await alertController
            .create({
              header: 'Failed',
              subHeader: 'Sign in Failed',
              message: err,
              buttons: ['OK'],
            });
        await errorAlert.present()
      })
    }
  }
}
</script>