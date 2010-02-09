<?php
require_once '_include.php';
require_once 'asserts.php';
require_once 'cert_lib.php';
require_once 'logger.php';

/* make sure we run safely */
assertEnvironment();

/* get hostname for user (from certificate) */
$host = getHostFromCert($_SERVER['SSL_CLIENT_CERT']);

if (is_null($host)) {
	header('Content-Type: text/plain');
	echo "Did not find a host for the provided certificate. Cannot continue.";
	exit(0);
} else {
	Logger::logEvent(LOG_NOTICE, "accepted client for $host from IP " .
			 $_SERVER['REMOTE_ADDR'] );

	/* parse input */
	if (isset($_POST['metadoc'])) {
		header('Content-Type: text/xml');
		$xml = stripslashes($_POST['metadoc']);
		$xmlparser = new SimpleXMLElement($xml);
		print_r($xmlparser);
	}
}

?>
