const currentUrl = window.location.pathname;
const links = document.querySelectorAll('.nav-menu li a');

/*
Определяет активную ссылку в меню
на основе текущего URL и добавляет класс "active".
 */
function getActiveLink (currentUrl, links) {
  links.forEach(function(link) {
    if (link.getAttribute('href') === currentUrl) {
      link.classList.add('active');
    }
  });
}

getActiveLink(currentUrl, links)
