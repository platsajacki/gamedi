import { getMaxWordsInElement, setBorderRadiusBasedOnHeight } from "../main.js"

const actions = ['resize', 'load']
const maxWordsInGame = 60

/** Активирует все прослушки 'games_list'. */
async function wiretapping () {
  for (const action of actions) {
      window.addEventListener(action,
        async () => await setBorderRadiusBasedOnHeight('.game img.main', 0.15)
      )
  }
}


await getMaxWordsInElement('text-description', maxWordsInGame)
wiretapping()
