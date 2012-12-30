<?php

    /*** make it or break it ***/
    error_reporting(E_ALL);

    try
    {
        /*** open the database file ***/
        $dbh = new PDO("sqlite:pbxcollect.db");

        /*** set all errors to excptions ***/
        $dbh->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        /*** run the query ***/
        //$dbh->query("SELECT * FROM calls");

        $sql = "SELECT * FROM calls ORDER BY cyear, cmonth, cday, ctime";
        echo "<table>";
        foreach ($dbh->query($sql) as $arry)
           {
           echo "<tr>";
           echo "<td align='right'>" . $arry['cday'] . "." . $arry['cmonth'] . "." . $arry['cyear'] . "</td>";
           echo "<td>" . $arry['ctime'] . "</td>";
           echo "<td>" . $arry['intline'] . "</td>";
           echo "<td>" . $arry['coline'] . "</td>";
           echo "<td>" . $arry['phonenum'] . "</td>";
           echo "<td align='right'>" . $arry['colduration'] . "</td>";
           echo "</tr>";
           }
        echo "</table>";

       // close the database connection
       $dbn = NULL;
    }

    catch(PDOException $e)
    {
        echo $e->getMessage();
    }

?>
