document.addEventListener("DOMContentLoaded", () => {

  function pieceTheme (piece) {
    return '/img/' + piece + '.svg'
  }

  var board = Chessboard('board', {
    pieceTheme: pieceTheme,
    position: 'start',
    draggable: false
  });
})
