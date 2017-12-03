<?php
	//$x = var_dump(function_exists('mysqli_connect'));
	//echo $x;
	$table = 'nyse_2017_11_18_17_01';
	$con = mysqli_connect("localhost","test","Test123+", "hw9") or die("Unable to connect");
	//echo 'test2';
	if (mysqli_connect_errno()) {
	echo "Failed to connect to MySQL: " . mysqli_connect_error();
	}
	//echo 'test1';
	$query = "SELECT * from " . $table;
	$queryt = "INSERT INTO test VALUES(1)";
	$result = mysqli_query($con, $query) or die(mysql_error()); 
	echo "<table border='1'>
	<tr>
	<th>ListNum</th>
	<th>Company</th>
	<th>Volume</th>
	<th>Price</th>
	<th>Chng</th>
	<th>pChng</th>
	</tr>";
	while($row = mysqli_fetch_array($result)) {
	echo "<tr>";
	echo "<td>" . $row['ListNum'] . "</td>";
	echo "<td>" . $row['Company'] . "</td>";
	echo "<td>" . $row['Volume'] . "</td>";
	echo "<td>" . $row['Price'] . "</td>";
	echo "<td>" . $row['Chng'] . "</td>";
	echo "<td>" . $row['pChng'] . "</td>";
	echo "</tr>";
	}
	echo "</table>";

	mysqli_close($con);
?>

