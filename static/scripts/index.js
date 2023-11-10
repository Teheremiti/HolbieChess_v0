document.addEventListener("DOMContentLoaded", () => {
  var board;

  function pieceTheme (piece) {
    return 'img/' + piece + '.svg';
  }

  board = Chessboard('board', {
    pieceTheme: pieceTheme,
    position: 'start',
    draggable: false
  });
})
