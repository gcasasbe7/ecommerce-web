<template>
<div class="identify-page">
    <div class="container">
        <div class="row">
            <div class="column" style="padding: 0px 80px 0px 80px">
                <LogIn @submit_form="complete_login" :errors="this.login_errors" />
            </div>
            <div class="column" style="padding: 0px 80px 0px 80px">
                <SignUp @submit_form="complete_signup" :errors="this.signup_errors" />
            </div>
        </div>
    </div>
</div>
</template>

<script>
import ApiHelper from '@/helpers/api_helper.js'
import SignIn from '@/components/identify/LogIn.vue'
import SignUp from '@/components/identify/SignUp.vue'

export default {
    name: 'Identify',
    components: [
        SignIn, SignUp
    ],
    mounted() {
        document.title = "Identify | iPadel"
    },
    data() {
        return {
            login_errors: [],
            signup_errors: []
        }
    },
    methods: {
        async complete_login(login_data) {
            // Reset the login errors
            this.login_errors = []

            // Declare the callbacks
            const callback = {
                success: (response) => {
                    // Fetch the user data and update the store
                    let data = response.data.result
                    // Update the store
                    this.$store.commit('onLoginUser', data)
                },
                error: (error) => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.login_errors.push(error.response.data[property])
                        }
                    } else if (error.message) {
                        this.login_errors.push(`Something went wrong, please try again later (${error.message})`)
                    }
                }
            }

            // Attempt to identify to the backend
            ApiHelper.login(callback, login_data)
        },

        async complete_signup(signup_data) {
            // Reset the signup errors
            this.signup_errors = []

            // Declare the callbacks
            const callback = {
                success: (response) => {
                    console.log(response)
                    // Redirect
                },
                error: (error) => {
                    console.log(error)
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.signup_errors.push(error.response.data[property])
                        }
                    } else if (error.message) {
                        this.signup_errors.push(`Something went wrong, please try again later (${error.message})`)
                    }
                }
            }

            // Attempt to identify to the backend
            ApiHelper.register(callback, signup_data)
        }
    }
}
</script>

<style scoped>
* {
    box-sizing: border-box;
}

/* Create two equal columns that floats next to each other */
.column {
    float: left;
    width: 50%;
    padding: 10px;
    height: 300px;
    /* Should be removed. Only for demonstration */
}

/* Clear floats after the columns */
.row:after {
    content: "";
    display: table;
    clear: both;
}

.red {
    color: red
}
</style>
