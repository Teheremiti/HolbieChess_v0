document.addEventListener("DOMContentLoaded", () => {
  var board;
  var game = new Chess();
  var mode = 'computer';
  var isGameOver = false;
  var moveCount = 0;

  var $history = $('.history');
  var history = [];

  function makeRandomMove () {
    var possibleMoves = game.moves();

    // Game over
    if (possibleMoves.length === 0) {
      isGameOver = true;
      return;
    }

    // Play a random legal move for black and update the board position
    var randomIdx = Math.floor(Math.random() * possibleMoves.length);
    game.move(possibleMoves[randomIdx]);

    board.position(game.fen());
  }

  var greySquare = function (square) {
    var squareEl = $('#board .square-' + square);

    var background = '#a9a9a9';
    if (squareEl.hasClass('black-3c85d') === true) {
      background = '#696969';
    }

    squareEl.css('background', background);
  };

  var removeGreySquares = function () {
    $('#board .square-55d63').css('background', '');
  };

  function onMouseoverSquare (square, piece) {
    // get list of possible moves for this square
    var moves = game.moves({
      square: square,
      verbose: true
    })

    // exit if there are no moves available for this square
    if (moves.length === 0) return

    // highlight the square moused over
    greySquare(square)

    // highlight the possible squares for this piece
    for (var i = 0; i < moves.length; i++) {
      greySquare(moves[i].to)
    }
  }

  function onMouseoutSquare (square, piece) {
    removeGreySquares()
  }

  function onDragStart (source, piece, position, orientation) {
    if (game.in_checkmate() === true || game.in_draw() === true || isGameOver === true ||
        (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
      return false;
    }
  }

  var onDrop = function (source, target) {
    removeGreySquares();

    var move = game.move({
      from: source,
      to: target,
      promotion: 'q'
    });

    if (move === null) return 'snapback';

    // Make random legal move for black
    if (mode === 'computer') {
      window.setTimeout(makeRandomMove, 250);
    }

    // Push the move to history
    moveCount++;
    if (game.turn() === 'w') {
      history.push(`${moveCount}. ${move.from}${move.to} `);
    } else {
      history.push(`${move.from}${move.to} `);
    }
    $history.text(history.join(' '));
  };

  var onSnapEnd = function () {
    board.position(game.fen());
  };

  const config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd,
  }

  board = Chessboard('board', config);

  $('p#local.button').on('click', () => {
    board.start();
    game = new Chess();
    mode = '1v1';
  })

  $('p#computer.button').on('click', () => {
    board.start();
    game = new Chess();
    mode = 'computer';
  })
})
