import { getUrlById, setLalbelByFocusInput } from '../main.js'

const registrationButton = 'registration-button'
const formClass = 'form.main'


/** Активирует все прослушки 'login'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}


await getUrlById(registrationButton)
await wiretapping()