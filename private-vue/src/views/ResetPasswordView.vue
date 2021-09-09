<template>
<div class="reset-password">
    <h1>Introduce your new password</h1>
    <div class="row" v-if="this.success">
        <div class="column">
            <ResetPassword @submit_form="complete_reset_password" />
        </div>
    </div>
    <div class="row" v-else>
        <div class="column">
            <h2>Reset Password Empty View</h2>
            <small>{{this.error}}</small>
        </div>
    </div>
</div>
</template>

<script>
import ResetPassword from '@/components/identify/ResetPassword.vue'
import ApiHelper from '@/helpers/api_helper.js'

export default {
    name: 'ResetPasswordView',
    components: {
        ResetPassword,
    },
    data() {
        return {
            success: true,
            uidb64: '',
            token: '',
            error: ''
        }
    },
    mounted() {
        document.title = "Reset Password | iPadel"
        this.check_reset_password_link()
    },
    methods: {
        check_reset_password_link(){

            const uidb64_param = this.$route.params.uidb64
            const token_param  = this.$route.params.token

            // API get call http://127.0.0.1:8000/api/v1/check-reset-password/{uidb64}/{token}

            // If valid response render reset password component
            // Else render reset password empty view with error message

            // Declare the callbacks
            const callback = {
                success: (response) => {
                    this.uidb64 = response.data.uidb64
                    this.token = response.data.token
                },
                error: (error) => {
                    this.success = false
                    this.error = error
                    // Todo: Error messaging
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.checkResetPasswordToken(callback, uidb64_param, token_param)
        },

        complete_reset_password(reset_password_data){
            reset_password_data = {
                'password': reset_password_data.password,
                'uidb64': this.uidb64,
                'token': this.token
            }
            // API PATCH call http://127.0.0.1:8000/api/v1/complete-reset-password/
            //"password": "Something22",
            //"uidb64": "MQ",
            //"token": "asnvoj-1a3d3a324ca34fd12f926f906c28e7a3"


            // Declare the callbacks
            const callback = {
                success: (response) => {
                    console.log("Password reset successful")
                },
                error: (error) => {
                    console.log(error)
                    // Todo: Error messaging
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.setNewPassword(callback, reset_password_data)
        }
    }
}
</script>
