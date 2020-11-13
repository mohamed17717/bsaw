// my code
document.addEventListener('DOMContentLoaded', (e) => {
  const responsiveSliderNav = document.querySelectorAll('.owl-nav:not(.disabled)');
  if (responsiveSliderNav.length == 2)
    responsiveSliderNav[0].remove()

  responsiveSliderNav[1].style.position = "absolute"
  responsiveSliderNav[1].style.top = "35%"
  responsiveSliderNav[1].style.left = "10px"
  responsiveSliderNav[1].style.right = "-10px"
  responsiveSliderNav[1].style.bottom = "0"
})