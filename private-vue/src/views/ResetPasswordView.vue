<template>
<div class="reset-password">
    <div class="row" v-if="this.valid_link">
        <div class="column">
            <ResetPassword v-if="!this.password_successfuly_reseted" @submit_form="complete_reset_password" />
            <div v-else>
                <h1>Password reset was successful! Press the button below to log in</h1>
                <button @click="redirect_to_identification">Log In</button>
            </div>
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
            password_successfuly_reseted: false,
            valid_link: true,
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
            // Fetch the url parameters
            const uidb64_param = this.$route.params.uidb64
            const token_param  = this.$route.params.token

            // Declare the callbacks
            const callback = {
                success: (response) => {
                    this.uidb64 = response.data.uidb64
                    this.token = response.data.token
                },
                error: (error) => {
                    this.valid_link = false
                    this.error = error
                    // Todo: Error messaging
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.checkResetPasswordToken(callback, uidb64_param, token_param)
        },

        complete_reset_password(reset_password_data){
            // Build the reset password data object
            reset_password_data = {
                'password': reset_password_data.password,
                'uidb64': this.uidb64,
                'token': this.token
            }

            // Declare the callbacks
            const callback = {
                success: (response) => {
                    this.password_successfuly_reseted = true
                    console.log("Password reset successful")
                },
                error: (error) => {
                    console.log(error)
                    // Todo: Error messaging
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.setNewPassword(callback, reset_password_data)
        },
        redirect_to_identification(){
            this.$router.push('/identify')
        }
    }
}
</script>
