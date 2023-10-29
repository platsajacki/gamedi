import getSizeDiscription from "../main.js"

const actions = ['DOMContentLoaded', 'resize']

/** Активирует все прослушки. */
function wiretapping () {
  console.log('fll')
  for (let action of actions) {
      window.addEventListener(action,
      () =>  getSizeDiscription(
        'game-list-img', 'games-list-discription'
      )
    )
  }
}


wiretapping()
