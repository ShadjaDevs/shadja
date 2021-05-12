<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-row>
        <ion-col size = "1">
          <ion-button @click="openStart">
            <ion-icon :icon="menuOutline"></ion-icon>
          </ion-button>
        </ion-col>
        <ion-col>
          <ion-title class = "mainTitle"> Sign Up For Updates </ion-title>
        </ion-col>
        </ion-row>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <div v-if='!isAuthenticated'>
        <div v-show="!(validateMobileNumber || validateEmailID)">
        <ion-card>
       <ion-list>
         <ion-radio-group @ionChange = "updateSubscription($event)" value="0">
           <ion-list-header>
            <ion-label>Subscription plan?</ion-label>
           </ion-list-header>
          <ion-item >
            <ion-label>{{subscriptionOptions[0].text}}</ion-label>
            <ion-radio slot="start" value="1">></ion-radio>
          </ion-item>
          <ion-item >
            <ion-label>{{subscriptionOptions[1].text}}</ion-label>
            <ion-radio slot="start" value="7">></ion-radio>
          </ion-item>
          <ion-item >
            <ion-label>{{subscriptionOptions[2].text}}</ion-label>
            <ion-radio slot="start" value="30">></ion-radio>
          </ion-item>
          <ion-item >
            <ion-label>{{subscriptionOptions[3].text}}</ion-label>
            <ion-radio slot="start" value="0">></ion-radio>
          </ion-item>
         </ion-radio-group>
      </ion-list>
        </ion-card>
        <ion-card id = "details">
         <form @submit.prevent="onSubmit" novalidate>

        <div>
          <ion-item>
            <ion-label position="floating">Mobile Number</ion-label>
            <ion-input type="numeric" name="mobileNumber" v-model="vv.mobileNumber.$model"/>
          </ion-item>
          <p class="formInfo"> Please enter a valid mobile number</p>
        </div>

        <div>
          <ion-item>
            <ion-label position="floating">Email</ion-label>
            <ion-input
              type="email"
              name="emailAddress"
              v-model="vv.emailAddress.$model"
            />
          </ion-item>
          <p class="formInfo"> Please enter a valid email address</p>
        </div>

        <div>
          <ion-item>
            <ion-label position="floating">ZipCode</ion-label>
            <ion-input type="numeric" name="mobileNumber" v-model="vv.zipCode.$model"/>
          </ion-item>
          <p class="formInfo">Please enter a valid zipcode</p>
        </div>

        <div>
          <ion-button v-if="!vv.$invalid && (vv.emailAddress.$model || vv.mobileNumber.$model)" type="submit" @click="sendInfo">SUBMIT</ion-button>
          <ion-button v-if="vv.$invalid || (!vv.emailAddress.$model && !vv.mobileNumber.$model)" type="submit" disabled
            >SUBMIT</ion-button
          >
        </div>
      </form>
        </ion-card>
      </div>
      <div> 
        <ion-card v-show="validateMobileNumber && validateEmailID" class="details">
          <div v-show="validateMobileNumber">
          <ion-item>
            <ion-input type="numeric" name="mobileOTP" v-model="userMobileOTP"/>
          </ion-item>
          <p class="formInfo"> Please enter the OTP sent to your mobile</p>
        </div>

        <div>
          <ion-item v-show="validateEmailID">
            <ion-input type="numeric" name="emailOTP" v-model="userEmailOTP"/>
          </ion-item>
          <p class="formInfo"> Please enter the OTP sent to your email</p>
        </div>
        <div>
          <ion-button type="submit" @click="sendOTPInfo">SUBMIT</ion-button>
        </div>
        </ion-card>
      </div>
      </div>
      <login v-else id="login" emitMetaData="recieveMetaData($event)"></login>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonRadio, IonRadioGroup, IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  toastController } from '@ionic/vue';
//import ExploreContainer from '@/components/ExploreContainer.vue';
import { menuOutline } from 'ionicons/icons';
import { menuController } from "@ionic/vue";
import { mapState } from 'vuex';
import Login from './login.vue';
import useDataService from '../services/data.service';
import { reactive, toRef } from "vue";
import { useRouter } from "vue-router";

import { useVuelidate } from "@vuelidate/core";
import { required, email, minLength, maxLength } from "@vuelidate/validators";
import { isPossiblePhoneNumber } from 'libphonenumber-js'


export default  {
  name: 'Tab2',
  components: { IonRadio, IonRadioGroup, IonHeader, IonToolbar, IonTitle, IonContent, IonPage, Login,
  IonItem,
  IonLabel,
  IonInput,
  IonButton },
  data() {
    return {
      model: '',
      subscriptionPeriod: 0,
      tempVV: {},
      userMobileOTP : '',
      userEmailOTP: '',
      validateMobileNumber: false,
      validateEmailID: false
    }
  },
  setup() {
    const { zipCode, searchRadius } = useDataService();

    const fform = reactive({
      mobileNumber: "",
      emailAddress: "",
      zipCode: zipCode
    });
    const isMobileNumberValid = (value) => {
      if(!value) {
        return true;
      }
        return isPossiblePhoneNumber(value, 'IN') === true && isNumeric(value);
    };
    const isNumeric = (n)=> {
      return !isNaN(parseFloat(n)) && isFinite(n) && n>=0;
    }
    const rules = {
      mobileNumber: { isMobileNumberValid },
      emailAddress: { email },
      zipCode: {required, minLength: minLength(6), maxLength: maxLength(6), isNumeric}
    };
    const vv = useVuelidate(rules, {
      mobileNumber: toRef(fform, "mobileNumber"),
      emailAddress: toRef(fform, "emailAddress"),
      zipCode: toRef(fform, "zipCode")
    });
    // handle the submit of the form, only called
    // if the form is valid
    const onSubmit = () => {
      vv.value.$touch();

      if (vv.value.$invalid) return;

      //console.log(vv);
      //alert("Form has been submitted! " + JSON.stringify(fform, null, 2));
      //console.log(fform);
    };
    const subscriptionOptions = [
      { val: '1', text: '1 day' },
      { val: '7', text: '7 days' },
      { val: '30', text: '30 days' },
      { val: '0', text: 'Till I cancel' },
    ];
    return {
      menuOutline,
      subscriptionOptions,
      zipCode,
      searchRadius,
      router: useRouter(),
      onSubmit,
      vv
    }
  },
  computed: {
      ...mapState("auth", ['isAuthenticated'])
  },
methods: {
  async handleToast() {
      const toast = await toastController.create({
        color: 'dark',
        duration: 2000,
        message: 'Request submitted'
      });

      await toast.present();
    },
  openStart() {
      menuController.open("mainMenu");
      //let a = document.querySelector('#startDate');
      console.log(this.startDate);
      console.log(this.zipCode, this.searchRadius);
    },
  updateSubscription(event) {
    console.log(event);
    this.subscriptionPeriod = event.detail.value;
  },
  sendInfo(){
    console.log(this.vv);
    this.validateMobileNumber =  true;
    this.validateEmailID = true;
  },
  resetData()
  {
    this.validateMobileNumber = false;
    this.validateEmailID = false;
    this.vv.mobileNumber.$model = '';
    this.vv.emailAddress.$model = '';
    this.vv.zipCode.$model = '';
  },
  sendOTPInfo() {
    this.handleToast();
    console.log(this.userMobileOTP, this.userEmailOTP);
    setTimeout(() => { this.resetData(); this.$router.replace('/tabs/tab3') }, 2000);
    
  }
},
}
</script>
<style scoped>
#login {
  padding-top: 55px !important;
}
.formInfo {
  font-size: smaller;
  font-style: italic;
  font-weight: 500;
  margin-top: 4px;
}
#details {
  margin-bottom: 80px;
}
.mainTitle {
  margin-left: 5px;
  padding-top: 10px;
}
</style>