<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            logger.php is part of MetaDoc
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


/* Logger
 *
 * This logs to syslog. It is a refork of the logger found in Confusa. It only
 * logs to syslog, and is not configurable.
 *
 * @author Henrik Austad <henrik.austad@uninett.no>
 */
class Logger {
	/**
	 * Logger
	 *
	 * From php.net:
	 *
	 * syslog() Priorities (in descending order)
	 * Constant		Description
	 * LOG_EMERG		system is unusable
	 * LOG_ALERT		action must be taken immediately
	 * LOG_CRIT		critical conditions
	 * LOG_ERR		error conditions
	 * LOG_WARNING	warning conditions
	 * LOG_NOTICE	normal, but significant, condition
	 * LOG_INFO		informational message
	 * LOG_DEBUG		debug-level message
	 *
	 * @param Integer $pri the priority of the log-entry
	 * @param String $message the log msg.
	 *
	 * @return void
	 * @access static
	 */
	static function logEvent($pri, $message)
	{
		define_syslog_variables();
		openlog("Confusa: ", LOG_PID | LOG_PERROR, LOG_LOCAL0);
		syslog((int)$pri, $message);
		closelog();
	}
} /* end Logger */
