import { getMaxWordsInElement, setBorderRadiusBasedOnHeight } from "../main.js"

const actions = ['DOMContentLoaded', 'resize']
const maxWordsInGame = 60

/** Активирует все прослушки 'games_list'. */
async function wiretapping () {
  getMaxWordsInElement('text-description', maxWordsInGame)
  for (const action of actions) {
      window.addEventListener(action,
        () => setBorderRadiusBasedOnHeight('.game img')
      )
  }
}


wiretapping()
