document.addEventListener("DOMContentLoaded", () => {
  var board;
  var game = new Chess();
  var mode = 'computer';
  var isGameOver = false;
  var moveCount = 0;

  var $history = $('.history');
  var history = [];

  function write_to_json(last_move) {
    try {
      const jsonData = JSON.stringify(last_move);
      console.log(jsonData);
      localStorage.setItem('last_move.json', jsonData);
    } catch (err) {
      console.error(err);
      throw err;
    }
  }

  function makeHolbieMove () {
    try {
      const fileContent = localStorage.getItem('last_move.json');
      const parsedData = JSON.parse(fileContent);
      console.log(parsedData);
    } catch (err) {
      console.error(err);
      throw err;
    }
  }

  function makeRandomMove () {
    var possibleMoves = game.moves();

    // Game over
    if (possibleMoves.length === 0) {
      isGameOver = true;
      return;
    }

    // Play a random legal move for black and update the board position
    var randomIdx = Math.floor(Math.random() * possibleMoves.length);
    var move = possibleMoves[randomIdx]
    game.move(move);

    // Push move to history
    history.push(move);
    $history.text(history.join(' '))
    board.position(game.fen());

    // Send move to JSON
    write_to_json(move);
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

  function pieceTheme (piece) {
    return '/img/' + piece + '.svg'
  }

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

    // Write move to JSON file in localStorage
    write_to_json(move.san);

    // Make random legal move for black
    if (mode === 'computer') {
      window.setTimeout(makeRandomMove, 250);
    }

    // Push the move to history
    if (game.turn() === 'b') {
      moveCount++;
      history.push(`${moveCount}. ${move.san} `);
    } else {
      history.push(`${move.san} `);
    }
    $history.text(history.join(' '));
  };

  var onSnapEnd = function () {
    board.position(game.fen());
  };

  const config = {
    pieceTheme: pieceTheme,
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd,
  }

  board = Chessboard('board', config);

  $('button.local').on('click', () => {
    board.start();
    game = new Chess();
    history = [];
    $history.text("");
    moveCount = 0;
    mode = '1v1';
  })

  $('button.computer').on('click', () => {
    board.start();
    game = new Chess();
    history = [];
    $history.text("");
    moveCount = 0;
    mode = 'computer';
  })

  /*$('button.previous').on('click', () => {

  })

  $('button.next').on('click', () => {

  })*/
})
