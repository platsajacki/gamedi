import { setBorderRadiusBasedOnHeight, changeImage } from '../main.js'

const gameImgMain = '.game-detail img.main'


/** Активирует все прослушки 'games_list'. */
async function wiretapping () {
  for (const action of ['resize', 'load']) {
      window.addEventListener(action,
        async () => await setBorderRadiusBasedOnHeight(gameImgMain, 0.15)
      )
  }
}


await wiretapping()
