document.addEventListener("DOMContentLoaded", () => {
  var board;
  var game = new Chess();
  var mode = new URLSearchParams(window.location.search).get('mode');
  var $history = $('.history');
  var $congratulations = $('.congratulations');

  function isGameOver() {
    return game.in_checkmate() || game.in_draw() || game.in_stalemate() ||
           game.in_threefold_repetition() || game.insufficient_material();
  }

  function write_to_json(game) {
    try {
      const jsonData = JSON.stringify(game);
      localStorage.setItem('game.json', jsonData);
    } catch (err) {
      console.error(err);
      throw err;
    }
  }

  function makeHolbieMove () {
    write_to_json(game.fen());
    try {
      const game_fen = localStorage.getItem('game.json');
      fetch('/IAMove', {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        body: game_fen
      })
      .then(response => response.json())
      .then(move => {
        //console.log('Response from IA: ', move);
        //console.log('-----------------');
        game.move(move);
        board.position(game.fen());

        $history.html(`<p><strong>Moves log:</strong><br>${game.pgn()}</p>`);

        write_to_json(move);

        if (isGameOver()) {
          $congratulations.html(`${game.turn() === 'w' ? 'Black' : 'White'} won :/<br>
                                 Better luck next time`);
        }
      })
      .catch(err => {
        console.error('Error communicating with chess IA:', err);
      })
    } catch (err) {
      console.error(err);
      throw err;
    }
  }

  function loadDailyPuzzle () {
    axios.get('https://lichess.org/api/puzzle/daily')
      .then(response => {
        const dailyPuzzle = { "pgn": response.data.game.pgn, "solution": response.data.puzzle.solution };
        write_to_json(dailyPuzzle.solution);
        const jsonData = localStorage.getItem('game.json');
        console.log('writing to json....', jsonData);

        const game_pgn = dailyPuzzle.pgn.split(' ');
        const last_move = game_pgn.pop();
        game.load_pgn(game_pgn.join());
        board = Chessboard('board', {
          position: game.fen(),
          orientation: game.turn() === 'b' ? 'white' : 'black',
          pieceTheme: pieceTheme,
          draggable: true,
          onDragStart: onDragStart,
          onDrop: onDrop,
          onMouseoutSquare: onMouseoutSquare,
          onMouseoverSquare: onMouseoverSquare,
          onSnapEnd: onSnapEnd,
        });

        game.move(last_move);
        board.position(game.fen());
        $history.html(`<p><strong>Moves log:</strong><br>${game.pgn()}</p>`);
      })
      .catch(err => console.error(err))
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
    const gameTurn = game.turn() === 'w' ? 'white' : 'black'; 
    if (gameTurn === board.orientation()) {
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
  }

  function onMouseoutSquare (square, piece) {
    removeGreySquares()
  }

  function onDragStart (source, piece, position, orientation) {
    const whiteDraggableOnly = piece.search(/^w/) !== -1;
    const blackDraggableOnly = piece.search(/^b/) !== -1;

    if (mode === 'puzzle') {
      if ((isGameOver() ||
          (orientation === 'white' && blackDraggableOnly) ||
          (orientation === 'black' && whiteDraggableOnly))) {
            return false;
          }
    } else {
      if (isGameOver() ||
          (game.turn() === 'w' && blackDraggableOnly) ||
          (game.turn() === 'b' && whiteDraggableOnly)) {
            return false;
      }
    }
  }

  var onDrop = function (source, target) {
    removeGreySquares();
    var move;
    if (mode === 'puzzle' && `${source}${target}` !== dailySolution[0]) {
      move = null;
    } else {
      move = game.move({
        from: source,
        to: target,
        promotion: 'q'
      });
    }
    if (move === null) return 'snapback';

    //console.log(`User move: ${move.san}`);

    if (mode === 'computer' && !isGameOver()) {
      makeHolbieMove();
    } else if (mode === 'puzzle' && !isGameOver()) {
      if (dailySolution.length > 1) dailySolution.shift();
      if (dailySolution.length > 1) {
        const nextMove = dailySolution.shift();
        const squares = {
          from: nextMove.substr(0, 2),
          to: nextMove.substr(2, 3),
        }
        game.move(squares);
      } else {
        $congratulations.html('<p>Great job! Come back tomorrow</br>or visit\
                               <a href="https://lichess.org/training/daily" target="_blank">Lichess.org</a> for more problems');
      }
    }

    $history.html(`<p><strong>Moves log:</strong><br>${game.pgn()}</p>`);
  };

  var onSnapEnd = function () {
    board.position(game.fen());
    if (mode === '1v1' && !isGameOver()) {
      board.flip();
    }
    if (isGameOver() && (mode !== 'puzzle')) {
      $congratulations.text(`${game.turn() === 'w' ? 'Black' : 'White'} won !`);
    }
  };

//==============================================================================
  if (mode === 'puzzle') {
    // The following code doesn't wait for loadDailyPuzzle() to finish
    // --> if game.json was not empty, the jsonData will be its previous content
    loadDailyPuzzle();
    const jsonData = localStorage.getItem('game.json');
    console.log('afterLoad', jsonData);
    var dailySolution = JSON.parse(jsonData);

    $('.restartBtn').html('');
    $('.disclaimer').html('* Daily puzzles are powered by the <a href="https://lichess.org/api" target="_blank">Lichess.org API</a>\
      We do not claim any type of ownership over their content.');
  } else {
    const randomOrientation = Math.random() > 0.5 ? 'white' : 'black';
    const config = {
      orientation: mode === 'computer' ? randomOrientation : 'white',
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
      makeHolbieMove();
    }
  }

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
    $congratulations.text('');
  })

  /*window.addEventListener('resize', () => {
    board.resize();
  })*/
})
