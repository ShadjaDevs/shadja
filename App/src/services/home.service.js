import { ApiService } from "./api.service";

class ResponseError extends Error {
    constructor(errorCode, message) {
        super(message);
        this.name = this.constructor.name;
        if (message != null) {
            this.message = message;
        }
        this.errorCode = errorCode;
    }
}

class HomeService {
async secretArea() {
        try {
            return ApiService.get("/secret");
        } catch (error) {
            throw new ResponseError(
                error.status,
                error.error.message
            );
        }
    }
}

export { HomeService, ResponseError };