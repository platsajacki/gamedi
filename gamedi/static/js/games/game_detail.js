import { setBorderRadiusBasedOnHeight, minRadiusImgMain, coefImgMain } from '../main.js'

const gameImgMain = '.game-detail img.main'
const scrollLeftButton = document.getElementById('scroll-left')
const scrollRightButton = document.getElementById('scroll-right')
const imagesContainer = document.querySelector('.box-img')

/**
 * Прокручивает изображения в контейнере при нажатии на кнопки прокрутки влево и вправо.
 */
async function getScrollImg(scrollLeftButton, scrollRightButton, imagesContainer) {
  let scrollPosition = 0
  const imageWidth = imagesContainer.firstElementChild.offsetWidth

  /** Прокручивает изображения вправо. */
  async function scrollRight() {
    const maxScroll = imagesContainer.scrollWidth - imagesContainer.clientWidth
    if (scrollPosition < maxScroll) {
      scrollPosition += imageWidth
      imagesContainer.scrollTo({
        left: scrollPosition,
        behavior: 'smooth'
      })
    }
  }

  /** Прокручивает изображения влево. */
  async function scrollLeft() {
    if (scrollPosition > 0) {
      scrollPosition -= imageWidth
      imagesContainer.scrollTo({
        left: scrollPosition,
        behavior: 'smooth'
      })
    }
  }

  scrollRightButton.addEventListener('click', scrollRight)
  scrollLeftButton.addEventListener('click', scrollLeft)
}


/** Активирует все прослушки 'games_list'. */
async function wiretapping () {
  for (const action of ['resize', 'load']) {
    window.addEventListener(action,
      async () => await setBorderRadiusBasedOnHeight(
        gameImgMain, coefImgMain, minRadiusImgMain
      )
    )
  }
  document.addEventListener(
    'DOMContentLoaded',
    async () => await getScrollImg(
      scrollLeftButton, scrollRightButton, imagesContainer
    )
  )
}


await wiretapping()
