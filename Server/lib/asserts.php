<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            asserts.php is part of MetaDoc
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

require_once 'logger.php';
/**
 * assertEnvironment() make sure that we are operating safely
 *
 * Assert that we are on SSL and on appropriate level before continuing. If any
 * of the requirements are not met, we abort and close the connection.
 *
 * @param void
 * @return void
 */
function assertEnvironment()
{
	global $log_error_code;
	/*
	 * are we on SSL
	 */
	if (is_null($_SERVER['HTTPS'])) {
		Logger::logEvent(LOG_NOTICE,
				  "[RI] ($log_error_code) Environment-variable 'HTTP' not available.");
		exit(0);
	}
	if (strtolower($_SERVER['HTTPS']) != 'on') {
		Logger::logEvent(LOG_NOTICE,
				  "[RI] ($log_error_code) Server is not running on SSL. Blocking robot-connections.");
		exit(0);
	}

	/*
	 * do we have a client certificate?
	 */
	if (is_null($_SERVER['SSL_CLIENT_CERT'])) {
		Logger::logEvent(LOG_NOTICE,
				  "[RI] ($log_error_code) Environment-variable 'SSL_CLIENT_CERT' not available.");
		exit(0);
	}
	$cert = $_SERVER['SSL_CLIENT_CERT'];
	if (!isset($cert) || $cert == "") {
		Logger::logEvent(LOG_NOTICE, "[RI] ($log_error_code) Connection from client (".
				  $_SERVER['REMOTE_ADDR'].
				  ") without certificate. Dropping connection. Make sure apache is configured with SSLVerifyClient optional_no_ca");
		exit(0);
	}

	/*
	 * Is the certificate properly constructed (can Apache find the DN)?
	 */
	if (is_null($_SERVER['SSL_CLIENT_I_DN'])) {
		Logger::logEvent(LOG_NOTICE, "Malformed certificate from " . $_SERVER['REMOTE_ADDR'] . ". Aborting.");
		exit(0);
	}

} /* end assertEnvironment() */
?>