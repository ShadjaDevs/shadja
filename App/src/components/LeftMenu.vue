<template>
  <ion-menu menu-id="mainMenu" class="mainMenu" content-id="mainMenu" :auto-hide="false" :disabled="false">
    <ion-header>
      <ion-toolbar color="primary">
        <ion-title>Menu</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-list>
        <ion-list-header>
          Navigate
        </ion-list-header>
        <ion-menu-toggle auto-hide="false">
          <ion-item button @click="$router.replace('/login')">
            <ion-icon
              slot="start"
              name='home'
            ></ion-icon>
            <ion-label>
              Login
            </ion-label>
          </ion-item>
          <ion-item button @click="$router.replace('/tabs/tab1')">
            <ion-icon
              slot="start"
              name='home'
            ></ion-icon>
            <ion-label>
              Home
            </ion-label>
          </ion-item>

          <ion-item button @click="$router.replace('/about')">
            <ion-icon
              slot="start"
              name='home'
            ></ion-icon>
            <ion-label>
              About
            </ion-label>
          </ion-item>
        </ion-menu-toggle>
      </ion-list>
    </ion-content>
  </ion-menu>
  <ion-router-outlet id="mainMenu"></ion-router-outlet>

</template>

<script>
  export default {
    name: "LeftMenu",
    props: {
      showMenu: Boolean
    },
    data() {
        return {
          hideMenu: true
        }
    }
  };
</script>