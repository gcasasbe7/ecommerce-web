<template>
<div class="sign-in-component">
    <h2>FIRST TIME HERE? REGISTER!</h2>
    <div class="signup-errors" v-if="this.errors.length">
        <p
        v-for="error in this.errors"
        :key="error">{{error}}</p>
    </div>
    <form @submit.prevent="submit_signup_form()">
        <IdentifyField @set_valid="set_valid_name" :type="this.name_field.type" :validators="this.name_field.validators" :placeholder="this.name_field.placeholder" :display_errors="this.display_errors"/>
        <IdentifyField @set_valid="set_valid_surname" :type="this.surname_field.type" :validators="this.surname_field.validators" :placeholder="this.surname_field.placeholder" :display_errors="this.display_errors"/>
        <IdentifyField @set_valid="set_valid_email" :type="this.email_field.type" :validators="this.email_field.validators" :placeholder="this.email_field.placeholder" :display_errors="this.display_errors"/>
        <IdentifyField @set_valid="set_valid_password" :type="this.password_field.type" :validators="this.password_field.validators" :placeholder="this.password_field.placeholder" :display_errors="this.display_errors"/>
        <IdentifyField @set_valid="set_valid_repeat_password" :type="this.repeat_password_field.type" :validators="this.repeat_password_field.validators" :placeholder="this.repeat_password_field.placeholder" :display_errors="this.display_errors" :password1="this.password_field.value"/>
        <br><br><button type="submit">Register</button>
    </form>
</div>
</template>

<script>
import config from '@/components/identify/config/signup_config.js'
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
                this.display_errors = false
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
        set_valid_name(is_valid, value){
            this.name_field.is_valid=is_valid
            this.name_field.value=value
        },
        set_valid_surname(is_valid, value){
            this.surname_field.is_valid=is_valid
            this.surname_field.value=value
        },
        set_valid_email(is_valid, value){
            this.email_field.is_valid=is_valid
            this.email_field.value=value
        },
        set_valid_password(is_valid, value){
            this.password_field.is_valid=is_valid
            this.password_field.value=value
            
            // Hook the password 1 to the validator object to perform the check
            this.repeat_password_field.validators[0].password1 = this.password_field.value
            // When the password 1 field is updated, the repeated password field is also verified
            //this.display_errors = false

            // todo refactor: Can validators define their own validate method using regex or func?
            // todo refactor: Can IdentityFields recieve one parent object in props?
            // todo new component that will contain both password 1 and 2 fields (RegisterPasswordsIdentityFields)
        },
        set_valid_repeat_password(is_valid, value){
            this.repeat_password_field.is_valid=is_valid 
            this.repeat_password_field.value=value
        },
        perform_signup(){
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
