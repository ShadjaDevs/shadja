<template>
  <div class="map" ref="mapDivRef"></div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "GMap",
  props: {
    center: { lat: Number, lng: Number },
    zoom: Number,
    mapType: String,
    disableUI: Boolean
  },
  setup(props) {
    // the google map object 
    const map = ref(null);

    // the map element in the templste
    const mapDivRef = ref(null);

    // load in the google script
    onMounted(() => {
      const key = "AIzaSyA7cFjyiTHtqmZC2RBGW-hYYSrjNHWLjaE";

      // create the script element to load
      const googleMapScript = document.createElement("SCRIPT");
      googleMapScript.setAttribute(
        "src",
        `https://maps.googleapis.com/maps/api/js?key=${key}&callback=initMap`
      );
      googleMapScript.setAttribute("defer", "");
      googleMapScript.setAttribute("async", "");
      document.head.appendChild(googleMapScript);
    });

    /**
     * this function is called as soon as the map is initialized
     */
    window.initMap = () => {
      map.value = new window.google.maps.Map(mapDivRef.value, {
        mapTypeId: props.mapType || "hybrid",
        zoom: props.zoom || 8,
        disableDefaultUI: props.disableUI || false,
        center: props.center || { lat: 38.0, lng: -77.01 }
      });
    };

    return {
      mapDivRef
    };
  }
};
</script>

<style lang="css" scoped>
.map {
  width: 100%;
  height: 300px;
  background-color: azure;
}
</style>