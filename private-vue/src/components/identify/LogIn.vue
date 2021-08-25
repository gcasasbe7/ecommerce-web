<template>
<div class="sign-in-component">
    <h2>ALREADY REGISTERED? LOG IN!</h2>
    <form @submit.prevent="submitSignInForm()">
        <IdentifyField :type="this.email_field.type" :validators="this.email_field.validators" :placeholder="this.email_field.placeholder" />
        <IdentifyField :type="this.password_field.type" :validators="this.password_field.validators" :placeholder="this.password_field.placeholder" />
        <!-- <br><input type="text" name="userEmail" placeholder="Email" v-model="email">
        <br><input type="password" name="userPassword" placeholder="Password" v-model="password"> -->
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
    data() {
        return {
            email_field: config.email_field,
            password_field: config.password_field,
        }
    },
    methods: {
        submitSignInForm() {
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
