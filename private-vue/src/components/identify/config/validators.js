// VALIDATORS DEFINITION
const EMAIL_VALIDATOR = {
    name: 'email_validator',
    regex: /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    error: "Please introduce a valid email",
    validate: (value) => {return EMAIL_VALIDATOR.regex.test(value)}
}
const PASSWORD_LENGTH_VALIDATOR = {
    name: 'password_length_validator',
    regex: /[a-zA-Z0-9]{8,}$/,
    error: "Your password must contain at least 8 characters",
    validate: (value) => {return PASSWORD_LENGTH_VALIDATOR.regex.test(value)}
}
const PASSWORD_CONTAINS_NUMBER_VALIDATOR = {
    name: 'password_contains_number_validator',
    regex: /\d/,
    error: "Your password must contain at least one number",
    validate: (value) => {return PASSWORD_CONTAINS_NUMBER_VALIDATOR.regex.test(value)}
}
const PASSWORD_CONTAINS_CAPITAL_VALIDATOR = {
    name: 'password_contains_capital_validator',
    regex: /[A-Z]/,
    error: "Your password must contain at least one capital letter",
    validate: (value) => {return PASSWORD_CONTAINS_CAPITAL_VALIDATOR.regex.test(value)}
}
const VALID_TEXT_VALIDATOR = {
    name: 'valid_text_validator',
    regex: /^[a-z\s]{0,255}$/i,
    error: "Please introduce a valid text",
    validate: (value) => {return VALID_TEXT_VALIDATOR.regex.test(value)}
}
const NOT_EMPTY_TEXT_VALIDATOR = {
    name: 'not_empty_text_validator',
    regex: /^(?!\s*$).+/,
    error: "Please fill this field",
    validate: (value) => {return NOT_EMPTY_TEXT_VALIDATOR.regex.test(value)}
}
const PASSWORDS_MATCH = {
    name: 'passwords_match_validator',
    password1: '',
    validate: (value) => {return PASSWORDS_MATCH.password1 === value},
    error: "Passwords don't match"
}

export default {
    // Login form validators definition
    login_validators: {
        email_validators: [EMAIL_VALIDATOR],
        password_validators: [
            PASSWORD_LENGTH_VALIDATOR, 
            PASSWORD_CONTAINS_NUMBER_VALIDATOR, 
            PASSWORD_CONTAINS_CAPITAL_VALIDATOR
        ]
    },
    // Sign up form validators definition
    signup_validators: {
        email_validators: [EMAIL_VALIDATOR],
        password_validators: [
            PASSWORD_LENGTH_VALIDATOR, 
            PASSWORD_CONTAINS_NUMBER_VALIDATOR, 
            PASSWORD_CONTAINS_CAPITAL_VALIDATOR
        ],
        repeat_password_validators: [
            PASSWORDS_MATCH,
        ],
        text_validators: [NOT_EMPTY_TEXT_VALIDATOR, VALID_TEXT_VALIDATOR]
    },
    // Reset password form validators definition
    reset_password_validators: {
        password_validators: [
            PASSWORD_LENGTH_VALIDATOR, 
            PASSWORD_CONTAINS_NUMBER_VALIDATOR, 
            PASSWORD_CONTAINS_CAPITAL_VALIDATOR
        ],
        repeat_password_validators: [
            PASSWORDS_MATCH,
        ],
    }
}