<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            Events.php is part of MetaDoc
 *
 * All of MetaDoc is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option) any
 * later version.
 *
 * MetaDoc is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 * A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * MetaDoc.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

require_once 'Management.php';
require_once 'logger.php';

/**
 * class Event
 *
 * Handle entries for events, on the form:
 * <MetaDoc version="1.0" fullUpdate="yes|no">
 *   <events name="site">
 *     <resourceDown reason="run out of jet-fuel"
 *		     dateDown="2010-01-01"
 *		     dateUp="2010-01-03"
 *		     shareDown="100">
 *     <resourceUp reason="found free fuel"
 *		   dateUp="2010-01-03">
 *   </events>
 * </MetaDoc>
 * See MetaDoc.dtd for the complete reference.
 *
 * @author Henrik Austad <henrik.austad@uninett.no>
 * @license GPLv3 http://www.gnu.org/licenses/gpl-3.0.txt
 */
abstract class Events extends Management
{
	protected $valid;
	public function __construct($xml, $host, $name, $tak)
	{
		parent::__construct($xml, $host, $name, $tak);
		$this->valid = True;

		/* match host to xml-host */
		$xmlhost = $this->get_top_attrs();
		$xmlhost = $xmlhost['name'];
		if ($this->get_host() != $xmlhost) {
			echo "Host in xml does not match owner of certificate, ".
				"this entry is not valid.\n";
			$this->valid = False;
		}
	}

	/**
	 * @see Management::handle_entry()
	 */
	protected function handle_entry($entry)
	{
		if (!$this->valid) {
			/* not valid host, do not match keypair, won't update
			 * host. */
			echo "host not valid, aborting\n";
			return false;
		}

		$attrs = array();
		$attributes = $entry->attributes();
		foreach ($attributes as $attr => $attr_value) {
			$attrs[$attr] = htmlentities($attr_value);
		}

		$reason = null;
		if (array_key_exists('reason', $attrs)) {
			$reason		= $attrs['reason'];
		}
		$date_down = null;
		if (array_key_exists('dateDown', $attrs)) {
			$date_down	= $attrs['dateDown'];
		}
		$date_up = null;
		if (array_key_exists('dateUp', $attrs)) {
			$date_up	= $attrs['dateUp'];
		}
		$share_down = null;
		if (array_key_exists('shareDown', $attrs)) {
			$share_down	= $attrs['shareDown'];
		}

		/* any remarks? */
		$remarks = null;
		if (isset($entry->remarks)) {
			$remarks = htmlentities($entry->remarks);
		}
		return $this->handle_event($reason,
					   $date_down,
					   $date_up,
					   $share_down,
					   $remarks);
	}

	/**
	 * handle_event()
	 *
	 * Process a single Event from a site.
	 *
	 * @param String $reason for the event
	 * @param String $date_down RCF3339 compliant date format
	 * @param String $date_up RCF3339 compliant date format
	 * @param String $share_down share of system affected [0,100]
	 * @param String $remarks Any extra info needed.
	 *
	 * @return Boolean true if event was handled successfully.
	 * @access protected
	 */
	protected abstract function handle_event($reason, $date_down,
						 $date_up, $share_down, $remarks);
}

/**
 * class EventsDown
 *
 * Handle down-events, when a system is going down for (un)scheduled
 * maintenance.
 */
final class EventsDown extends Events
{
	public function __construct($xml, $host)
	{
		parent::__construct($xml, $host, 'resourceDown', array('name'));
	}

	/**
	 * @see Events::handle_entry()
	 */
	protected function handle_event($reason, $date_down,
					$date_up, $share_down, $remarks)
	{
		echo "Events (down) entry: \n";
		echo "reason:\t\t$reason\n";
		echo "Down:\t\t$date_down\n";
		echo "Up:\t\t$date_up\n";
		echo "share:\t\t$share_down\n";
		echo "Host:\t\t".$this->get_host() . "\n";
		if (!is_null($remarks)) {
			echo "remarks: $remarks\n";
		}
		echo "\n";
		Logger::logEvent(LOG_NOTICE, "processed resourceDown-event for ".
				 $this->get_host());
		return true;
	}
}

/**
 * class EventsUp
 *
 * If a system comes back up before the schedule, this handles that message.
 */
final class EventsUp extends Events
{
	public function __construct($xml, $host)
	{
		parent::__construct($xml, $host, 'resourceUp', array('name'));
	}

	/**
	 * @see Events::handle_entry()
	 */
	protected function handle_event($reason, $date_down,
					$date_up, $share_down, $remarks)
	{
		echo "Events (up) entry: \n";
		echo "Up:\t\t$date_up\n";
		echo "reason:\t\t$reason\n";
		if (!is_null($remarks)) {
			echo "remarks: $remarks\n";
		}
		echo "\n";
		Logger::logEvent(LOG_NOTICE, "processed resourceUp-event for ".
				 $this->get_host());
		return true;
	}
}

?>
