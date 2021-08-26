<template>
<div class="sign-in-component">
    <h2>ALREADY REGISTERED? LOG IN!</h2>
    <div class="login-errors" v-if="this.errors.length">
        <p
        v-for="error in this.errors"
        :key="error">{{error}}</p>
    </div>
    <form @submit.prevent="submit_login_form()">
        <IdentifyField @set_valid="set_valid_email" :type="this.email_field.type" :validators="this.email_field.validators" :placeholder="this.email_field.placeholder" :display_errors="this.display_errors"/>
        <IdentifyField @set_valid="set_valid_password" :type="this.password_field.type" :validators="this.password_field.validators" :placeholder="this.password_field.placeholder" :display_errors="this.display_errors"/>
        <br><br><button type="submit">Log in</button>
    </form>
</div>
</template>

<script>
import config from '@/components/identify/config/login_config.js'
import IdentifyField from '@/components/identify/IdentifyField.vue'

export default {
    name: 'LogIn',
    components: {
        IdentifyField
    },
    props: {
        errors: Array,
    },
    data() {
        return {
            display_errors: false,
            email_field: config.email_field,
            password_field: config.password_field
        }
    },
    methods: {
        submit_login_form() {
            this.display_errors = true

            if (this.validate_fields()) {
                this.perform_login()
            }
        },
        validate_fields() {return this.email_field.is_valid && this.password_field.is_valid},
        set_valid_email(is_valid, value){
            this.email_field.is_valid=is_valid
            this.email_field.value=value

        },
        set_valid_password(is_valid, value){
            this.password_field.is_valid=is_valid
            this.password_field.value=value
        },
        perform_login() {
            this.$emit('submit_form', {
                'email': this.email_field.value,
                'password': this.password_field.value
            })
        }
    }
}
</script>
