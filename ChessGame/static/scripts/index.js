document.addEventListener("DOMContentLoaded", () => {

  function pieceTheme (piece) {
    return '/img/' + piece + '.svg'
  }

  var board = Chessboard('board', {
    pieceTheme: pieceTheme,
    position: 'start',
    draggable: false
  });

  $('button.local').on('click', () => {
    window.location.href = '/play.html?mode=1v1';
  })

  $('button.computer').on('click', () => {
    window.location.href = '/play.html?mode=computer';
  })
})
