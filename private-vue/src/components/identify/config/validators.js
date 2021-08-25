// VALIDATORS DEFINITION
const EMAIL_VALIDATOR = {
    regex: /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    error: "Please introduce a valid email"
}
const PASSWORD_LENGTH_VALIDATOR = {
    regex: /[a-zA-Z0-9]{8,}$/,
    error: "Your password must contain at least 8 characters"
}
const PASSWORD_CONTAINS_NUMBER_VALIDATOR = {
    regex: /\d/,
    error: "Your password must contain at least one number"
}
const PASSWORD_CONTAINS_CAPITAL_VALIDATOR = {
    regex: /[A-Z]/,
    error: "Your password must contain at least one capital letter"
}
const VALID_TEXT_VALIDATOR = {
    regex: /^[a-z\s]{0,255}$/i,
    error: "Please introduce a valid text"
}

export default {
    login_validators: {
        email_validators: [EMAIL_VALIDATOR],
        password_validators: [
            PASSWORD_LENGTH_VALIDATOR, 
            PASSWORD_CONTAINS_NUMBER_VALIDATOR, 
            PASSWORD_CONTAINS_CAPITAL_VALIDATOR
        ]
    },
    signup_validators: {
        email_validators: [EMAIL_VALIDATOR],
        password_validators: [
            PASSWORD_LENGTH_VALIDATOR, 
            PASSWORD_CONTAINS_NUMBER_VALIDATOR, 
            PASSWORD_CONTAINS_CAPITAL_VALIDATOR
        ],
        text_validators: [VALID_TEXT_VALIDATOR]
    }
}