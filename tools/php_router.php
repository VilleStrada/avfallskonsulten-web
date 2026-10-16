<?php
// Router för PHP:s inbyggda server, härmar .htaccess (rena adresser + 404) vid lokalt test:
//   php -S localhost:8765 -t docs tools/php_router.php
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$rot = __DIR__ . '/../docs';
if ($path !== '/' && file_exists($rot . $path)) {
    return false;                       // riktig fil (bild, css, php) serveras som den är
}
$fil = $rot . rtrim($path, '/') . '.html';
if ($path === '/' || $path === '') { $fil = $rot . '/index.html'; }
if (file_exists($fil)) {
    header('Content-Type: text/html; charset=utf-8');
    readfile($fil);
} else {
    http_response_code(404);
    readfile($rot . '/404.html');
}
