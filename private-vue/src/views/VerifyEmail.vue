<template>
<div class="verify-email">
    <div class="container">
        <div class="row">
            <h1>Verify email</h1>
            <h3>{{ this.message }}</h3>
        </div>
    </div>
</div>
</template>

<script>
import ApiHelper from '@/helpers/api_helper.js'

export default {
    name: 'VerifyEmail',
    data() {
        return {
            token: '',
            message: '',
        }
    },
    mounted() {
        // Fetch the user token from the get query parameter
        this.token = this.$route.query.token
        // Attempt to verify the email with the backend service
        this.verifyEmail()
    },
    methods: {
        verifyEmail() {
            // Declare the callbacks
            const callback = {
                success: (response) => {
                    this.message = response.data.result
                },
                error: (error) => {
                    this.message = error
                }
            }

            // Fetch the current category detail from the Api
            ApiHelper.verifyEmail(callback, this.token)
        }
    }
}
</script>
