/**
 * Helper file to manage the front end data storage.
 * Provides friendly methods to store and retrieve data from the multiple store points of the front end application.
 * Storage points provided: Browser Local Storage & Browser Cookies
 */

class StorageHelper {
    ACCESS_TOKEN_KEY    = "$tk_access"
    REFRESH_TOKEN_KEY   = "$tk_refresh"
    USER_KEY            = "$usr"
    
    /**
     * Returns a cookie value given it's key
     * @param {Cookie key} key 
     * @returns Value for the given key, undefined if not defined
     */
    getCookie(key) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${key}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    /**
     * Sets a a new cookie key-value pair to the document
     * @param {Cookie key} key 
     * @param {Cookie value} value 
     */
    setCookie(key, value) {document.cookie = `${key}=${value}`}

    /**
     * Fetches the value of a locally stored key-value pair in the Local Storage
     * @param {Locally stored item key} key 
     * @returns String value for that given key or null if not defined
     */
    getLocalValue(key) {return localStorage.getItem(key)}

    /**
     * Stores a new key-value pair into the Local Storage
     * @param {Storing key} key 
     * @param {Storing value} value 
     */
    setLocalValue(key, value) {localStorage.setItem(key, value)}

    storeUser(data) {
        localStorage.setItem(this.USER_KEY, JSON.stringify(data))
    }

    removeUser() {
        localStorage.removeItem(this.USER_KEY)
    }

    getUser() {
        return JSON.parse(localStorage.getItem(this.USER_KEY))
    }
}

export default new StorageHelper()