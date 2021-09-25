import validators from '@/components/identify/config/validators'

export default {
    email_field: {
        value: '',
        type: 'text',
        validators: validators.login_validators.email_validators,
        placeholder: 'Email',
        is_valid: false,
        label: 'Email'
    },
    password_field: {
        value: '',
        type: 'password',
        validators: validators.login_validators.password_validators,
        placeholder: 'Password',
        is_valid: false,
        label: 'Password'
    },
}