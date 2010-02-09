<?php
/* Logger
 *
 * This logs to syslog. It is a refork of the logger found in Confusa. It only
 * logs to syslog.
 *
 * Henrik Austad, June 2008, Uninett Sigma A/S
 * Henrik Austad, Feb. 2010, Uninett Sigma A/S
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
	 */
	static function logEvent($pri, $message)
          {
               define_syslog_variables();

		/* add this after the pri-test, as we don't want to  */
	       openlog("Confusa: ", LOG_PID | LOG_PERROR, LOG_LOCAL0);
	       syslog((int)$pri, $message);
	       closelog();
	  }
} /* end Logger */
