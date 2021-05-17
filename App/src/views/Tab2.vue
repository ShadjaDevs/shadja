<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-row>
        <ion-col size = "1" v-show="showItem">
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
            <ion-label position="floating">Pincode</ion-label>
            <ion-input type="numeric" name="mobileNumber" v-model="vv.pinCode.$model"/>
          </ion-item>
          <p class="formInfo">Please enter a valid pincode</p>
        </div>

        <div>
          <ion-label position="floating">Radius</ion-label>
          <!-- <ion-input type="numeric" name="mobileNumber" v-model="vv.pinCode.$model"/> -->
          <ion-item>
              <ion-list>
                <ion-radio-group v-model="vv.radius.$model" value="100">
                  <ion-item >
                    <ion-label>{{radiusOptions[0].text}}</ion-label>
                    <ion-radio slot="start" value="5">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{radiusOptions[1].text}}</ion-label>
                    <ion-radio slot="start" value="10">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{radiusOptions[2].text}}</ion-label>
                    <ion-radio slot="start" value="25">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{radiusOptions[3].text}}</ion-label>
                    <ion-radio slot="start" value="50">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{radiusOptions[4].text}}</ion-label>
                    <ion-radio slot="start" value="100">></ion-radio>
                  </ion-item>
                </ion-radio-group>
              </ion-list>
          </ion-item>
        </div>

        <div>
          <ion-label position="floating">Age</ion-label>
          <!-- <ion-input type="numeric" name="mobileNumber" v-model="vv.pinCode.$model"/> -->
          <ion-item>
              <ion-list>
                <ion-radio-group v-model="vv.age.$model" value="1">
                  <ion-item >
                    <ion-label>{{ageOptions[0].text}}</ion-label>
                    <ion-radio slot="start" value="1">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{ageOptions[1].text}}</ion-label>
                    <ion-radio slot="start" value="2">></ion-radio>
                  </ion-item>
                </ion-radio-group>
              </ion-list>
          </ion-item>
        </div>

        <div>
          <ion-label position="floating">Vaccine Brand</ion-label>
          <!-- <ion-input type="numeric" name="mobileNumber" v-model="vv.pinCode.$model"/> -->
          <ion-item>
              <ion-list>
                <ion-radio-group v-model="vv.vaccineBrand.$model" value="Both">
                  <ion-item >
                    <ion-label>{{brandOptions[0].text}}</ion-label>
                    <ion-radio slot="start" value="Covaxin">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{brandOptions[1].text}}</ion-label>
                    <ion-radio slot="start" value="Covishield">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{brandOptions[2].text}}</ion-label>
                    <ion-radio slot="start" value="Both">></ion-radio>
                  </ion-item>
                </ion-radio-group>
              </ion-list>
          </ion-item>
        </div>

        <div>
          <ion-label position="floating">Vaccine Type</ion-label>
          <!-- <ion-input type="numeric" name="mobileNumber" v-model="vv.pinCode.$model"/> -->
          <ion-item>
              <ion-list>
                <ion-radio-group v-model="vv.vaccineType.$model" value="Both">
                  <ion-item >
                    <ion-label>{{typeOptions[0].text}}</ion-label>
                    <ion-radio slot="start" value="Free">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{typeOptions[1].text}}</ion-label>
                    <ion-radio slot="start" value="Paid">></ion-radio>
                  </ion-item>
                  <ion-item >
                    <ion-label>{{typeOptions[2].text}}</ion-label>
                    <ion-radio slot="start" value="Both">></ion-radio>
                  </ion-item>
                </ion-radio-group>
              </ion-list>
          </ion-item>
        </div>

        <div>
          <ion-label position="floating">Subscription Period</ion-label>
          <!-- <ion-input type="numeric" name="mobileNumber" v-model="vv.pinCode.$model"/> -->
          <ion-item>
              <ion-list>
                <ion-radio-group v-model="vv.period.$model" value="0">
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
          </ion-item>
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
      <div  v-show="validateMobileNumber || validateEmailID"> 
        <ion-card> 
          <div>
            <p> Your UUID is {{ UUID }}. <br> Please copy it and store it a secure place in case you want to make changes to this request in the future. </p>
            <ion-button @click="copyUUID()">Copy UUID</ion-button>
          </div>
        </ion-card>
        <ion-card class="details">
          <div v-show="validateMobileNumber">
          <ion-item>
            <ion-input type="numeric" name="mobileOTP" v-model="userMobileOTP"/>
          </ion-item>
          <p class="formInfo"> Please enter the 4 digit OTP sent to your mobile</p>
        </div>

        <div>
          <ion-item v-show="validateEmailID">
            <ion-input type="numeric" name="emailOTP" v-model="userEmailOTP"/>
          </ion-item>
          <p class="formInfo"> Please enter the 4 digit OTP sent to your email</p>
        </div>
        <div>
          <ion-button v-if="userEmailOTP.length == 4" type="submit" @click="sendOTPInfo">SUBMIT</ion-button>
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
  toastController,
  alertController } from '@ionic/vue';
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
import { isPossiblePhoneNumber } from 'libphonenumber-js';

import APIService from '../services/APIService.js';

import { Plugins } from '@capacitor/core';


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
      validateEmailID: true,
      subscriptionData: {
        modeOfContact: [],
        pinCode: 0,
        radius: 0,
        age: '',
        vaccineBrand: '',
        vaccineType: '',
        dateSubscribed: ''
      },
      showItem: false,
      UUID: "170f907e-7a9c-459c-a7fe-d36c5cee500e",
      otpVerified: false
    }
  },
  setup() {
    const { pinCode, searchRadius } = useDataService();

    const { Clipboard } = Plugins;

    const fform = reactive({
      mobileNumber: "",
      emailAddress: "",
      pinCode: pinCode,
      radius: null,
      age: "",
      vaccineBrand: "",
      vaccineType: "",
      period: ""
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
      pinCode: {required, minLength: minLength(6), maxLength: maxLength(6), isNumeric},
      radius: { required },
      age: { required },
      vaccineBrand: { required },
      vaccineType: { required },
      period: { required }
    };
    const vv = useVuelidate(rules, {
      mobileNumber: toRef(fform, "mobileNumber"),
      emailAddress: toRef(fform, "emailAddress"),
      pinCode: toRef(fform, "pinCode"),
      radius: toRef(fform, "radius"),
      age: toRef(fform, "age"),
      vaccineBrand: toRef(fform, "vaccineBrand"),
      vaccineType: toRef(fform, "vaccineType"),
      period: toRef(fform, "period")
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
      { val: 1, text: '1 day' },
      { val: 7, text: '7 days' },
      { val: 30, text: '30 days' },
      { val: 0, text: 'Till I cancel' },
    ];

    const radiusOptions = [
        { id: 0, text: '5km', value: 5, isActive: false},
        { id: 1, text: '10km', value: 10, isActive: false },
        { id: 2, text: '25km', value: 25, isActive: false },
        { id: 3, text: '50km', value: 50, isActive: false },
        { id: 4, text: '100km', value: 100, isActive: false },
        { id: 5, text: '500km', value: 500, isActive: false }
      ];

    const ageOptions = [
      { val: '1', text: '18 - 44' },
      { val: '2', text: '45+' }
    ];

    const brandOptions = [
      { val: 'covaxin', text: 'Covaxin' },
      { val: 'covishield', text: 'Covishield' },
      { val: 'both', text: 'Both' }
    ];

    const typeOptions = [
      { val: 'Free', text: 'Free' },
      { val: 'Paid', text: 'Paid' },
      { val: 'Both', text: 'Both' }
    ];
    return {
      menuOutline,
      subscriptionOptions,
      pinCode,
      searchRadius,
      router: useRouter(),
      onSubmit,
      vv,
      radiusOptions,
      ageOptions,
      brandOptions,
      typeOptions,
      Clipboard
    }
  },
  computed: {
      ...mapState("auth", ['isAuthenticated'])
  },
methods: {
  async handleToast(m) {
      const toast = await toastController.create({
        color: 'dark',
        duration: 2000,
        message: m
      });

      await toast.present();
    },
  copyUUID() {
    this.Clipboard.write({
      string: this.UUID
    });
    this.handleToast('Copied');
    if (this.otpVerified) {
      setTimeout(() => { this.presentConfirm(); }, 1000);
    }
  },
  openStart() {
      menuController.open("mainMenu");
      //let a = document.querySelector('#startDate');
      console.log(this.vv);
    },
  updateSubscription(event) {
    console.log(event);
    this.subscriptionPeriod = event.detail.value;
  },
  dateToString(dateObj) {
    let tempDate = new Date(dateObj);
    let dd = String(tempDate.getDate()).padStart(2, '0');
    let mm = String(tempDate.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = tempDate.getFullYear();
    let strToRet = dd + '-' + mm + '-' + yyyy;
    return strToRet; 
  },
  async presentConfirm() {
    const alert = await alertController
        .create({
          cssClass: 'my-custom-class',
          header: 'ALERT',
          message: 'Did you copy your UUID?',
          buttons: [
            {
              text: 'No',
              role: 'cancel'
            },
            {
              text: 'Yes',
              handler: () => {
                this.resetData();
              }
            }
        ]
        });
      return alert.present();
  },
  sendInfo(){
    let api = new APIService;
    api.getNearByPinCodes(this.vv.pinCode.$model, this.vv.radius.$model).then((response) => {
        let formData = {
          'old': false,
          'pincodes': response.data.pincodes,
          'want_free': false,
          'start_date': '',
          'end_date': ''
        };

        formData.old = this.vv.age.$model === "2";
        
        if (this.vv.vaccineType.$model != "Both") {
          formData.want_free = this.vv.vaccineType.$model === "Free";
        }

        if (this.vv.vaccineBrand.$model != 'Both') {
          formData.flavor = this.vv.vaccineBrand.$model.toLowerCase();
        }

        let startDate = new Date(),
            endDate = new Date();
            
        if (this.vv.period.$model != 0) {
            endDate.setDate(endDate.getDate() + Number(this.vv.period.$model) - 1);
        } else {
          endDate = null;
        }

        formData.start_date = this.dateToString(startDate);
        formData.end_date = this.dateToString(endDate);

        if (this.vv.mobileNumber.$model != "") {
          formData.mobile = Number(this.vv.mobileNumber.$model);
        }

        if (this.vv.emailAddress.$model != "") {
          formData.email = this.vv.emailAddress.$model;
        }

        api.postSubscription(formData).then((response) => {
          if (response.status == 200){
            this.handleToast('Request submitted successfully.');
            this.UUID = response.data.uuid;
            if ('email' in formData) {
              this.validateEmailID = true;
            }
          }
        })
        
    });
  },
  resetData()
  {
    this.validateMobileNumber = false;
    this.validateEmailID = false;
    this.vv.mobileNumber.$model = '';
    this.vv.emailAddress.$model = '';
    this.vv.pinCode.$model = '';
    this.vv.radius.$model = null;
    this.vv.age.$model = null;
    this.vv.vaccineBrand.$model = null;
    this.vv.vaccineType.$model = null;
    this.vv.period.$model = null;
    this.otpVerified = false;
  },
  sendOTPInfo() {
    let api = new APIService;
    let formData = {};
    if (this.userEmailOTP && this.userEmailOTP.length === 4) {
      formData.otp_email = this.userEmailOTP;
    }
    api.postOTP(formData, this.UUID).then((response) => {
      if (response.status == 200) {
        this.handleToast('OTP verified successfully');
        this.otpVerified = true;
        setTimeout(() => { this.presentConfirm(); }, 1000);
        //console.log(this.userMobileOTP, this.userEmailOTP);
        
      }
    });
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