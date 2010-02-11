<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            SiteInfo.php is part of MetaDoc
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

require_once 'Management.php';
require_once 'logger.php';

/**
 * SiteInfo
 *
 * <MetaDoc version="1.0" fullUpdate="yes|no">
 *    <siteInfo name="foo_site">
 *        <software progName="gcc"
 *		    version="4.4.1"
 *		    license="GPL"
 *		    infoURL="http://www.example.org/" />
 *        <software progName="javac"
 *		    version="1.6.1" />
 *	  <config element="cores" metric="count" volume="2050" />
 *	  <config element="totalDisk" metric="TB" volume="76" />
 *    </siteInfo>
 * </MetaDoc>
 */
abstract class SiteInfo extends Management
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
			$this->valid = False;
		}
	}

	/**
	 * @see Management::handle_entry()
	 */
	protected function handle_entry($entry)
	{
		if (!$this->valid) {
			/* not valid host, do not match keypair, won't update host. */
			return false;
		}
		$attrs = array();
		$attributes = $entry->attributes();
		foreach ($attributes as $attr => $attr_value) {
			$attrs[$attr] = htmlentities($attr_value);
		}
		return $this->handle_si($attrs);
	}

	/**
	 * handle_si()
	 *
	 * Process a single event. Since the event can be of different types,
	 * subclasses must provide this.
	 *
	 * Process SiteInfo
	 *
	 * @param Array $val_arr array of values
	 *
	 * @return Boolean
	 * @access protected
	 */
	protected abstract function handle_si($val_arr);
}

final class Software extends SiteInfo
{

	public function __construct($xml, $host)
	{
		parent::__construct($xml, $host, 'software', array('name'));
	}

	/**
	 * @see SiteInfo::handle_si()
	 */
	protected function handle_si($val_arr)
	{
		print_r($val_arr);
		return true;
	}
} /* end Software */

final class Config extends SiteInfo
{
	public function __construct($xml, $host)
	{
		parent::__construct($xml, $host, 'software', array('name'));
	}

	/**
	 * @see SiteInfo::handle_si()
	 */
	protected function handle_si($val_arr)
	{
		print_r($val_arr);
		return true;
	}
} /* end Config */
