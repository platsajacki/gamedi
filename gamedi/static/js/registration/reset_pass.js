import {
  setLalbelByFocusInput, changeTextContentByInput
} from '../main.js'

const formClass = 'form.main'
const idEmail = 'id_email'
const newTextContentEmail = 'Электронная почта:'


/** Активирует все прослушки 'reset_pass'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}


await changeTextContentByInput(idEmail, newTextContentEmail)
await wiretapping()
