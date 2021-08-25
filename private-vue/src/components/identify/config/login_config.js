import validators from '@/components/identify/config/validators'

export default {
    email_field: {
        type: 'text',
        validators: validators.login_validators.email_validators,
        placeholder: 'Email'
    },
    password_field: {
        type: 'password',
        validators: validators.login_validators.password_validators,
        placeholder: 'Password'
    },
}