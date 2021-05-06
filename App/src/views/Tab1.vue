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
          <ion-title class ="mainTitle"> Search By Zip Code </ion-title>
        </ion-col>
        </ion-row>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-row>
        <ion-col>
        <ion-searchbar 
        @ionInput="zipCodeEntry($event.target.value)" 
        placeholder="Pincode or locality"></ion-searchbar>
        </ion-col>
        </ion-row>
        <ion-row>
          <div id = "groupedButtons">
          <ion-col>
          <ion-button class = "but" id="0" @click="updateRadioOptions(0)" v-bind:color="radiusOptions[0].isActive ? 'primary' : 'secondary'" size="small">
            <ion-label>{{ radiusOptions[0].text }}</ion-label>
          </ion-button>
          </ion-col>  
          <ion-col>
          <ion-button class = "but" id="1" @click="updateRadioOptions(1)" v-bind:color="radiusOptions[1].isActive ? 'primary' : 'secondary'" size="small">
            <ion-label>{{ radiusOptions[1].text }}</ion-label>
          </ion-button>
          </ion-col> 
          <ion-col>
          <ion-button class = "but" id="2" @click="updateRadioOptions(2)" v-bind:color="radiusOptions[2].isActive ? 'primary' : 'secondary'" size="small">
            <ion-label>{{ radiusOptions[2].text }}</ion-label>
          </ion-button>
          </ion-col> 
          <ion-col>
          <ion-button class = "but" id="3" @click="updateRadioOptions(3)" v-bind:color="radiusOptions[3].isActive ? 'primary' : 'secondary'" size="small">
            <ion-label>{{ radiusOptions[3].text }}</ion-label>
          </ion-button>
          </ion-col> 
          <ion-col> 
          <ion-button class = "but" id="4" @click="updateRadioOptions(4)" v-bind:color="radiusOptions[4].isActive ? 'primary' : 'secondary'" size="small">
            <ion-label>{{ radiusOptions[4].text }}</ion-label>
          </ion-button>
          </ion-col> 
          <ion-col>
          <ion-button class = "but" id="5" @click="updateRadioOptions(5)" v-bind:color="radiusOptions[5].isActive ? 'primary' : 'secondary'" size="small">
            <ion-label>{{ radiusOptions[5].text }}</ion-label>
          </ion-button>
          </ion-col>    
          </div>     
        </ion-row>
          <ion-card>
            <ion-card-content>
              Matching zip codes found: {{ matchingZipCodes.length }} <br>
              Available slots: {{ availableSlots }}
            </ion-card-content>
          </ion-card>
          <gmap
          v-show="false"
            :disableUI="false"
            :zoom="12"
            mapType="roadmap"
            :center="{ lat: 38.8977859, lng: -77.0057621 }">
          </gmap>
          <google-map :init="initializeGoogleMap" :markers="markers" />
          <ion-card v-if = "availableSlots === 0">
            <ion-card-content>
              Looks like there are no slots available for your search parameters. Click on the bell icon below to sign up for updates.
            </ion-card-content>
          </ion-card>


    
      <!-- <ExploreContainer name="Tab 1 page" /> -->
    </ion-content>
  </ion-page>
</template>

<script>
import { IonPage, IonHeader, IonToolbar, IonContent, IonSearchbar, } from '@ionic/vue';
//import ExploreContainer from '@/components/ExploreContainer.vue';
import Gmap from '@/components/gmap.vue';
import { caretForwardCircle, menu, menuOutline } from 'ionicons/icons';
import { menuController } from "@ionic/vue";
import useDataService from '../services/data.service';
import GoogleMap from '@/components/GoogleMap.vue';
import { reactive } from 'vue'

export default  {
  name: 'Tab1',
  components: { IonHeader, IonToolbar, IonContent, IonPage, IonSearchbar, Gmap, GoogleMap },
  data() {
    return {
      matchingZipCodes: [],
      availableSlots: 0,
      radiusOptions: [
        { id: 0, text: '5km', value: 5, isActive: false},
        { id: 1, text: '10km', value: 10, isActive: false },
        { id: 2, text: '25km', value: 25, isActive: false },
        { id: 3, text: '50km', value: 50, isActive: false },
        { id: 4, text: '100km', value: 100, isActive: false },
        { id: 5, text: '500km', value: 500, isActive: false }
      ],
      clicked: false,
      activeColor: 'blue',
      mapMarkers: []
    }
  },
  setup() {
    const { zipCode, searchRadius } = useDataService();
    const markers = reactive([
      {
        lat: 48.8566,
        lng: 2.3522,
        content: { content: `Paris Capital of <b>France</b>` },
        icon:
          "data:image/svg+xml,%3Csvg width='14' height='20' viewBox='0 0 14 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 9.5C6.33696 9.5 5.70107 9.23661 5.23223 8.76777C4.76339 8.29893 4.5 7.66304 4.5 7C4.5 6.33696 4.76339 5.70107 5.23223 5.23223C5.70107 4.76339 6.33696 4.5 7 4.5C7.66304 4.5 8.29893 4.76339 8.76777 5.23223C9.23661 5.70107 9.5 6.33696 9.5 7C9.5 7.3283 9.43534 7.65339 9.3097 7.95671C9.18406 8.26002 8.99991 8.53562 8.76777 8.76777C8.53562 8.99991 8.26002 9.18406 7.95671 9.3097C7.65339 9.43534 7.3283 9.5 7 9.5ZM7 0C5.14348 0 3.36301 0.737498 2.05025 2.05025C0.737498 3.36301 0 5.14348 0 7C0 12.25 7 20 7 20C7 20 14 12.25 14 7C14 5.14348 13.2625 3.36301 11.9497 2.05025C10.637 0.737498 8.85652 0 7 0Z' fill='%234FB8FF'/%3E%3C/svg%3E",
      },
      {
        lat: 51.5074,
        lng: 0.1278,
        content: { content: `London Capital of <b>England</b>` },
        icon:
          "https://developers.google.com/maps/documentation/javascript/examples/full/images/info-i_maps.png",
      },
      {
        lat: 41.9028,
        lng: 12.4964,
        content: { content: `Roma Capital of <b>Italy</b>` },
      },
      {
        lat: 41.9028,
        lng: 12.4964,
        content: { content: `Roma Capital of <b>Italy</b>` },
      },
      {
        lat: 40.4168,
        lng: 3.7038,
        content: { content: `Madrid Capital of <b>Spain</b>` },
      },
      {
        lat: 39.9334,
        lng: 32.8597,
        content: { content: `Ankara Capital of <b>Turkey</b>` },
      },
    ]);
    const initializeGoogleMap = {
      streetViewControl: true,
      scaleControl: true,
      center: { lat: 34.04924594193164, lng: 34.04924594193164 },
      zoom: 2,
    };
    const markerIcons = {
      covaxin: {
        free:"data:image/svg+xml,%3Csvg width='14' height='20' viewBox='0 0 14 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 4.5C7.66304 4.5 8.29893 4.76339 8.76777 5.23223C9.23661 5.70107 9.5 6.33696 9.5 7C9.5 7.3283 9.43534 7.65339 9.3097 7.95671C9.18406 8.26002 8.99991 8.53562 8.76777 8.76777C8.53562 8.99991 8.26002 9.18406 7.95671 9.3097C7.65339 9.43534 7.3283 9.5 7 9.5C6.33696 9.5 5.70107 9.23661 5.23223 8.76777C4.76339 8.29893 4.5 7.66304 4.5 7C4.5 6.33696 4.76339 5.70107 5.23223 5.23223C5.70107 4.76339 6.33696 4.5 7 4.5ZM7 0C8.85652 0 10.637 0.737498 11.9497 2.05025C13.2625 3.36301 14 5.14348 14 7C14 12.25 7 20 7 20C7 20 0 12.25 0 7C0 5.14348 0.737498 3.36301 2.05025 2.05025C3.36301 0.737498 5.14348 0 7 0ZM7 2C5.67392 2 4.40215 2.52678 3.46447 3.46447C2.52678 4.40215 2 5.67392 2 7C2 8 2 10 7 16.71C12 10 12 8 12 7C12 5.67392 11.4732 4.40215 10.5355 3.46447C9.59785 2.52678 8.32608 2 7 2Z' fill='%234FB8FF'/%3E%3C/svg%3E%0A",
        paid:"data:image/svg+xml,%3Csvg width='14' height='20' viewBox='0 0 14 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 9.5C6.33696 9.5 5.70107 9.23661 5.23223 8.76777C4.76339 8.29893 4.5 7.66304 4.5 7C4.5 6.33696 4.76339 5.70107 5.23223 5.23223C5.70107 4.76339 6.33696 4.5 7 4.5C7.66304 4.5 8.29893 4.76339 8.76777 5.23223C9.23661 5.70107 9.5 6.33696 9.5 7C9.5 7.3283 9.43534 7.65339 9.3097 7.95671C9.18406 8.26002 8.99991 8.53562 8.76777 8.76777C8.53562 8.99991 8.26002 9.18406 7.95671 9.3097C7.65339 9.43534 7.3283 9.5 7 9.5ZM7 0C5.14348 0 3.36301 0.737498 2.05025 2.05025C0.737498 3.36301 0 5.14348 0 7C0 12.25 7 20 7 20C7 20 14 12.25 14 7C14 5.14348 13.2625 3.36301 11.9497 2.05025C10.637 0.737498 8.85652 0 7 0Z' fill='%234FB8FF'/%3E%3C/svg%3E%0A"
      },
      covishield: {
        free:"data:image/svg+xml,%3Csvg width='14' height='20' viewBox='0 0 14 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 4.5C7.66304 4.5 8.29893 4.76339 8.76777 5.23223C9.23661 5.70107 9.5 6.33696 9.5 7C9.5 7.3283 9.43534 7.65339 9.3097 7.95671C9.18406 8.26002 8.99991 8.53562 8.76777 8.76777C8.53562 8.99991 8.26002 9.18406 7.95671 9.3097C7.65339 9.43534 7.3283 9.5 7 9.5C6.33696 9.5 5.70107 9.23661 5.23223 8.76777C4.76339 8.29893 4.5 7.66304 4.5 7C4.5 6.33696 4.76339 5.70107 5.23223 5.23223C5.70107 4.76339 6.33696 4.5 7 4.5ZM7 0C8.85652 0 10.637 0.737498 11.9497 2.05025C13.2625 3.36301 14 5.14348 14 7C14 12.25 7 20 7 20C7 20 0 12.25 0 7C0 5.14348 0.737498 3.36301 2.05025 2.05025C3.36301 0.737498 5.14348 0 7 0ZM7 2C5.67392 2 4.40215 2.52678 3.46447 3.46447C2.52678 4.40215 2 5.67392 2 7C2 8 2 10 7 16.71C12 10 12 8 12 7C12 5.67392 11.4732 4.40215 10.5355 3.46447C9.59785 2.52678 8.32608 2 7 2Z' fill='%232ECC71'/%3E%3C/svg%3E%0A",
        paid:"data:image/svg+xml,%3Csvg width='14' height='20' viewBox='0 0 14 20' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M7 9.5C6.33696 9.5 5.70107 9.23661 5.23223 8.76777C4.76339 8.29893 4.5 7.66304 4.5 7C4.5 6.33696 4.76339 5.70107 5.23223 5.23223C5.70107 4.76339 6.33696 4.5 7 4.5C7.66304 4.5 8.29893 4.76339 8.76777 5.23223C9.23661 5.70107 9.5 6.33696 9.5 7C9.5 7.3283 9.43534 7.65339 9.3097 7.95671C9.18406 8.26002 8.99991 8.53562 8.76777 8.76777C8.53562 8.99991 8.26002 9.18406 7.95671 9.3097C7.65339 9.43534 7.3283 9.5 7 9.5ZM7 0C5.14348 0 3.36301 0.737498 2.05025 2.05025C0.737498 3.36301 0 5.14348 0 7C0 12.25 7 20 7 20C7 20 14 12.25 14 7C14 5.14348 13.2625 3.36301 11.9497 2.05025C10.637 0.737498 8.85652 0 7 0Z' fill='%232ECC71'/%3E%3C/svg%3E%0A"
      }
    }
    return {
      caretForwardCircle,
      menu,
      zipCode,
      searchRadius,
      initializeGoogleMap,
      markers,
      menuOutline,
      markerIcons
    }
  },
methods: {
  zipCodeEntry(value) {
    console.log(value, this);
    this.zipCode = value;
  },
  searchRadiusEntry(event) {
    console.log(event.details.value);
  },
  initiateSeach() {
    let a = document.querySelector('#searchRadius');
    console.log(a);
    console.log("ZipCode: " + this.zipCode + "searchRadius:" + this.searchRadius );
  },
  openStart() {
      menuController.open("mainMenu");
    },
    updateRadioOptions(id) {
      for (let i=0; i <6; i ++) {
        if (i==id) {
          this.radiusOptions[i].isActive = true;
          this.searchRadius = this.radiusOptions[i].value;
        } else {
          this.radiusOptions[i].isActive = false;
        }
      }
    },
    emitMetaData() {
      let toEmit = { zipCode: this.zipCode, searchRadius: this.searchRadius};
      this.$emit('emittingMetaData', toEmit);
    },
    fetchAppointmentDetails() {
        this.setUpMarkers([]);
        //To do set availableSlots
    },
    setUpMarkers(data) {
      for (let i = 0; i < data.length; i++) {
          let tempMarker = {};
          tempMarker.lat = data[i].lat;
          tempMarker.long = data[i].long;
          tempMarker.content = data[i].content;
          if (data[i].covaxin) {
            tempMarker = data[i].free ? this.markerIcons.covaxin.free : this.markerIcons.covaxin.paid;
          } else {
            tempMarker = data[i].free ? this.markerIcons.covishield.free : this.markerIcons.covishield.paid;
          }
      }
    }
    
},
watch: {
  zipCode() {
      if (this.zipCode.length == 6) {
        this.fetchAppointmentDetails();
      }
    },
    searchRadius() {
      this.fetchAppointmentDetails();
    }
},
};
</script>

<style scoped>
.but{
  margin: 0 auto;
  display: inline-block;
  width: 50px;
}
#groupedButtons {
  margin-left: auto;
  margin-right: auto;
}
.mainTitle {
  margin-left: 5px;
  padding-top: 10px;
}
</style>