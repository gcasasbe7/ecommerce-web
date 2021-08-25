<template>
<div class="sign-in-component">
    <h2>FIRST TIME HERE? REGISTER!</h2>
    <form @submit.prevent="submitSignUpForm()">
        <IdentifyField :type="this.name_field.type" :validators="this.name_field.validators" :placeholder="this.name_field.placeholder" />
        <IdentifyField :type="this.surname_field.type" :validators="this.surname_field.validators" :placeholder="this.surname_field.placeholder" />
        <IdentifyField :type="this.email_field.type" :validators="this.email_field.validators" :placeholder="this.email_field.placeholder" />
        <IdentifyField :type="this.password_field.type" :validators="this.password_field.validators" :placeholder="this.password_field.placeholder" />
        <IdentifyField :type="this.repeat_password_field.type" :validators="this.repeat_password_field.validators" :placeholder="this.repeat_password_field.placeholder" />

        <!-- <br><input type="text" name="userName" placeholder="Name" v-model="s_name">
        <br><input type="text" name="userSurname" placeholder="Surname" v-model="s_surname">
        <br><input type="text" name="userEmail" placeholder="Email" v-model="s_email">
        <br><input type="password" name="userPassword" placeholder="Password" v-model="s_password">
        <br><input type="password" name="userPassword2" placeholder="Repeat password" v-model="s_password2"> -->
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
    mounted() {
        console.log("")
    },
    data() {
        return {
            email_field: config.email_field,
            password_field: config.password_field,
            repeat_password_field: config.repeat_password_field,
            name_field: config.name_field,
            surname_field: config.surname_field,
        }
    },
    methods: {
        submitSignUpForm() {
            if (this.validate_fields()) {
                /* 
                COMMUNICATE CHILDER IDENTIFYFIELDS TO VALIDATE THEMSELVES
                FETCH THE RESULT FROM ALL THE IDENTIFY FIELDS
                IF ALL THE VALIDATIONS ARE CORRECT

                SHOOT THE API LOG IN CALL
                
                ELSE DO NOTHING (IDENTIFYFIELDS WILL DISPLAY THE CONVENIENT ERRORS)
                */
            }
        },
        validate_fields() {
            
        }
    }
}
</script>
