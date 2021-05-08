<template>
  <ion-app>
    <left-menu :showMenu="true"/>
    <ion-router-outlet />
  </ion-app>
  <ion-menu-controller></ion-menu-controller>
</template>

<script>
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { defineComponent } from 'vue';
import LeftMenu from "./components/LeftMenu.vue";

export default defineComponent({
  name: 'App',
  components: {
    LeftMenu,
    IonApp,
    IonRouterOutlet
  }
});
</script>