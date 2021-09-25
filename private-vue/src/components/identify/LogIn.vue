<template>
<div class="sign-in-component">
    <h2>ALREADY REGISTERED? LOG IN!</h2>
    <div class="login-errors" v-if="this.errors.length">
        <p
        v-for="error in this.errors"
        :key="error">{{error}}</p>
    </div>
    <form @submit.prevent="submit_login_form()">
        <InputField @set_valid="set_valid_email" :label="this.email_field.label" :type="this.email_field.type" :validators="this.email_field.validators" :placeholder="this.email_field.placeholder" :display_errors="this.display_errors"/>
        <InputField @set_valid="set_valid_password" :label="this.password_field.label" :type="this.password_field.type" :validators="this.password_field.validators" :placeholder="this.password_field.placeholder" :display_errors="this.display_errors"/>
        <a href="/shop"><small>Forgotten password?</small></a>
        <br><br><button type="submit">Log in</button>
    </form>
</div>
</template>

<script>
import config from '@/components/identify/config/login_config.js'
import InputField from '@/components/identify/InputField.vue'

export default {
    name: 'LogIn',
    components: {
        InputField
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