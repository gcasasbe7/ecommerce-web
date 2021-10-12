import validators from '@/components/identify/config/validators'

export default {
    email_field: {
        value: 'test@gmail.com',
        type: 'text',
        validators: validators.signup_validators.email_validators,
        placeholder: 'Email',
        is_valid: false,
        label: 'Email',
    },
    password_field: {
        value: '',
        type: 'password',
        validators: validators.signup_validators.password_validators,
        placeholder: 'Password',
        is_valid: false,
        label: 'Password',
    },
    repeat_password_field: {
        value: '',
        type: 'password',
        validators: validators.signup_validators.repeat_password_validators,
        placeholder: 'Repeat password',
        is_valid: false,
        label: 'Repeat password',
    },
    name_field: {
        value: '',
        type: 'text',
        validators: validators.signup_validators.text_validators,
        placeholder: 'Name',
        is_valid: false,
        label: 'Name',
    },
    surname_field: {
        value: '',
        type: 'text',
        validators: validators.signup_validators.text_validators,
        placeholder: 'Surname',
        is_valid: false,
        label: 'Surname',
    },
}