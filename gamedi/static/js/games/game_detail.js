import { setBorderRadiusBasedOnHeight, minRadiusImgMain, coefImgMain } from '../main.js'

const gameImgMain = '.game-detail img.main'


/** Активирует все прослушки 'games_list'. */
async function wiretapping () {
  for (const action of ['resize', 'load']) {
      window.addEventListener(action,
        async () => await setBorderRadiusBasedOnHeight(
          gameImgMain, coefImgMain, minRadiusImgMain
        )
      )
  }
}

// const scrollRight = document.getElementById('scroll-right')
// const boxImg = document.getElementById('box-img')

// scrollRight.addEventListener('click', function() {
//     boxImg
//   }
// )

await wiretapping()
