<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            Management.php is part of MetaDoc
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

abstract class Management
{
	/* simpleXML-object relevant for this Management */
	private $xml;

	/* the host sending the data, found from the cert/ dir *.owner */
	private $host;


	/* the entry in the XML-list this class shall handle. */
	private $entry_name;

	/* if any attributes with the top-class needs to be handled, it is
	 * stored in this array for later retrieval.
	 */
	private $top_attrs;

	public function __construct($xml, $host, $entry_name, $tak = null)
	{
		$this->xml		= $xml;
		$this->host		= $host;
		$this->entry_name	= $entry_name;
		$this->top_attrs	= array();
		if (isset($tak)) {
			foreach ($tak as $key) {
				$this->top_attrs[$key] = "". $this->xml[$key];
			}
		}
	}

	public function __tostring()
	{
		return $this->entry_name;
	}

	protected function get_host()
	{
		return $this->host;
	}

	/**
	 * get_top_attrs() return the array of all the attributes
	 *
	 * This is for elements such that
	 * <top_elem attr1="foo" attr2="bar">
	 *   <elem attr="foobar1" />
	 *   <elem attr="foobar2" />
	 *   <elem attr="foobar3" />
	 * </top_elem>
	 *
	 * The function will then return an array('foo', 'bar')
	 *
	 * @param void
	 * @return Array|null list of top attributes
	 * @access protected
	 */
	protected function get_top_attrs()
	{
		if (count($this->top_attrs) > 0)
			return $this->top_attrs;
		return null;
	}

	/**
	 * iterate() work through the xml-file and process each individual
	 * element.
	 *
	 * <top_elem>
	 *   <elem attr="foobar1" />
	 *   <elem attr="foobar2" />
	 *   <elem attr="foobar3" />
	 * </top_elem>
	 *
	 * It will pass each <elem .. /> to the subclass' handle_entry.
	 *
	 * @param  : none
	 * @return : none
	 */
	public function iterate()
	{
		if (is_null($this->entry_name)) {
			return;
		}
		$entries = $this->xml->$this;
		foreach ($entries as $e) {
			if (!$this->handle_entry($e)) {
				echo __FILE__ .":".__LINE__ ." ";
				echo "Errors whilst handling entry. ";
				echo "FIXME: add error-handling logic.\n";
			}
		}
	}

	/**
	 * handle_entry() handle single subelement in the Metadoc
	 *
	 * Each element found in iterate() will be sent to this function.
	 *
	 * @param SimpleXML_ELement $entry provided (subtree) part of the XML document.
	 * @return Boolean True if the element was successfully handled.
	 */
	protected abstract function handle_entry($entry);

}
?>