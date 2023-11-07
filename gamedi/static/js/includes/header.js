const currentUrl = window.location.pathname;
const links = document.querySelectorAll('.nav-menu li a');
const burger = document.getElementById('burger')
const cross = document.getElementById('cross')
const burgerLinks = document.getElementById('burger-links')

/**
 * Определяет активную ссылку в меню
 * на основе текущего URL и добавляет класс "active".
*/
async function getActiveLink(currentUrl, links) {
  links.forEach(function (link) {
    if (link.getAttribute('href') === currentUrl) {
      link.classList.add('active')
    }
  })
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
  burger.addEventListener('click', function (event) {
    getBurgerLinks(burger, burgerLinks)
  })
  cross.addEventListener('click', function (event) {
    getBurgerLinks(cross, burgerLinks)
  })
}


rollBurgerMenu(burger, cross, burgerLinks)
getActiveLink(currentUrl, links)
