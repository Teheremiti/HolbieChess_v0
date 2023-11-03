<!DOCTYPE html>
<html><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holbie Friends</title></html>
    <link rel="stylesheet" type="text/css" href="../static/styles/header.css">
    <link rel="stylesheet" type="text/css" href="../static/styles/body.css">
    <link rel="stylesheet" type="text/css" href="../static/styles/friends.css">
    <link rel="stylesheet" type="text/css" href="../static/styles/footer.css">
</head>

<body>
    <header>
        <div class="homepage">
            <a href="./index.html">
                <div class="logo">
                    <img src="../img/holbielogo.png" alt="holbielogo">
                </div>
                <h1> Holbie Chess </h1>
            </a>
        </div>
        <div class="user">
            <div class="searchbar"></div>
            <div class="usericon">
              <!-- if not logged in -->
              <a href={{ url_for('register') }}><img src='../img/usericon.png' alt="usericon"></a>
              <!-- if logged in -->
              <!-- Display profile pic & redirect to user page on click  -->
            </div>
        </div>
    </header>

    <main></main>

    <footer>
        <p> Made by Teheremiti & Tristan </p>
    </footer>
</body>
</html>

