const grid = document.querySelector('.grid');
const msnry = new Masonry(grid, {
  itemSelector: '.box',
  columnWidth: '.box',
  gutter: 15,
  horizontalOrder: true,
});

// relance Masonry après le chargement complet
window.addEventListener('load', () => {
  msnry.layout();
});

