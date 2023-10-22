const currentUrl = window.location.pathname;
const links = document.querySelectorAll('.nav-menu li a');
const burger = document.getElementById('burger')
const burgerLinks = document.getElementById('burger-links')

/*
Определяет активную ссылку в меню
на основе текущего URL и добавляет класс "active".
 */
function getActiveLink(currentUrl, links) {
  links.forEach(function (link) {
    if (link.getAttribute('href') === currentUrl) {
      link.classList.add('active');
    }
  });
}


/* Раскрыввает и закрывает бургер меню. */
function getBurgerLinks(burgerLinks) {
  if (burgerLinks.style.display === 'none') {
    burgerLinks.style.display = 'flex';
  } else {
    burgerLinks.style.display = 'none';
  }
}


function rollBurgerMenu(burger, burgerLinks) {
  burger.addEventListener('click', function (event) {
    getBurgerLinks(burgerLinks)
  })
}


rollBurgerMenu(burger, burgerLinks)
getActiveLink(currentUrl, links);
