<template>
<div class="sign-in-component">
    <h2>FIRST TIME HERE? REGISTER!</h2>
    <div class="signup-errors" v-if="this.errors.length">
        <p v-for="error in this.errors" :key="error">{{error}}</p>
    </div>
    <form @submit.prevent="submit_signup_form()">
        <InputField @set_valid="set_valid_name" :label="this.name_field.label" :type="this.name_field.type" :validators="this.name_field.validators" :placeholder="this.name_field.placeholder" :display_errors="this.display_errors" />
        <InputField @set_valid="set_valid_surname" :label="this.surname_field.label" :type="this.surname_field.type" :validators="this.surname_field.validators" :placeholder="this.surname_field.placeholder" :display_errors="this.display_errors" />
        <InputField @set_valid="set_valid_email" :label="this.email_field.label" :type="this.email_field.type" :validators="this.email_field.validators" :placeholder="this.email_field.placeholder" :display_errors="this.display_errors" />
        <InputField @set_valid="set_valid_password" :label="this.password_field.label" :type="this.password_field.type" :validators="this.password_field.validators" :placeholder="this.password_field.placeholder" :display_errors="this.display_errors" />
        <InputField @set_valid="set_valid_repeat_password" :label="this.repeat_password_field.label" :type="this.repeat_password_field.type" :validators="this.repeat_password_field.validators" :placeholder="this.repeat_password_field.placeholder" :display_errors="this.display_errors" :password1="this.password_field.value" />
        <br><br><button type="submit">Register</button>
    </form>
</div>
</template>

<script>
import config from '@/components/identify/config/signup_config.js'
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
            password_field: config.password_field,
            repeat_password_field: config.repeat_password_field,
            name_field: config.name_field,
            surname_field: config.surname_field,
        }
    },
    methods: {
        submit_signup_form() {
            this.display_errors = true

            if (this.validate_fields()) {
                this.perform_signup()
            }
        },
        validate_fields() {
            return this.name_field.is_valid &&
                this.surname_field.is_valid &&
                this.email_field.is_valid &&
                this.password_field.is_valid &&
                this.repeat_password_field.is_valid
        },
        set_valid_name(is_valid, value) {
            this.name_field.is_valid = is_valid
            this.name_field.value = value
        },
        set_valid_surname(is_valid, value) {
            this.surname_field.is_valid = is_valid
            this.surname_field.value = value
        },
        set_valid_email(is_valid, value) {
            this.email_field.is_valid = is_valid
            this.email_field.value = value
        },
        set_valid_password(is_valid, value) {
            this.password_field.is_valid = is_valid
            this.password_field.value = value

            // Hook the password 1 value to the repeat password validator object to perform the check
            this.repeat_password_field.validators[0].password1 = this.password_field.value
        },
        set_valid_repeat_password(is_valid, value) {
            this.repeat_password_field.is_valid = is_valid
            this.repeat_password_field.value = value
        },
        perform_signup() {
            this.$emit('submit_form', {
                'name': this.name_field.value,
                'surname': this.surname_field.value,
                'email': this.email_field.value,
                'password': this.password_field.value
            })
        }
    }
}
</script>
