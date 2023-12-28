import { setBorderRadiusBasedOnHeight, minRadiusImgMain, coefImgMain } from '../main.js'

const gameImgMain = '.game-detail img.main'
const scrollLeftButton = document.getElementById('scroll-left')
const scrollRightButton = document.getElementById('scroll-right')
const mainImage = document.querySelector('.main-detail')
const imagesContainer = document.querySelector('.box-img')
const images = imagesContainer.querySelectorAll('.box-img img')
const activeScrollImage = 'active-image'
const notActiveScrollImage = 'not-active-image'


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
      imagesContainer.scrollTo(
        {
          left: scrollPosition,
          behavior: 'smooth'
        }
      )
    }
  }

  /** Прокручивает изображения влево. */
  async function scrollLeft() {
    if (scrollPosition > 0) {
      scrollPosition -= imageWidth
      imagesContainer.scrollTo(
        {
          left: scrollPosition,
          behavior: 'smooth'
        }
      )
    }
  }

  scrollRightButton.addEventListener('click', scrollRight)
  scrollLeftButton.addEventListener('click', scrollLeft)
}


/**
 * Устанавливает класс `activeScrollImage`
 * на изображении, совпадающем с `currentImageSrc`,
 * и удаляет этот класс у остальных изображений
 * из переданного массива `images`.
 */
async function getActiveImage(images, currentImageScr, activeScrollImage) {
  images.forEach(
    image => {
      if (image.getAttribute('src') === currentImageScr) {
        image.classList.remove(notActiveScrollImage)
        image.classList.add(activeScrollImage)
      } else {
        image.classList.remove(activeScrollImage)
        image.classList.add(notActiveScrollImage)
      }
    }
  )
}

/**
 * Обрабатывает событие клика по изображению в скролле,
 * заменяя основное изображение.
 */
async function handleImageClick(event) {
  const clickedImageSrc = event.target.getAttribute('src')
  mainImage.setAttribute('src', clickedImageSrc)
  await getActiveImage(images, clickedImageSrc, activeScrollImage)
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

  imagesContainer.querySelectorAll('img').forEach(
    image => {image.addEventListener('click', handleImageClick)}
  )
}


await getActiveImage(
  images, mainImage.getAttribute('src'), activeScrollImage
)
await wiretapping()
