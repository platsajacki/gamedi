import {
  setLalbelByFocusInput, changeTextContentByInput
} from '../main.js'

const formClass = 'form.main'
const idEmail = 'id_email'
const newTextContentEmail = 'Электронная почта:'
const idNewPass2 = 'id_new_password2'
const newTextPass2 = 'Повторите пароль:'


/** Активирует все прослушки 'reset_pass'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}


await changeTextContentByInput(idEmail, newTextContentEmail)
await changeTextContentByInput(idNewPass2, newTextPass2)
await wiretapping()
