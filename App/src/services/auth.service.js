import { ApiService } from "./api.service";
import { TokenService } from "./token.service";
//import { AxiosRequestConfig } from "axios";
import qs from "qs";

class AuthenticationError extends Error {
    constructor(errorCode, message) {
        super(message);
        this.name = this.constructor.name;
        if (message != null) {
            this.message = message;
        }
        this.errorCode = errorCode;
    }
}

class AuthService{
    async signIn(signInData) {
        const requestData = {
            method: "post",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Authorization: 'Basic ' + btoa(process.env.VUE_APP_CLIENT_ID + ':' + process.env.VUE_APP_CLIENT_SECRET)
            },
            url: "/oauth/token",
            data: qs.stringify({
                "grant_type": "password",
                username: signInData.username,
                password: signInData.password
            })
        };

        try {
            const response = await ApiService.customRequest(requestData);
            TokenService.saveToken(response.data.access_token);
            TokenService.saveRefreshToken(response.data.refresh_token);
            ApiService.setHeader();

            ApiService.mount401Interceptor();

            return response.data;
        } catch (error) {
            this.catchError(error);
        }
    }

    async refreshToken() {
        const refreshToken = TokenService.getRefreshToken();

        const requestData = {
            method: "post",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Authorization: 'Basic ' + btoa(process.env.VUE_APP_CLIENT_ID + ':' + process.env.VUE_APP_CLIENT_SECRET)
            },
            url: "/oauth/token",
            data: qs.stringify({
                "grant_type": "refresh_token",
                refreshToken: refreshToken
            })
        };

        try {
            const response = await ApiService.customRequest(requestData);

            TokenService.saveToken(response.data.access_token);
            TokenService.saveRefreshToken(response.data.refresh_token);
            ApiService.setHeader();

            return response.data.access_token;
        } catch (error) {
            throw new AuthenticationError(
                error.response.status,
                error.response.data.error_description
            );
        }
    }

    signOut() {
        TokenService.removeToken();
        TokenService.removeRefreshToken();
        ApiService.removeHeader();
        ApiService.unmount401Interceptor();
    }

    async signup(email, password, name) {
        const signupData = {
            method: "post",
            headers: { "Content-Type": "application/json" },
            url: "/oauth/signup",
            data: {
                email: email,
                password: password,
                name: name
            }
        };

        try {
            return await ApiService.customRequest(signupData);
        } catch (error) {
            this.catchError(error);
        }
    }

    catchError(error) {
        let status;
        let description;

        if (error.response === undefined) {
            status = error.message;
            description = error.message;
        } else {
            status = error.response.status;
            description = error.response.data.error_description;
        }

        throw new AuthenticationError(status, description);
    }
}

export { AuthService, AuthenticationError };