<?php
/**
 * Tar emot bokningsformuläret och mejlar det till info@avfallskonsulten.se.
 *
 * Lyckad sändning  -> 303 till /tack
 * Fel i fälten     -> 303 tillbaka till sidan med ?fel=1#boka
 * Spamrobot        -> låtsas lyckas (303 till /tack) utan att skicka
 *
 * Testläge (ingen e-post skickas, meddelandet sparas i includes/utkorg/ i stället):
 *   - sajten körs på localhost/127.0.0.1, eller
 *   - filen includes/testlage.txt finns (ta bort den på webbhotellet!)
 * Lokalt test kräver PHP:  php -S localhost:8765 -t docs tools/php_router.php
 */
declare(strict_types=1);

const MOTTAGARE = 'info@avfallskonsulten.se';
const AVSANDARE = 'noreply@avfallskonsulten.se';   // måste vara en adress på egna domänen för att Loopia ska skicka

function tillbaka(string $dit): never {
    header('Location: ' . $dit, true, 303);
    exit;
}
function falt(string $namn): string {
    return trim((string)($_POST[$namn] ?? ''));
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    tillbaka('/');
}

$referer = (string)($_SERVER['HTTP_REFERER'] ?? '');
$tillbakaSida = parse_url($referer, PHP_URL_PATH) ?: '/';
$tillbakaSida = preg_replace('~[^a-zA-Z0-9_/\-]~', '', $tillbakaSida) ?: '/';

// Honungsfälla: fältet "webbplats" är dolt för människor
if (falt('webbplats') !== '') {
    tillbaka('/tack');
}
// Formulär som skickas snabbare än 3 sekunder efter att sidan laddades är nästan alltid robotar
$t = (int)falt('t');
if ($t > 0 && (time() * 1000 - $t) < 3000) {
    tillbaka('/tack');
}

$tjanster = [
    'grovavfall' => 'Hämtning av grovavfall och grovsopor',
    'atervinning' => 'Hämtning av återvinning (löpande)',
    'byggavfall' => 'Bygg- och trädgårdsavfall',
    'bortforsling' => 'Bortforsling av möbler och skräp',
    'karltvatt' => 'Kärltvätt',
    'soprum' => 'Renovering av soprum',
    'radgivning' => 'Rådgivning',
    'annat' => 'Annat',
];

$tjanst = $tjanster[falt('tjanst')] ?? '';
$adress = falt('adress');
$lagenheter = falt('lagenheter');
$namn = falt('namn');
$telefon = falt('telefon');
$epost = falt('epost');
$meddelande = falt('meddelande');

$ok = $tjanst !== '' && $adress !== '' && $namn !== '' && $telefon !== ''
    && filter_var($epost, FILTER_VALIDATE_EMAIL) !== false
    && $lagenheter !== '' && ctype_digit($lagenheter)
    && falt('samtycke') !== ''
    && strlen($meddelande) < 5000;

if (!$ok) {
    tillbaka($tillbakaSida . '?fel=1#boka');
}

$rader = [
    "Ny förfrågan från avfallskonsulten.se",
    "",
    "Tjänst:           $tjanst",
    "Adress:           $adress",
    "Antal lägenheter: $lagenheter",
    "Namn:             $namn",
    "Telefon:          $telefon",
    "E-post:           $epost",
    "",
    "Meddelande:",
    $meddelande !== '' ? $meddelande : '(inget)',
    "",
    "Skickat: " . date('Y-m-d H:i') . "  från sida: $tillbakaSida",
];
$text = implode("\n", $rader);
$amne = "Bokningsförfrågan: $tjanst, $namn";

$testlage = in_array($_SERVER['SERVER_NAME'] ?? '', ['localhost', '127.0.0.1'], true)
    || file_exists(__DIR__ . '/testlage.txt');

if ($testlage) {
    $mapp = __DIR__ . '/utkorg';
    if (!is_dir($mapp)) { mkdir($mapp, 0755, true); }
    file_put_contents($mapp . '/' . date('Ymd-His') . '.txt', "Till: " . MOTTAGARE . "\nÄmne: $amne\n\n$text\n");
    tillbaka('/tack');
}

$headers = [
    'From: Avfallskonsulten webb <' . AVSANDARE . '>',
    'Reply-To: ' . $namn . ' <' . $epost . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
];
$skickat = mail(
    MOTTAGARE,
    mb_encode_mimeheader($amne, 'UTF-8'),
    $text,
    implode("\r\n", $headers)
);

tillbaka($skickat ? '/tack' : $tillbakaSida . '?fel=2#boka');
