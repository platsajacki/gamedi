import { setBorderRadiusBasedOnHeight, changeImage } from '../main.js'

const gameImgMain = '.game-detail img.main'
const hoverSrcGameImgMain = 'hover-src'


/** Активирует все прослушки 'games_list'. */
async function wiretapping () {
  for (const action of ['resize', 'load']) {
      window.addEventListener(action,
        async () => await setBorderRadiusBasedOnHeight(gameImgMain, 0.15)
      )
  }
  await changeImage(gameImgMain, hoverSrcGameImgMain)
}


await wiretapping()
