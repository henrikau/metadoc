<?php
require_once 'Management.php';
require_once 'logger.php';

/**
 * Allocations
 *
 * This class represents the allocations a project will receive for the
 * different periods, and of the class.
 *
 * It expects XML-structures on the following format:
 * <allocations>
 *   <all_entry account_nmb="NN12345" hours="1000" all_class="pri" period="2010.1" />
 *   <all_entry account_nmb="NN12345" hours="2000" all_class="nonpri" period="2010.1" />
 * </allocations>
 */
class Allocations extends Management
{
	public function __construct($xml, $host)
	{
		parent::__construct($xml, $host, 'all_entry');
	}

	/**
	 * @see Management::handle_entry()
	 */
	protected function handle_entry($entry)
	{
		$account_nmb	= htmlentities($entry['account_nmb']);
		$hours		= htmlentities($entry['hours']);
		$all_class	= strtolower(htmlentities($entry['all_class']));
		if (!($all_class == 'pri' || $all_class == 'nonpri')) {
			echo "Not legal class $all_class. Expected one of pri|nonpri.\n";
			return false;
		}
		$period		= htmlentities($entry['period']);
		Logger::logEvent(LOG_NOTICE,
				  "Adding new allocation for $account_nmb: $hours cpu-hours of class $all_class");
		echo "$account_nmb: $hours $all_class $period\n";
		return true;
	}
}
?>