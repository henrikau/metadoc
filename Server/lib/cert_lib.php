<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            cert_lib.php is part of MetaDoc
 *
 * All of MetaDoc is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * MetaDoc is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with MetaDoc.  If not, see <http://www.gnu.org/licenses/>.
 *
 */


/**
 * getHostFromCert return the name of the host owning the certificate.
 *
 * @param String $cert the pem-encoded certificate
 * @return String|Null $owner the host (name) of the owner of the certifiate
 */
function getHostFromCert($cert)
{
	if (is_null($cert)) {
		return null;
	}
	$x509 = openssl_x509_parse($cert);
	if (is_null($x509)) {
		return null;
	}
	$hash = $x509['hash'];
	if (is_null($hash)) {
		return null;
	}
	$host = null;

	/* does the file exist in the cert-dir? */
	$path = dirname(dirname(__FILE__));
	$cert_path = $path . "/certs/" . $hash;
	if (!file_exists($cert_path)) {
		echo "Certificate with hash $hash does not exist in the cert-dir! Looking for $cert_path";
		return null;
	}

	if (!is_readable($cert_path)) {
		echo "Cannot read $cert_path. Aborting. Please fix.";
		return null;
	}

	/* compare cert with stored just to be sure */
	$stored = file_get_contents($cert_path);
	if (trim($cert) != trim($stored)) {
		echo "<p>\n";
		echo "Error: we have a name-collision. Two different certificates with matching hash.\n";
		echo "Stored certificate ($hash)\n";
		echo "$stored\n";

		echo "Provided by client ($hash)\n";
		echo "<pre>$cert</pre>\n";
		return null;
	}
	/* who owns this certificate? */
	$owner_file = $path . "/certs/" . $hash . ".owner";
	if (!file_exists($owner_file)) {
		echo "Owner not configured. Please add the name of the owner in $owner_file";
		return null;
	}
	if (!is_readable($owner_file)) {
		echo "Cannot read $owner_file. Please fix.";
		return null;
	}
	$fd = fopen($owner_file, "r");
	if (!$fd) {
		echo "Could not open $owner_file for reading.";
		return null;
	}

	/* for each line, strip away comments, last line-entry will be treated
	 * as a host. */
	while ($l = fgets($fd, 512)) {
		$line = trim($l);
		if (!strpos($line, "#")) {
			if ($line != ""){
				$host = $line;
			}
		}
	}
	fclose($fd);
	return $host;
} /* end getHostFromCert */

?>
