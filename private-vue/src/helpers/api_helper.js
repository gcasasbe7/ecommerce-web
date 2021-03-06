import axios from 'axios'
import store from '../store'
import storageHelper from './storage_helper'

class ApiData {
    // Base Api URL
    static BASE_API_URL = '/api/v1'
    // Valid response code
    static VALID_RESPONSE_CODE = 200
    // Failed Authentication response code
    static AUTHENTICATION_ERROR_CODE = 401
    // Define the timeout for the API calls
    static API_CALL_TIMEOUT = 8000
    // Successful Api Call Fallback
    static positive(callback, response) {
        // Decapsulate the response data
        response = response.data
        // Is the response valid?
        if (response.status === ApiData.VALID_RESPONSE_CODE) {
            // Execute the callback with success
            callback.success(response)
        } else {
            // Fallback to the error scenario for non expected status
            callback.error(response.message)
        }
    }
    // Invalid Api Call Fallback
    static negative(callback, error) {
        if (error.response.status === ApiData.AUTHENTICATION_ERROR_CODE) {
            console.log("Detected unauthentication error. Calling unauth")
            callback.unauth()
        } else {
            // Fallback to the error scenario
            callback.error(error)
        }
    }
    // Authentification header definition
    static getAuthHeader() {
        // Fetch the current user
        let user = storageHelper.getUser()
        // Ensure the auth header can be built correctly
        if (user && user.tokens.access_token) {
            return { Authorization: 'Bearer ' + user.tokens.access_token }
        } else {
            return {}
        }
    }
}

export default {
    /**
     * Api Endpoint:    Login
     * Method:          POST
     * Api Url:         /api/v1/login/
     * Required Params: [Post request params: {'email' : "value", 'password' : "value"}]
     * @param {Object} callback     ~> Success and error scenarios
     * @param {String} login_data   ~> User login credentials
     */
    async login(callback, login_data) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/login/`
        // Launch the Api call providing callback actions
        this.performApiPostCall(url, callback, login_data)
    },


    /**
     * Api Endpoint:    Register
     * Method:          POST
     * Api Url:         /api/v1/register/
     * Required Params: [Post request params: {'name' : "value",'surname' : "value",'email' : "value", 'password' : "value"}]
     * @param {Object} callback      ~> Success and error scenarios
     * @param {String} signup_data   ~> User registration credentials
     */
    async register(callback, signup_data) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/register/`
        // Launch the Api call providing callback actions
        this.performApiPostCall(url, callback, signup_data)
    },


    /**
     * Api Endpoint:    Get Category Detail
     * Method:          GET
     * Api Url:         /api/v1/shop/${categorySlug}/
     * Required Params: [${categorySlug}]
     * @param {Object} callback      ~> Success and error scenarios
     * @param {String} categorySlug  ~> Current category to fetch
     */
    async getCategoryDetail(callback, categorySlug) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/shop/${categorySlug}/`
        // Launch the Api call providing callback actions
        this.performApiGetCall(url, callback)
    },


    /**
     * Api Endpoint:    Get Categories
     * Method:          GET
     * Api Url:         /api/v1/categories
     * Required Params: []
     * @param {Object} callback ~> Success and error scenarios
     */
    async getCategories(callback) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/categories/`
        // Launch the Api call providing callback actions
        this.performApiGetCall(url, callback)
    },


    /**
     * Api Endpoint:    Get Product Detail
     * Method:          GET
     * Api Url:         /api/v1/shop/${categorySlug}/${productSlug}/
     * Required Params: [${categorySlug}, ${productSlug}]
     * @param {Object} callback      ~> Success and error scenarios
     * @param {String} categorySlug  ~> Current category to fetch
     * @param {String} productSlug   ~> Current product to fetch
     */
    async getProductDetail(callback, categorySlug, productSlug) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/shop/${categorySlug}/${productSlug}/`
        // Launch the Api call providing callback actions
        this.performApiGetCall(url, callback)
    },


    /**
     * Api Endpoint:    Check Reset Password Link
     * Method:          GET
     * Api Url:         /api/v1/check-reset-password/${uidb64}/${token}
     * Required Params: [${uidb64}, ${token}]
     * @param {Object} callback ~> Success and error scenarios
     * @param {String} uidb64   ~> User Id 64 Base Encoded
     * @param {String} token    ~> User Password Reset Token
     */
    async checkResetPasswordToken(callback, uidb64, token) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/check-reset-password/${uidb64}/${token}/`
        // Launch the Api call providing callback actions
        this.performApiGetCall(url, callback)
    },


    /**
     * Api Endpoint:    Search products
     * Method:          POST
     * Api Url:         /api/v1/products/search/
     * Required Params: [Post request params: {'query' : "value"}]
     * @param {Object} callback ~> Success and error scenarios
     * @param {Object} query    ~> Search query
     */
    async performSearch(callback, query) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/products/search/`
        // Launch the Api call providing callback actions
        this.performApiPostCall(url, callback, query)
    },


    /**
     * Api Endpoint:    Set new password
     * Method:          PATCH
     * Api Url:         /api/v1/complete-reset-password/
     * Required Params: [Patch request params: {'uidb64' : "value", "token": "value", "password": "value"}]
     * @param {Object} callback ~> Success and error scenarios
     * @param {Object} data     ~> Set new password required data
     */
    async setNewPassword(callback, data) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/complete-reset-password/`
        // Launch the Api call providing callback actions
        this.performApiPatchCall(url, callback, data)
    },


    /**
     * Api Endpoint:    Checkout
     * Method:          POST
     * Api Url:         /api/v1/checkout/
     * Required Params: [Post request params: {'user_data' : {"token": "value"},
     *                                         'basket' : {basket_content & basket_creation_date}}]
     * @param {Object} callback ~> Success and error scenarios
     * @param {Object} data     ~> Checkout data
     */
    async checkout(callback, data) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/checkout/`
        // Launch the Api call providing callback actions
        this.performApiPostCall(url, callback, data)
    },


    /**
     * Api Endpoint:    Refresh token
     * Method:          POST
     * Api Url:         /api/v1/token/refresh/
     * Required Params: [Post request params: {'refresh' : "value"}
     * @param {Object} data     ~> User refresh token
     */
    async refreshToken(action) {
        // Define the data structure
        let data = { "refresh": store.state.user.tokens.refresh_token }
            // Declare the url
        const url = `${ApiData.BASE_API_URL}/token/refresh/`
            // Define the Api call
        await axios
            .post(url, data, { headers: ApiData.getAuthHeader() }, { timeout: ApiData.API_CALL_TIMEOUT })
            .then(response => {
                // Update the user token
                store.commit('setUserAccessToken', response.data.access)
                // Re attempt the previous action
                action.do()
            })
            .catch(error => {
                // Is the token invalid?
                if (error.code === "token_not_valid") {
                    // None of the user tokens could be validated. Log out
                    store.commit('onLogoutUser')
                }
            })
    },

    /**
     * Api Endpoint:    Verify Email
     * Method:          GET
     * Api Url:         /api/v1/verify-email/?token={value}
     * @param {Object} callback ~> Success and error scenarios
     */
     async verifyEmail(callback, token) {
        // Declare the url
        const url = `${ApiData.BASE_API_URL}/verify-email/?token=${token}`
        // Launch the Api call providing callback actions
        this.performApiGetCall(url, callback)
    },




    /**
     * Root method to fire the GET api calls
     * @param {String} url      ~> Endpoint url to hit
     * @param {Object} callback ~> Success and error scenarios
     */
    async performApiGetCall(url, callback) {
        // Assert the application is loading while the asynchronous call is executed
        store.commit('setIsApplicationLoading', true)

        // Perform the api call through Axios
        await axios
            .get(url, { headers: ApiData.getAuthHeader() }, { timeout: ApiData.API_CALL_TIMEOUT })
            .then(response => {
                // Execute the success callback
                ApiData.positive(callback, response)
            })
            .catch(error => {
                // Execute the callback with errors
                ApiData.negative(callback, error)
            })

        // Assert the application has finished loading the asynchronous call
        store.commit('setIsApplicationLoading', false)
    },


    /**
     * Root method to fire the POST api calls
     * @param {String} url          ~> Endpoint url to hit
     * @param {Object} callback     ~> Success and error scenarios
     * @param {Object} post_params  ~> POST parameters
     */
    async performApiPostCall(url, callback, post_params) {
        // Assert the application is loading while the asynchronous call is executed
        store.commit('setIsApplicationLoading', true)

        // Perform the api call through Axios
        await axios
            .post(url, post_params, { headers: ApiData.getAuthHeader() }, { timeout: ApiData.API_CALL_TIMEOUT })
            .then(response => {
                // Execute the success callback
                ApiData.positive(callback, response)
            })
            .catch(error => {
                // Execute the callback with errors
                ApiData.negative(callback, error)
            })

        // Assert the application has finished loading the asynchronous call
        store.commit('setIsApplicationLoading', false)
    },


    /**
     * Root method to fire the PATCH api calls
     * @param {String} url          ~> Endpoint url to hit
     * @param {Object} callback     ~> Success and error scenarios
     * @param {Object} patch_params  ~> PATCH parameters
     */
    async performApiPatchCall(url, callback, patch_params) {
        // Assert the application is loading while the asynchronous call is executed
        store.commit('setIsApplicationLoading', true)

        // Perform the api call through Axios
        await axios
            .patch(url, patch_params, { headers: ApiData.getAuthHeader() }, { timeout: ApiData.API_CALL_TIMEOUT })
            .then(response => {
                // Execute the success callback
                ApiData.positive(callback, response)
            })
            .catch(error => {
                // Execute the callback with errors
                ApiData.negative(callback, error)
            })

        // Assert the application has finished loading the asynchronous call
        store.commit('setIsApplicationLoading', false)
    },
}