import { setLalbelByFocusInput } from '../main.js'

const formClass = 'form.main'
const errorformset = document.querySelector('.errorformset')
const formsetInfo = document.querySelector('.formset-info')

/** Активирует все прослушки 'game_profile'. */
async function wiretapping () {
  await setLalbelByFocusInput(formClass)
}

if (errorformset && errorformset.textContent) {
  errorformset.scrollIntoView({'behavior': 'smooth'})
}

if (formsetInfo) {
  formsetInfo.scrollIntoView({'behavior': 'smooth'})
}

await wiretapping()
