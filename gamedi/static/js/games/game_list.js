import {
  getMaxWordsInElement, setBorderRadiusBasedOnHeight, changeImage
} from '../main.js'

const maxWordsInGame = 60
const gameImgMain = '.game img.main'
const hoverSrcGameImgMain = 'hover-src'
const textDescription = 'text-description'
const games = document.getElementsByClassName('game')
const orangeColor = 'var(--main-orange)'


/** Меняет стили игр на главной в зависимости от номера итерации. */
async function setGameIterStyle(games, color) {
  const innerWidth = window.innerWidth
  for (let i = 1; i < games.length; i += 2) {
    const game = games[i]

    const mainImage = game.querySelector('img.main')
    mainImage.style.order = innerWidth > 1000 ? 1 : 0
    mainImage.style.borderColor = color

    const description = game.querySelector('.description')
    if (innerWidth > 1000) {
      description.style.paddingLeft = 0
      description.style.paddingRight = '1.5rem'
    }
    description.querySelector('.line-circle-right').style.display = 'none'
    description.querySelector('.line-circle-left').style.display = 'flex'
    description.querySelector('.game-name a').style.color = color

    const price = description.querySelector('.price')
    price.querySelector('.final').style.color = color
    price.querySelector('a').style.backgroundColor = color
  }
}


/** Активирует все прослушки 'games_list'. */
async function wiretapping () {
  for (const action of ['DOMContentLoaded', 'resize']) {
      window.addEventListener(action,
        async () => await setGameIterStyle(games, orangeColor)
      )
  }
  for (const action of ['resize', 'load']) {
      window.addEventListener(action,
        async () => await setBorderRadiusBasedOnHeight(gameImgMain, 0.15)
      )
  }
  await changeImage(gameImgMain, hoverSrcGameImgMain)
}


await getMaxWordsInElement(textDescription, maxWordsInGame)
await wiretapping()
