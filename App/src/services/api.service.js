import axios from "axios";
import {store} from '@/store';
//import {TokenService} from "@/services/token.service";
import {loadingController} from '@ionic/vue';

class ApiService {
    constructor(baseURL) {
        axios.defaults.baseURL = baseURL;
        this._requestInterceptor = 0;
        this._401interceptor = 0;
        //this.tokenService = new TokenService;
    }
    // setHeader() {
    //     axios.defaults.headers.common[
    //         "Authorization"
    //         ] = `Bearer ${this.tokenService.getToken()}`;
    // }
    // removeHeader() {
    //     axios.defaults.headers.common = {};
    // }
    get(resource) {
        return axios.get(resource);
    }

    post(resource, data) {
        return axios.post(resource, data);
    }

    put(resource, data) {
        return axios.put(resource, data);
    }

    delete(resource) {
        return axios.delete(resource);
    }

    customRequest(data) {
        return axios(data);
    }

    mountRequestInterceptor() {
        this._requestInterceptor = axios.interceptors.request.use(async config => {
            console.log("show loading");
            const loading = await loadingController.create({
                message: 'Please wait...'
            });
            await loading.present();

            return config;
        });
    }

    mount401Interceptor() {
        this._401interceptor = axios.interceptors.response.use(
            response => {
                loadingController.dismiss().then(r => console.log(r));
                return response;
            },
            async error => {
                loadingController.dismiss().then(r => console.log(r));
                if (error.request.status === 401) {
                    if (error.config.url.includes("oauth/token")) {
                        await store.dispatch("auth/signOut");
                        throw error;
                    } else {
                        try {
                            await store.dispatch("auth/refreshToken");
                            return this.customRequest({
                                method: error.config.method,
                                url: error.config.url,
                                data: error.config.data
                            });
                        } catch (e) {
                            throw error;
                        }
                    }
                }
                throw error;
            }
        );
    }

    unmount401Interceptor() {
        axios.interceptors.response.eject(this._401interceptor);
    }
}

export { ApiService };

