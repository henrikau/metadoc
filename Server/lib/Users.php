<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            Users.php is part of MetaDoc
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
 * class Users
 *
 * Handle entries in the MetaDoc of the type:
 * <MetaDoc version="1.0" fullUpdate="yes|no">
 *     <users>
 *	   <user_entry username="foo"
 *		       uid="1001"
 *		       full_name="Foo Bar"
 *		       password="t3mpW0rd"
 *		       default_grups="users"
 *		       special_path="/home/special/"
 *		       shell="/bin/zsh"
 *		       email="foo@example.org"
 *		       phone="555-12345"
 *		       status="new" />
 *     </users>
 * </MetaDoc>
 *
 * See MetaDoc.dtd for the complete reference.
 *
 * @author Henrik Austad <henrik.austad@uninett.no>
 * @license GPLv3 http://www.gnu.org/licenses/gpl-3.0.txt
 */
class Users extends Management
{
	private $fullUpdate;	/* if the hunk of data is to be considered as
				 * full update or partial. */

	public function __construct($xml, $fu, $host)
	{
		parent::__construct($xml, $host, 'user_entry');
		$this->fullUpdate = $fu;
	}

	/*Customize these 3 functions to add/modify/remove users on your system.
	 */

	/**
	 * add()	Add a new user to the system
	 *
	 * @param String $username	username to use on the system (provided
	 *				to coordinate common username on all
	 *				national systems).
	 * @param String $uid		Needs to be coordinated on a national
	 *				level.
	 * @param String $full_name
	 * @param String $pw		Initial password
	 * @param String $dg		Default group the user should belong to
	 * @param String $sp		Special path (if the user should get $HOME
	 *				elsewhere than in /home)
	 * @param String $shell
	 * @param String $email
	 * @param String $phone
	 *
	 * @return Boolean True		if the user was inserted without errors.
	 * @access private
	 */
	private function add($username, $uid, $full_name, $pw,
			     $dg, $sp, $shell, $email, $phone)
	{
		if (empty($username)	||
		    empty($uid)		||
		    empty($full_name)	||
		    empty($pw)		||
		    empty($dg)		||
		    empty($sp)		||
		    empty($shell)	||
		    empty($email)	||
		    empty($phone)) {
			echo "Error with supplied arguments. Need all parameters when adding a new user.\n";
			return false;
		}
		echo "adding $username, $uid, $full_name, $pw, $dg, $sp, $shell, $email, $phone\n";
		Logger::logEvent(LOG_NOTICE, "added user $username, $full_name, $uid to system.");
		return true;
	}

	/**
	 * update()	Update an existing user.
	 *
	 * @param String $username
	 * @param String $uid
	 * @param String $full_name
	 * @param String $pw
	 * @param String $dg
	 * @param String $sp
	 * @param String $shell
	 * @param String $email
	 * @param String $phone
	 *
	 * @return Boolean True		if the user was updated without errors.
	 * @access private
	 */
	private function update($username, $uid, $full_name, $pw,
				$dg, $sp, $shell, $email, $phone)
	{
		echo "updating $username, $uid, $full_name, $pw, $dg, $sp, $shell, $email, $phone\n";
		Logger::logEvent(LOG_NOTICE, "Updated $username with new values.");
		return true;
	}

	/**
	 * del()	Delete a user from the system.
	 *
	 * @param String $username
	 *
	 * @return Boolean True		if the user was removed without errors.
	 * @access private
	 */
	private function del($username)
	{
		echo "removing user $username from system.\n";
		Logger::logEvent(LOG_NOTICE, "Removed $username from system.");
		return true;
	}


	/**
	 * @see Management::handle_entry()
	 */
	protected function handle_entry($entry)
	{
		$attributes = $entry->attributes();
		$attrs = array();
		foreach ($attributes as $attr => $attr_value) {
			$attrs[$attr] = htmlentities($attr_value);
		}
		$username = "";
		if (array_key_exists('username', $attrs)) {
			$username = $attrs['username'];
		} else {
			/* username is REQUIRED for all types of user_entry */
			return false;
		}
		$full_name = "";
		if (array_key_exists('full_name', $attrs)) {
			$full_name = $attrs['full_name'];
		}
		$uid = "";
		if (array_key_exists('uid', $attrs)) {
			$uid = $attrs['uid'];
		}
		$status	= "existing";
		if (array_key_exists('status', $attrs)) {
			$status = $attrs['status'];
		}

		$pw	= "";
		if (array_key_exists('password', $attrs)) {
			$pw = $attrs['password'];
		}

		$dg	= "";
		if (array_key_exists('default_group', $attrs)) {
			$dg = $attrs['default_group'];
		}

		$sp	= "";
		if (array_key_exists('special_path', $attrs)) {
			$sp = $attrs['special_path'];
		}

		$shell	= "";
		if (array_key_exists('shell', $attrs)) {
			$shell = $attrs['shell'];
		}

		$email	= "";
		if (array_key_exists('email', $attrs)) {
			$email = $attrs['email'];
		}

		$phone	= "";
		if (array_key_exists('phone', $attrs)) {
			$phone = $attrs['phone'];
		}
		switch ($status) {
		case 'new':
			return $this->add($username, $uid, $full_name, $pw,
					  $dg, $sp, $shell, $email, $phone);
			break;
		case 'existing':
			return $this->update($username, $uid, $full_name, $pw,
					     $dg, $sp, $shell, $email, $phone);
			break;
		case 'delete':
			return $this->del($username);
			break;
		default:
			break;
		}
		return false;
	} /* end handle_entry */
} /* end Users */
?>