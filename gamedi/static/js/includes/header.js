const currentUrl = window.location.pathname;
const links = document.querySelectorAll('.nav-menu li a');
const burger = document.getElementById('burger')
const arrow = document.getElementById('arrow')
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
function getBurgerLinks(elem, burgerLinks) {
  if (elem === burger) {
    burgerLinks.style.display = 'flex';
    burger.style.display = 'none';
    arrow.style.display = 'block';
  } else {
    burgerLinks.style.display = 'none';
    burger.style.display = 'block';
    arrow.style.display = 'none';
  }
}


function rollBurgerMenu(burger, arrow, burgerLinks) {
  burger.addEventListener('click', function (event) {
    getBurgerLinks(burger, burgerLinks)
  })
  arrow.addEventListener('click', function (event) {
    getBurgerLinks(arrow, burgerLinks);
  });
}


rollBurgerMenu(burger, arrow, burgerLinks)
getActiveLink(currentUrl, links);
