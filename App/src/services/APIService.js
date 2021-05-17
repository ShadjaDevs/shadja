import axios from 'axios';

export default class APIService {
    constructor() {
        this.URL = "https://api.bookmyvaccine.app";
        this.baseAPIInstance = {
            baseURL: '',
            timeout: 60000, // time out of 1 minute
            headers: { 'Access-Control-Allow-Origin' : '*' }
        }
    }

    /**
     *
     * @param instance - axios instance to make the query
     * @param options - additional options for the query
     */
    getAPI(instance, options = {}){
        //Build the options into a query string
        //let qs = Object.keys(options).map(key => key + '=' + options[key]).join('&');
        return instance.get('', options).then(response => {
            const status = response.status;
            if(status === 200) {
                return response;
            } else {
                throw new Error('Please check your internet connection and try again.');
            }
        })
            .catch((error) => {
                alert(error);
            });
    }

    /**
     *
     * @param instance - axios instance to make the query
     * @param options - additional options for the query
     */
    putAPI(instance, options){
        //Build the options into a query string
        let qs = Object.keys(options).map(key => key + '=' + options[key]).join('&');
        return instance.put('?'+qs).then(response => {
            const status = response.status;
            if(status === 200) {
                return response;
            } else {
                throw new Error('Please check your internet connection and try again.');
            }
        })
            .catch((error) => {
                alert(error);
            });
    }

    /**
     *
     * @param instance - axios instance to make the query
     * @param options - additional options for the query
     */
    postAPI(instance, options){
        //Build the options into a query string
        //let qs = Object.keys(options).map(key => key + '=' + options[key]).join('&');
        //qs = 'projects' + qs;
        return instance.post('', options).then(response => {
            const status = response.status;
            if(status === 200) {
                return response;
            } else {
                throw new Error('Please check your internet connection and try again.');
            }
        })
            .catch((error) => {
                alert(error);
            });
    }

    fetchProjectsBySearchParameter(groupID, options = {}) {
        if (groupID === null) {
            return Promise.all([]);
        }
        options.show_pagination = true;
        options.per_page = 100;

        this.baseAPIInstance.baseURL = this.URL+'/api/v4/groups/'+groupID+'/projects';

        let instance = axios.create(this.baseAPIInstance);

        return this.getAPI(instance, options);
    }

    /**
     *
     * @param groupID
     * @param options
     * @returns {Promise<{Data from API}[] | never>}
     */
    fetchSubGroupsBySearchParameter(groupID, options = {}) {
        if (groupID === null) {
            return Promise.all([]);
        }
        options.show_pagination = true;
        options.per_page = 100;

        this.baseAPIInstance.baseURL = this.URL+'/api/v4/groups/'+groupID+'/subgroups';

        let instance = axios.create(this.baseAPIInstance);

        return this.getAPI(instance, options);
    }


    // triggerPipeline(formData, groupID) {
    //     if (!formData) {
    //         return Promise.all([]);
    //     }
    //     let projectCreationPipeline = getEnvironmentValue(this.URL, 'projectCreationPipeline');

    //     this.baseAPIInstance.baseURL = this.URL+'/api/v4/projects/'+groupID+'/trigger/pipeline';

    //     this.baseAPIInstance.data = {
    //         ref: projectCreationPipeline.ref,
    //         token: projectCreationPipeline.triggerToken
    //     }

    //     formData.set('ref', this.baseAPIInstance.data.ref);
    //     formData.set('token', this.baseAPIInstance.data.token);

    //     let instance = axios.create(this.baseAPIInstance);

    //     return this.postAPI(instance, formData);
    // }

    getPipelineDetails(pipelineID, groupID) {
        if (!pipelineID) {
            return Promise.all([]);
        }
        this.baseAPIInstance.baseURL = this.URL+'/api/v4/projects/'+groupID+'/pipelines/'+pipelineID;

        let instance = axios.create(this.baseAPIInstance);

        return this.getAPI(instance);
    }
    
    getProjectDetailsByNamespace(namespace) {
        this.baseAPIInstance.baseURL = `${this.URL}/api/v4/projects/${namespace}`

        let instance = axios.create(this.baseAPIInstance);

        return this.getAPI(instance)
    }

    getNearByPinCodes(pinCode, radius) {

        this.baseAPIInstance.baseURL = `${this.URL}/nearby_pincodes/${pinCode}/${radius}`;

        let instance = axios.create(this.baseAPIInstance);

        return this.getAPI(instance);

    }

    postSubscription(formData) {
        this.baseAPIInstance.baseURL = `${this.URL}/add_subscription`;

        let instance = axios.create(this.baseAPIInstance);

        return this.postAPI(instance, formData);
    }

    postOTP(formData, uuid) {
        this.baseAPIInstance.baseURL = `${this.URL}/input_otp/${uuid}`;

        let instance = axios.create(this.baseAPIInstance);

        return this.postAPI(instance, formData);
    }
}