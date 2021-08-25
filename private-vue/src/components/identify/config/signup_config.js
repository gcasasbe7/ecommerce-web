import validators from '@/components/identify/config/validators'

export default {
    email_field: {
        type: 'text',
        validators: validators.signup_validators.email_validators,
        placeholder: 'Email'
    },
    password_field: {
        type: 'password',
        validators: validators.signup_validators.password_validators,
        placeholder: 'Password'
    },
    repeat_password_field: {
        type: 'password',
        validators: validators.signup_validators.password_validators,
        placeholder: 'Repeat password'
    },
    name_field: {
        type: 'text',
        validators: validators.signup_validators.text_validators,
        placeholder: 'Name'
    },
    surname_field: {
        type: 'text',
        validators: validators.signup_validators.text_validators,
        placeholder: 'Surname'
    },
}