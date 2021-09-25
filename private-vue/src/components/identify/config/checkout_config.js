import validators from '@/components/identify/config/validators'

export default {
    name_field: {
        value: '',
        type: 'text',
        validators: validators.checkout_validators.text_validators,
        placeholder: 'Name',
        is_valid: false,
        label: 'Name'
    },
    surname_field: {
        value: '',
        type: 'text',
        validators: validators.checkout_validators.text_validators,
        placeholder: 'Surname',
        is_valid: false,
        label: 'Surname'
    },
    email_field: {
        value: '',
        type: 'text',
        validators: validators.checkout_validators.email_validators,
        placeholder: 'Email',
        is_valid: false,
        label: 'Email'
    },
    phone_field: {
        value: '',
        type: 'text',
        validators: validators.checkout_validators.phone_validators,
        placeholder: 'Phone number',
        is_valid: false,
        label: 'Phone number'
    },
    address_field: {
        value: '',
        type: 'text',
        validators: validators.checkout_validators.address_validators,
        placeholder: 'Full address',
        is_valid: false,
        label: 'Address'
    },
    city_field: {
        value: '',
        type: 'text',
        validators: validators.checkout_validators.city_validators,
        placeholder: 'City',
        is_valid: false,
        label: 'City'
    },
    zipcode_field: {
        value: '',
        type: 'text',
        validators: validators.checkout_validators.zipcode_validators,
        placeholder: 'Zipcode',
        is_valid: false,
        label: 'Zipcode'
    },

}