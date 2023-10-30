import getSizeDescription from "../main.js"

const actions = ['DOMContentLoaded', 'resize']

/** Активирует все прослушки. */
function wiretapping () {
  console.log('fll')
  for (let action of actions) {
      window.addEventListener(action,
      () =>  getSizeDescription(
        'game-list-img', 'games-list-description'
      )
    )
  }
}


wiretapping()
