import validators from '@/components/identify/config/validators'

export default {
    password_field: {
        value: '',
        type: 'password',
        validators: validators.signup_validators.password_validators,
        placeholder: 'Password',
        is_valid: false
    },
    repeat_password_field: {
        value: '',
        type: 'password',
        validators: validators.signup_validators.repeat_password_validators,
        placeholder: 'Repeat password',
        is_valid: false
    },
}