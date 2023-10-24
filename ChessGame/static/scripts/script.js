document.addEventListener("DOMContentLoaded", () => {
  var board;
  var game = new Chess();
  var isGameOver = false;
  //var stockfish = new Worker('stockfish');

  var $history = $('.history');
  var history = [];

  /*stockfish.postMessage('uci');
  stockfish.postMessage('isready');
  stockfish.postMessage('ucinewgame');*/

  function onDragStart (source, piece, position, orientation) {
    if (game.in_checkmate() === true || game.in_draw() === true || isGameOver === true ||
        (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
      return false;
    }
  }

  var onDrop = function (source, target) {
    var move = game.move({
      from: source,
      to: target,
      promotion: 'q'
    });

    removeGreySquares();
    if (move === null) return 'snapback';

    // Push the move to history
    history.push(`${move.from}${move.to}`);
    $history.text(history.join(' '));

    /*// Make the AI opponent move
    stockfish.postMessage('position fen ' + game.fen());
    stockfish.postMessage('go depth 5');*/
  };

  var onSnapEnd = function () {
    board.position(game.fen());
  };

  var removeGreySquares = function () {
    $('#board .square-55d63').css('background', '');
  };

  var greySquare = function (square) {
    var squareEl = $('#board .square-' + square);

    var background = '#a9a9a9';
    if (squareEl.hasClass('black-3c85d') === true) {
      background = '#696969';
    }

    squareEl.css('background', background);
  };

  var onDragMove = function (oldPos, newPos) {
    var square = newPos;
    removeGreySquares();

    var moves = game.moves({
      square: square,
      verbose: true
    });

    for (var i = 0; i < moves.length; i++) {
      greySquare(moves[i].to);
    }
  };

  /*stockfish.onmessage = function (event) {
    if (event.data.startsWith('bestmove')) {
      var bestMove = event.data.split(' ')[1];
      game.ugly_move(bestMove);
      board.position(game.fen());
      // Push the AI move to history
      history.push(game.fen());
      $history.text(history.join(' '));
    }
  };*/

  board = ChessBoard('board', {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: removeGreySquares,
    onSnapEnd: onSnapEnd,
    onDragMove: onDragMove
  });
})
