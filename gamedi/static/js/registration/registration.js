import {
  setLalbelByFocusInput, changeTextContentByInput
} from '../main.js'

const formClass = 'form.main'
const idPass2 = 'id_password2'
const newTextContentPass2 = 'Подтвердите пароль:'
const marginTopPass2 = -1.2

/**
 * Выравнивает стандартную форму Django (id_password2)
 * по 'marginTop' и меняет его контент на более короткий.
 * */
async function setStylePass2(marginTop) {
  const errorlist = document.getElementsByClassName('errorlist')
  if (!errorlist.length) {
    const pass2 = document.getElementById(idPass2)
    const labelForPass2 = pass2.previousElementSibling
    pass2.style.marginTop = `${marginTop}rem`
    labelForPass2.style.marginTop = `${marginTop}rem`
  }
}


/** Активирует все прослушки 'registration'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}


await changeTextContentByInput(idPass2, newTextContentPass2)
await setStylePass2(marginTopPass2)
await wiretapping ()