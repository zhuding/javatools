/**
 * Created by jacky on 16/10/6.
 */
$(document).ready(function () {
	$('#db_name').on('change', function () {
		var db_name = $(this).val();
		window.location.href = "/dbtools?db_name=" + db_name;
	});
	$('#table_name').on('change', function () {
		var db_name = $('#db_name').val();
		var table_name = $(this).val();
		window.location.href = "/dbtools?db_name=" + db_name + "&table_name=" + table_name;
	});
	$('#changeTable').on('click', function () {
		var db_name = $('#db_name').val();
		var table_name = $('#table_name').val();
		var object_name = $('#object_name').val();
		if (db_name == '') {
			alert('Please choose db name.');
			$('#db_name').focus();
			return false;
		}
		if (table_name == '') {
			alert('Please choose table name.');
			$('#table_name').focus();
			return false;
		}
		if (object_name == '') {
			alert('Please input object name.');
			$('#object_name').focus();
			return false;
		}
		window.location.href = "/dbtools?db_name=" + db_name + "&table_name=" + table_name + "&object_name=" + object_name;

	});
});