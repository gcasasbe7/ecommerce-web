import axios from 'axios'
import store from '../store'

class ApiData {
    // Base Api URL
    static BASE_API_URL = '/api/v1'
    // Valid response code
    static VALID_RESPONSE_CODE     = 200
}

export default {
    /**
     * Api Endpoint:    Get Category Detail
     * Api Url:         /api/v1/shop/${categorySlug}/
     * Required Params: ${categorySlug} 
     * @param {Object} callback      ~> Success and error scenarios
     * @param {String} categorySlug  ~> Current category to fetch
     */
    async getCategoryDetail(callback, categorySlug) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/shop/${categorySlug}/`
        // Launch the Api call
        this.performApiCall(url, callback)
    },

    /**
     * Root method to fire the api calls
     * @param {String} url      ~> Endpoint url to hit
     * @param {Object} callback ~> Success and error scenarios
     */
    async performApiCall(url, callback){
        // Assert the application is loading while the asynchronous call is executed
        store.commit('setIsApplicationLoading', true)

        // Perform the api call through Axios
        await axios
            .get(url)
            .then(response => {
                // todo remove
                callback.success(response)
                // Is the response valid?
                if(response.response_code === ApiData.VALID_RESPONSE_CODE){
                    // Execute the callback with success
                    callback.success(response)
                }
            })
            .catch(error => {
                // Execute the callback with errors
                callback.error(error)
            })
        
        // Assert the application has finished loading the asynchronous call
        store.commit('setIsApplicationLoading', false)
    }
}