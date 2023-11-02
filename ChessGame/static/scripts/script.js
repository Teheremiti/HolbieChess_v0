document.addEventListener("DOMContentLoaded", () => {
  var board;
  var game = new Chess();
  var mode = 'computer';
  var isGameOver = false;
  var moveCount = 0;

  var $history = $('.history');
  var history = [];

  function write_to_json(game_fen) {
    try {
      const jsonData = JSON.stringify(game_fen);
      localStorage.setItem('game_fen.json', jsonData);
    } catch (err) {
      console.error(err);
      throw err;
    }
  }

  function makeHolbieMove () {
    try {
      const game_fen = localStorage.getItem('game_fen.json');
      console.log('Communicating with IA...')
      fetch('/IAMove', {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        body: game_fen
      })
      .then(response => response.json())
      .then(move => {
        console.log('Response from IA: ', move);
        game.move(move);
        board.position(game.fen());

        // Push move to history and update board position
        history.push(move);
        $history.text(history.join(' '));

        // Send move to JSON
        write_to_json(move);
      })
      .catch(err => {
        console.error('Error communicating with chess IA:', err);
      })
    } catch (err) {
      console.error(err);
      throw err;
    }
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

    // Make IA move
    if (mode === 'computer') {
      window.setTimeout(makeHolbieMove, 250);
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
    write_to_json(game.fen());

    if (mode === '1v1') {
      board.flip();
    }
  };

  board = Chessboard('board', {
    pieceTheme: pieceTheme,
    position: 'start',
    draggable: false
  });

  function restartGame () {
    board.destroy();
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
    game = new Chess();
    history = [];
    $history.text("");
    moveCount = 0;
  }

  $('button.local').on('click', () => {
    restartGame();
    mode = '1v1';
  })

  $('button.computer').on('click', () => {
    restartGame();
    mode = 'computer';
  })

  /*$('button.previous').on('click', () => {

  })

  $('button.next').on('click', () => {

  })*/
})
