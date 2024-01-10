import { getUrlById, setLalbelByFocusInput } from '../main.js'

const formClass = 'form.main'


/** Активирует все прослушки 'user_form'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}


await wiretapping()
