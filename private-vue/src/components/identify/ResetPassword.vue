<template>
<div class="reset-password-component">
    <form @submit.prevent="submit_reset_password_form()">
        <IdentifyField @set_valid="set_valid_password" :type="this.password_field.type" :validators="this.password_field.validators" :placeholder="this.password_field.placeholder" :display_errors="this.display_errors" />
        <IdentifyField @set_valid="set_valid_repeat_password" :type="this.repeat_password_field.type" :validators="this.repeat_password_field.validators" :placeholder="this.repeat_password_field.placeholder" :display_errors="this.display_errors" :password1="this.password_field.value" />
        <br><br><button type="submit">Set new password</button>
    </form>

</div>
</template>

<script>
import config from '@/components/identify/config/reset_password_config.js'
import IdentifyField from '@/components/identify/IdentifyField.vue'

export default {
    name: 'ResetPasswordComponent',
    components: {
        IdentifyField,
    },
    data() {
        return {
            display_errors: false,
            password_field: config.password_field,
            repeat_password_field: config.repeat_password_field,
        }
    },
    methods: {
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
        submit_reset_password_form() {
            this.display_errors = true

            if (this.validate_fields()) {
                this.perform_reset_password()
            }
        },
        validate_fields() {
            return this.password_field.is_valid && this.repeat_password_field.is_valid
        },
        perform_reset_password() {
            this.$emit('submit_form', {
                'password': this.password_field.value
            })
        }
    }
}
</script>
