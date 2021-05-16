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
          <ion-title class = "mainTitle"> My Subscriptions </ion-title>
        </ion-col>
        </ion-row>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <div v-if='!isAuthenticated'>
        <div v-for="(sub, index) in subscriptions" :key="sub">
        <ion-card>
            <ion-item>
            <ion-button @click="presentConfirm(index)" class = "floatingRight" slot="end">
              <ion-icon :icon="trash"/>
            </ion-button>
            <ion-card-content>
              Mode of contact: {{sub.modeOfContact}} <br>
              ZipCode: {{sub.zipCode}} <br>
              Date subscribed: {{ sub.dateSubscribed }} <br>
              Period: {{sub.period}}
            </ion-card-content>
            </ion-item>
        </ion-card>	
      </div>
      </div>
      <login v-else id="login" emitMetaData="recieveMetaData($event)"></login>
      <ion-alert-controller></ion-alert-controller>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonItem,
  IonButton,
  IonCard,
  toastController,
  alertController } from '@ionic/vue';
//import ExploreContainer from '@/components/ExploreContainer.vue';
import { menuOutline, trash  } from 'ionicons/icons';
import { menuController } from "@ionic/vue";
import { mapState } from 'vuex';
import Login from './login.vue';


export default  {
  name: 'Tab2',
  components: { IonHeader, IonToolbar, IonTitle, IonContent, IonPage, Login,
  IonItem,
  IonButton,
  IonCard },
  data() {
    return {
      model: '',
      subscriptionPeriod: 0,
      tempVV: {},
      userMobileOTP : '',
      userEmailOTP: '',
      validateMobileNumber: false,
      validateEmailID: false,
      subToEdit: [],
      subscriptions : [
      { modeOfContact: "1111111111", zipCode: "560097", period: "Till I cancel", dateSubscribed: "05/06/2021" },
      { modeOfContact: "1111111111", zipCode: "560096", period: "Till I cancel", dateSubscribed: "05/06/2021" },
      { modeOfContact: "1111111111", zipCode: "560095", period: "Till I cancel", dateSubscribed: "05/06/2021" },
      { modeOfContact: "1111111111", zipCode: "560094", period: "Till I cancel", dateSubscribed: "05/06/2021" }
    ]
    }
  },
  setup() {
    return {
      menuOutline, trash
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
        position: 'bottom',
        message: 'Subscription deleted'
      });

      await toast.present();
    },
  openStart() {
      menuController.open("mainMenu");
      //let a = document.querySelector('#startDate');
      console.log(this.startDate);
      console.log(this.zipCode, this.searchRadius);
      this.formatDate(this.subscriptions);
    },
  async deleteSub(index) {
      console.log(this.subscriptions, this.subToEdit);
      this.subToEdit.push(this.subscriptions[index]);
      this.subscriptions.splice(index, 1);
      console.log(this.subscriptions, this.subToEdit);
      this.handleToast();
  },
  async presentConfirm(index) {
    const alert = await alertController
        .create({
          cssClass: 'my-custom-class',
          header: 'ALERT',
          message: 'Are you sure you want to delete this?',
          buttons: [
            {
              text: 'Cancel',
              role: 'cancel',
              handler: () => {
                console.log('Cancel clicked');
              }
            },
            {
              text: 'Yes',
              handler: () => {
                this.deleteSub(index);
              }
            }
        ]
        });
      return alert.present();
  },
  formatDate(subscriptions) {
    subscriptions.forEach((sub) => {
        let subDate = new Date(sub.dateSubscribed);
        let dd = String(subDate.getDate()).padStart(2, '0');
        let mm = String(subDate.getMonth() + 1).padStart(2, '0'); //January is 0!
        let yyyy = subDate.getFullYear();

        sub.dateSubscribed = dd + '/' + mm + '/' + yyyy;
    });
  }
},
}
</script>
<style scoped>
.floatingRight {
  top:5px;
  right:5px;
  position: absolute;
}
.mainTitle {
  margin-left: 5px;
  padding-top: 10px;
}
</style>