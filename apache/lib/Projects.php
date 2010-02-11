<?php
/**
 * PHP version 5.
 *
 * LICENSE: GPLv3
 *
 *            Projects.php is part of MetaDoc
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
 * Projects
 *
 * Class representing a set of projects to the site.
 *
 * Each site is host to one or more projects. This class decodes the
 * projects-part of the MetaDoc XML message and provides hooks where the
 * sysadmin can add logic for treating the requests.
 *
 * <MetaDoc version="1.0" fullUpdate="yes|no">
 *     <projects>
 *	   <project_entry name="foopro"
 *		       gid="1001"
 *		       status="new"
 *		       account_nmb="NN12345"
 *		       valid_from="2010-01-01"
 *		       valid_to="2020-01-01" />
 *     </projects>
 * </MetaDoc>
 *
 * @author Henrik Austad <henrik.austad@uninett.no>
 * @copyright 2009-2010 UNINETT Sigma A/S
 * @license http://www.gnu.org/licenses/gpl-3.0.txt
 */
class Projects extends Management
{
	private $fullUpdate;	/* if the hunk of data is to be considered as
				 * full update. */
	public function __construct($xml, $fu, $host)
	{
		parent::__construct($xml, $host, 'project_entry');
		$this->fullUpdate = $fu;
	}

	/**
	 * add() add a new Project
	 *
	 * This is a skeleton function and should be customized to the local
	 * site. It is used as an internal function and should not be called
	 * from the outside.
	 *
	 *
	 * @param String	$name:	the name of the project to go in
	 *				/etc/groups
	 * @param String	$gid:	the group-id provided centrally. If not
	 *				set, a gid should be assigned from the
	 *				local share of the pool
	 * @param String	$account_nmb:
	 *				The account-number provided by the
	 *				Resource Allocation Comittee
	 * @param String	$valid_from:
	 *				The project should not be accessible
	 *				*before* this date.
	 * @param String|null	$valid_to:
	 *				The project should not be accessible
	 *				*after* this date.
	 * @param Array|null	$users:	List of users associcated with the
	 *				project. This is typically the list of
	 *				people found at a project's entry in
	 *				/etc/groups
	 *
	 * @return Boolean true if the project was successfully added
	 * @access private
	 */
	private function add($name, $gid, $account_nmb, $valid_from, $valid_to, $users)
	{
		echo "add $name ($gid, $account_nmb, $valid_from, $valid_to)\n";
		if (isset($users)) {
			print_r($users);
		}
		Logger::logEvent(LOG_NOTICE, "Adding project $name, $gid, $account_nmb to system.");
		return true;
	}

	/**
	 * update() update an existing Project
	 *
	 * The method must retrieve infromation about the project from the
	 * system, compare the values and update where needed. Some basic
	 * sanitycheck should also be provided.
	 *
	 * @param String	$name:	the name of the project to go in
	 *				/etc/groups
	 * @param String	$gid:	the group-id provided centrally. If not
	 *				set, a gid should be assigned from the
	 *				local share of the pool
	 * @param String	$account_nmb:
	 *				The account-number provided by the
	 *				Resource Allocation Comittee
	 * @param String	$valid_from:
	 *				The project should not be accessible
	 *				*before* this date.
	 * @param String|null	$valid_to:
	 *				The project should not be accessible
	 *				*after* this date.
	 * @param Array|null	$users:	List of users associcated with the
	 *				project. This is typically the list of
	 *				people found at a project's entry in
	 *				/etc/groups
	 *
	 * @return Boolean true if the project was successfully updated.
	 * @access private
	 */
	private function update($name,
				$gid,
				$account_nmb,
				$valid_from,
				$valid_to,
				$users)
	{
		Logger::logEvent(LOG_NOTICE, "updating $name with new values.");
		echo "updating $name with new vals.";
		return true;
	}

	/**
	 * delete() remove a project completely from the system.
	 *
	 * This should remove all references to the project, including freeing
	 * space used by the project. Users only connected to this project
	 * should *not* be removed, removal-notice for users will be handled in
	 * Users.php.
	 *
	 * @param String $name		: Groupname as presented in /etc/groups
	 * @param String $account_nmb	: The account-number  as provided by
	 *				  RFK. This is in case the logs etc
	 * 				  needs it.
	 * @return Boolean true if Project was deleted without errors.
	 * @access private
	 */
	private function delete($name, $account_nmb)
	{
		echo "deleting $name - $account_nmb\n";
		Logger::logEvent(LOG_NOTICE, "Removed $name - $account_nmb from system.");
		return true;
	}


	/**
	 * @see Management::handle_entry()
	 */
	protected function handle_entry($entry)
	{
		$name		= htmlentities($entry['name']);
		$gid		= htmlentities($entry['gid']);
		$status		= htmlentities($entry['status']);
		$account_nmb	= htmlentities($entry['account_nmb']);
		$valid_from	= htmlentities($entry['valid_from']);
		$valid_to	= htmlentities($entry['valid_to']);

		/* any remarks? */
		$users = array();
		foreach ($entry->user_entry as $user) {
			$users[] = $user['username']."";
		}

		switch($status) {
		case 'new':
			return $this->add($name, $gid, $account_nmb, $valid_from, $valid_to, $users);
		case 'existing':
			return $this->update($name, $gid, $account_nmb, $valid_from, $valid_to, $users);
		case 'delete':
			return $this->delete($name, $account_nmb);
		default:
			echo "Unknown status: $status. Expected new|existing|delete.\n";
			break;
		}
		return false;
	} /* end handle_entry */
} /* end class Projects */