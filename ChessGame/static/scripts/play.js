document.addEventListener("DOMContentLoaded", () => {
  var board;
  var game = new Chess();
  var mode = new URLSearchParams(window.location.search).get('mode');
  var $history = $('.history');

  function isGameOver() {
    return game.in_checkmate() || game.in_draw() || game.in_stalemate() ||
           game.in_threefold_repetition() || game.insufficient_material();
  }

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
    write_to_json(game.fen());
    try {
      const game_fen = localStorage.getItem('game_fen.json');
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
        console.log('-----------------')
        game.move(move);
        board.position(game.fen());

        // Push move to history
        $history.html(`<p><strong>Moves log:</strong><br>${game.pgn()}</p>`);

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
    if (isGameOver() ||
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
    console.log(`User move: ${move.san}`);

    // Make IA move
    if (mode === 'computer' && !isGameOver()) {
      window.setTimeout(makeHolbieMove, 250);
    }

    // Push the move to history
    $history.html(`<p><strong>Moves log:</strong><br>${game.pgn()}</p>`);
  };

  var onSnapEnd = function () {
    board.position(game.fen());
    if (mode === '1v1' && !isGameOver()) {
      board.flip();
    }
  };

  const config = {
    // Set the orientation randomly if playing against computer
    orientation: mode === '1v1' ? 'white' : Math.random() > 0.5 ? 'white' : 'black',
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
  if (board.orientation() === 'black') {
    window.setTimeout(makeHolbieMove, 250);
  }

  $('button.local').on('click', () => {
    window.location.replace('/play.html?mode=1v1');
  })

  $('button.computer').on('click', () => {
    window.location.replace('./play.html?mode=computer');
  })

  var last_moves = [];
  $('button.previous').on('click', () => {
    last_moves.push(game.undo().san);
    board.position(game.fen());
  })

  $('button.next').on('click', () => {
    game.move(last_moves.pop());
    board.position(game.fen());
    // If we go back before the IA makes a move, when we come back the move is
    // not made and the position is blocked.
  })

  $('button.restart').on('click', () => {
    game.reset();
    board.start();
    $history.html('');
    if (mode === '1v1') {
      board.orientation('white');
    }
  })

  /*window.addEventListener('resize', () => {
    board.resize();
  })*/
})
