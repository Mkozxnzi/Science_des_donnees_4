const grid = document.querySelector('.grid');

new Masonry(grid, {
  itemSelector: '.box',
  columnWidth: '.box',
  gutter: 15,
  horizontalOrder: true,
});
