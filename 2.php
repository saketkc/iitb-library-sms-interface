<?php
$param1 = $_GET['param1'];
$param2 = $_GET['param2'];
$param3 = $_GET['param3'];
$param4 = $_GET['param4'];
$url = 'http://10.102.56.95/' . $param1 . '/' . $param2 . '/' . $param3;
if ( $param4 != '0')
{
	 $url .= '/' . $param4;
}
//echo $url;
//$url = "10.101.201.141:5000/grades/saket.kumar/thisisit1314./2";
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_GET, 1);
curl_setopt($ch, CURLOPT_GETFIELDS, "");
echo curl_exec ($ch);

curl_close ($ch);
?>
