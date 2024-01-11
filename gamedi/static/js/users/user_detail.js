import {
  setBorderRadiusBasedOnHeight, minRadiusImgMain, coefImgMain, getMaxCharInElement
} from '../main.js'

const profileGameImg = '.profile-game img'
const profileGameName = 'profile-game-name'
const maxCharInGameName = 30


/** Активирует все прослушки 'user_detail'. */
async function wiretapping () {
  for (const action of ['resize', 'load']) {
    window.addEventListener(action,
      async () => await setBorderRadiusBasedOnHeight(profileGameImg, coefImgMain, minRadiusImgMain)
    )
  }
}

await getMaxCharInElement(profileGameName, maxCharInGameName)
await wiretapping()
