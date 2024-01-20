const mainOrangeColor = 'var(--main-orange)'
const whiteColor = '#fff'
export const coefImgMain = 0.15
export const minRadiusImgMain = 40


/**
 * Проверяет, состоит ли строка только из
 * букв латинского и кириллического алфавитов.
 */
async function isAlpha(str) {
  return /^[a-zA-Zа-яА-Я]+$/.test(str)
}


/**
 * Регулярное выражение,
 * которое ищет только знаки препинания,
 * исключая кавычки.
 */
async function containsPunctuation(str) {
  return /^[.,!?;: -]+$/.test(str)
}


/** Устанавливает количество слов в элементе. */
export async function getMaxWordsInElement(className, maxWords) {
  const elements = document.getElementsByClassName(className)
  for (const element of elements) {
    let words = element.innerHTML.trim().split(' ')
    if (words.length > maxWords) {
      words = words.slice(0, maxWords)
      let lastWord = words[maxWords - 1]
      if (!(await isAlpha(lastWord))) {
        while (await containsPunctuation(lastWord[lastWord.length - 1])) {
          lastWord = lastWord.slice(0, -1)
        }
        words[maxWords - 1] = lastWord
      }
      element.innerHTML = words.join(' ') + '...'
    }
  }
}


/** Устанавливает количество символов в элементе. */
export async function getMaxCharInElement(className, maxChars) {
  const elements = document.getElementsByClassName(className)
  for (const element of elements) {
    let chars = element.textContent
    if (chars.length > maxChars) {
      chars = chars.slice(0, maxChars)
      let lastChar = chars[maxChars-1]
      while (await containsPunctuation(lastChar)) {
        chars = chars.slice(0, -1)
        lastChar = chars[chars.length - 1]
      }
      element.textContent =  chars + '...'
    }
  }
}


/** Устанавливает 'border-radius' в зависимости от coef высоты объекта. */
export async function setBorderRadiusBasedOnHeight(className, coef, minRadius) {
  const elements = document.querySelectorAll(className)
  elements.forEach(element => {
    element.style.borderRadius = Math.max(element.height * coef, minRadius) + 'px'
  })
}


/** Изменяет изображение при наведении. */
export async function changeImage(classImgName, changedAttr) {
  const imgs = document.querySelectorAll(classImgName)

  imgs.forEach(img => {
    const originalSrc = img.src
    const hoverSrc = img.getAttribute(changedAttr)

    img.addEventListener('mouseover', () => {
      img.src = hoverSrc;
    })
    img.addEventListener('mouseout', () => {
      img.src = originalSrc;
    })
  })
}


/** Присваивает по 'ID' ссылку указанную в 'data-url' в теге. */
export async function getUrlById(id) {
  document.getElementById(id).addEventListener(
    'click', function() {window.location.href = this.getAttribute('data-url')}
  )
}


/** В форме обновляет цвет 'label' при фокусе на 'input'. */
export async function setLalbelByFocusInput(formClass) {
  const form = document.querySelector(formClass)
  form.querySelectorAll('input').forEach(
    input => {
      const label = document.querySelector(`label[for="${input.id}"]`)

      if (label) {
        async function handleFocus() {
          label.style.backgroundColor = mainOrangeColor
          label.style.color = whiteColor
        }

        async function handleBlur() {
          label.style.backgroundColor = whiteColor
          label.style.color = mainOrangeColor
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


/** Меняет текст 'label' элемента 'input'. */
export async function changeTextContentByInput(idInput, textContent) {
  const input = document.getElementById(idInput)
  if (input) {input.previousElementSibling.textContent = textContent}
}
