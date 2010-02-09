<?php
define('WEB_DIR', dirname(__FILE__));
$path = ini_get('include_path');
$path = $path . PATH_SEPARATOR;
$path .= PATH_SEPARATOR . dirname(WEB_DIR) . '/';
$path .= PATH_SEPARATOR . dirname(WEB_DIR) . '/www';
$path .= PATH_SEPARATOR . dirname(WEB_DIR) . '/lib';
$path .= PATH_SEPARATOR . dirname(WEB_DIR) . '/certs';
ini_set('include_path', $path);
?>
