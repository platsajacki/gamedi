/**
 * Проверяет, состоит ли строка только из
 * букв латинского и кириллического алфавитов.
 */
async function isAlpha(str) {
  return /^[a-zA-Zа-яА-Я]+$/.test(str);
}


/**
 * Регулярное выражение,
 * которое ищет только знаки препинания,
 * исключая кавычки.
 */
async function containsPunctuation(str) {
  return /^[.,!?;:-]+$/.test(str);
}


/** Устанавливает количество символов в элементе. */
export async function getMaxWordsInElement(className, maxWords) {
  const elements = document.getElementsByClassName(className)
  for (const element of elements) {
    let words = element.textContent.trim().split(' ')
    if (words.length > maxWords) {
      words = words.slice(0, maxWords)
      let lastWord = words[maxWords - 1]
      if (!(await isAlpha(lastWord))) {
        while (await containsPunctuation(lastWord[lastWord.length - 1])) {
          lastWord = lastWord.slice(0, -1)
        }
        words[maxWords - 1] = lastWord
      }
      element.textContent = words.join(' ') + '...'
    }
  }
}


/** Устанавливает 'border-radius' в зависимостиот высоты объекта. */
export async function setBorderRadiusBasedOnHeight(className) {
  const elements = document.querySelectorAll(className)
  elements.forEach(element => {
    element.style.borderRadius = element.height * 0.15 + 'px'
  })
}
