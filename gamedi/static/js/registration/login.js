import { getUrlById } from '../main.js'

const registrationButton = 'registration-button'
const formClass = 'form.main'
const mainOrangeColor = 'var(--main-orange)'
const whiteColor = '#fff'

/** В форме обновляет цвет 'label' при фокусе на 'input'. */
async function setLalbelByFocusInput(formClass) {
  const form = document.querySelector(formClass)
  form.querySelectorAll('input').forEach(
    input => {
      const label = document.querySelector(`label[for="${input.id}"]`)

      if (label) {
        async function handleFocus() {
          label.style.backgroundColor = mainOrangeColor;
          label.style.color = whiteColor;
        }

        async function handleBlur() {
          label.style.backgroundColor = whiteColor;
          label.style.color = mainOrangeColor;
        }

        input.addEventListener('focus', handleFocus)
        input.addEventListener('blur', handleBlur)

        if (input.hasAttribute('autofocus')) {
          handleFocus()
        }
      }
    }
  )
}


/** Активирует все прослушки 'login'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}


await getUrlById(registrationButton)
await wiretapping ()