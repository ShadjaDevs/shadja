import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

import { IonicVue } from '@ionic/vue';

/* Core CSS required for Ionic components to work properly */
import '@ionic/vue/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';

/* Theme variables */
import './theme/variables.css';
import { ApiService } from "@/services/api.service";
import {TokenService} from "@/services/token.service";
import { store } from "./store";
import GoogleMap from '@/components/GoogleMap.vue';

const app = createApp(App)
  .use(IonicVue)
  .use(GoogleMap)
  .use(router)
  .use(store);

const a = new ApiService(process.env.VUE_APP_ROOT_API);
const tokenService = new TokenService;

if (tokenService.getToken()) {
  a.setHeader();
  a.mountRequestInterceptor();
  a.mount401Interceptor();
}
  
router.isReady().then(() => {
  app.mount('#app');
});

