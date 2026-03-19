document.addEventListener("DOMContentLoaded", function () {

  const hero = document.getElementById("heroSlide");

  if (!hero) {
    console.log("❌ heroSlide not found");
    return;
  }

  if (typeof images === "undefined") {
    console.log("❌ images array not found");
    return;
  }

  let index = 0;

  function showSlide(i) {
    hero.style.backgroundImage = `url('${images[i]}')`;
    console.log("Showing:", images[i]); // debug
  }

  function nextSlide() {
    index = (index + 1) % images.length;
    showSlide(index);
  }

  function prevSlide() {
    index = (index - 1 + images.length) % images.length;
    showSlide(index);
  }

  showSlide(index);
  setInterval(nextSlide, 4000);

  window.nextSlide = nextSlide;
  window.prevSlide = prevSlide;

});


document.addEventListener("DOMContentLoaded", function () {

    console.log("JS Loaded");

    // TOGGLE FILTER
    window.toggleFilter = function (el) {
        el.parentElement.classList.toggle("active");
    };

    // PRICE SLIDER
    const priceRange = document.getElementById("priceRange");
    const priceValue = document.getElementById("priceValue");

    if (priceRange && priceValue) {
        priceRange.addEventListener("input", function () {
            priceValue.innerText = this.value;
        });
    }

});

