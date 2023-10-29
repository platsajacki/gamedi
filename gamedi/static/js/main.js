/** Выравнивает 'example' с 'final' в контейнере по высоте.*/
export default function getSizeDiscription(example_id, final_id) {
  let example_elem = document.getElementById(example_id)
  let final_elem = document.getElementById(final_id)
  final_elem.style.maxHeight = `${example_elem.height}px`
}
