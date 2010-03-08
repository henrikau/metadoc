<?php
require_once '_include.php';
require_once 'asserts.php';
require_once 'cert_lib.php';
require_once 'logger.php';

/* make sure we run safely */
assertEnvironment();

/* get hostname for user (from certificate) */
$host = getHostFromCert($_SERVER['SSL_CLIENT_CERT'], $error);

if (is_null($host)) {
	header('Content-Type: text/plain');
	echo $error;
	exit(0);
} else {
	Logger::logEvent(LOG_NOTICE, "accepted client for $host from IP " .
			 $_SERVER['REMOTE_ADDR'] );

	/* parse input */
	if (isset($_POST['metadoc'])) {
		$fullUpdate = false;
		$xml = new SimpleXMLElement(stripslashes($_POST['metadoc']));

		/* verify version */
		$v = $xml['version'];
		if ($v != "1.0") {
			echo "Unsupported version ($v), 1.0 required, cannot continue.\n";
			exit(0);
		}

		/* detect full/partial update */
		switch(strtolower($xml['fullUpdate'])) {
		case "yes":
			$fullUpdate = true;
			break;
		case "no":
			break;
		default:
			echo "unknown fullUpdate value, aborting.\n";
			exit(0);
			break;
		}

		header('Content-Type: text/plain');
		if (isset($xml->users)) {
			require_once 'Users.php';
			$um = new Users($xml->users, $fullUpdate, $host);
			$um->iterate();
		}
		if (isset($xml->projects)) {
			require_once 'Projects.php';
			$pm = new Projects($xml->projects, $fullUpdate, $host);
			$pm->iterate();
		}

		if (isset($xml->allocations)) {
			require_once 'Allocations.php';
			$a = new Allocations($xml->allocations, $host);
			$a->iterate();
		}
		if (isset($xml->events)) {
			require_once 'Events.php';
			$eu = new EventsUp($xml->events, $host);
			$eu->iterate();
			$ed = new EventsDown($xml->events, $host);
			$ed->iterate();
		}
		if (isset($xml->siteInfo)) {
			require_once 'SiteInfo.php';
			$sw = new Software($xml->siteInfo, $host);
			$sw->iterate();
			$conf = new Software($xml->siteInfo, $host);
			$conf->iterate();
		}
	}
}

?>
