document.addEventListener('DOMContentLoaded', function () {
    renderSlider('.slider');
  });

  const nextSlide = () => {
  let activeSlide = document.querySelector('.slide--active');
  let nextSlide = activeSlide.nextElementSibling;

  if (!nextSlide) {
    nextSlide = document.querySelector('.slide:first-child');
  }

  activeSlide.classList.remove('slide--active');
  nextSlide.classList.remove('next');
  nextSlide.classList.add('slide--active');

  renderSlides();
  renderBtns();
};

  const renderBtns = () => {
    let nextBtn = document.querySelector('#forvard');
    let prevBtn = document.querySelector('#back');

    let activeSlide = document.querySelector('.slide--active');
    let prevSlide = activeSlide.previousElementSibling;
    !prevSlide ? prevBtn.classList.add('disabled') : prevBtn.classList.remove('disabled');

    let nextSlide = activeSlide.nextElementSibling;
    !nextSlide ? nextBtn.classList.add('disabled') : nextBtn.classList.remove('disabled');
  }

  const prevSlide = () => {
  let activeSlide = document.querySelector('.slide--active');
  let prevSlide = activeSlide.previousElementSibling;

  if (!prevSlide) {
    prevSlide = document.querySelector('.slide:last-child');
  }

  activeSlide.classList.remove('slide--active');
  prevSlide.classList.remove('prev');
  prevSlide.classList.add('slide--active');

  renderSlides();
  renderBtns();
};

  const renderSlides = () => {
    let slides = document.querySelectorAll('.slide');
    if (!slides) {
      return;
    }
    let activeSlide = document.querySelector('.slide--active');
    if (!activeSlide) {
      activeSlide = slides.item(0);
      activeSlide.classList.add('slide--active');
    }
    [].forEach.call(slides, function (slide) {
      slide.classList.remove('prev', 'next')
    });

    let prevSlide = activeSlide.previousElementSibling;
    prevSlide && prevSlide.classList.add('prev');

    let nextSlide = activeSlide.nextElementSibling;
    nextSlide && nextSlide.classList.add('next');

   let nextNextSlide = nextSlide ? nextSlide.nextElementSibling : null;
   nextNextSlide && nextNextSlide.classList.add('next');

  }

  const renderSlider = (element) => {
    const slider = document.querySelector(element);
    if (slider) {
      let nextButton = document.querySelector("#forvard");
      nextButton.addEventListener('click', function () {
        nextSlide();
      })

      let prevButton = document.querySelector("#back");
      prevButton.addEventListener('click', function () {
        prevSlide();
      })
      renderSlides();
    }
  }