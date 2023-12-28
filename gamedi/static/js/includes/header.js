const currentUrl = window.location.pathname;
const links = document.querySelectorAll('.nav-menu li a');
const burger = document.getElementById('burger')
const cross = document.getElementById('cross')
const burgerLinks = document.getElementById('burger-links')
const foxUpperPath = '/static/img/includes/fox_upper.svg'
const foxBottomPath = '/static/img/includes/fox_bottom.svg'

/**
 * Определяет активную ссылку в меню
 * на основе текущего URL и добавляет класс "active".
*/
async function getActiveLink(currentUrl, links, foxUpperPath, foxBottomPath) {
  links.forEach(function (link) {
      if (link.getAttribute('href') === currentUrl) {
        const upperImg = document.createElement('img')
        upperImg.classList.add('active-link')
        upperImg.src = foxUpperPath
        link.parentNode.insertBefore(upperImg, link)
        const bottomImg = document.createElement('img')
        bottomImg.classList.add('active-link', 'bottom')
        bottomImg.src = foxBottomPath
        link.parentNode.insertBefore(bottomImg, link.nextSibling)
      }
    }
  )
}


/** Раскрыввает и закрывает выплывающее меню. */
async function getBurgerLinks(elem, burgerLinks) {
  if (elem === burger) {
    burgerLinks.style.display = 'flex'
    burger.style.display = 'none'
    cross.style.display = 'block'
    return
  }
  burgerLinks.style.display = 'none'
  burger.style.display = 'block'
  cross.style.display = 'none'
}


/** Включает прослушку для открытия и закрытия меню. */
async function rollBurgerMenu(burger, cross, burgerLinks) {
  burger.addEventListener('click', async function (event) {
    await getBurgerLinks(burger, burgerLinks)
  })
  cross.addEventListener('click', async function (event) {
    await getBurgerLinks(cross, burgerLinks)
  })
}


rollBurgerMenu(burger, cross, burgerLinks)
getActiveLink(currentUrl, links, foxUpperPath, foxBottomPath)
