<template>
  <ion-page>
    <ion-tabs>
      <ion-tab-bar slot="bottom">
        <ion-tab-button v-show="showItem" tab="tab1" href="/tabs/tab1">
          <ion-icon :icon="location" />
          <ion-label>Search by ZIP code</ion-label>
        </ion-tab-button>
          
        <ion-tab-button tab="tab2" href="/tabs/tab2">
          <ion-icon :icon="notifications" />
          <ion-label>Sign up for updates</ion-label>
        </ion-tab-button>
        
        <ion-tab-button v-show="showItem" tab="tab3" href="/tabs/tab3">
          <ion-icon :icon="megaphone"/>
          <ion-label>My Subscriptions</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script>
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage } from '@ionic/vue';
import { ellipse, square, triangle, location, notifications, megaphone } from 'ionicons/icons';

export default {
  name: 'Tabs',
  components: { IonLabel, IonTabs, IonTabBar, IonTabButton, IonIcon, IonPage },
  setup() {
    const showItem = false;
    return {
      ellipse, 
      square, 
      triangle,
      location,
      notifications,
      megaphone,
      showItem
    }
  }
}
</script>