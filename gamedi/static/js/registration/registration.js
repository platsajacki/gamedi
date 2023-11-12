import {
  setLalbelByFocusInput, changeTextContentByInput
} from '../main.js'

const formClass = 'form.main'
const idPass2 = 'id_password2'
const newTextContentPass2 = 'Подтвердите пароль:'
const nameEmailInput = 'email'


/** Добовляет 'autocomplete' к 'input' по 'name'. */
async function addInputAutocompleteByName (name) {
  const input = document.querySelector(`input[name='${name}']`)
  if (input) {
    input.setAttribute('autocomplete', 'email')
  }
}


/** Активирует все прослушки 'registration'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}


await addInputAutocompleteByName(nameEmailInput)
await changeTextContentByInput(idPass2, newTextContentPass2)
await wiretapping()