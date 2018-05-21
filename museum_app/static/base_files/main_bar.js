<script type="text/javascript">
function myfunc(ul) {
	var className = ul.getAttribute("class");
	if(className=="nav-item") {
		ul.className += " active";
	} else {
		ul.className = "nav-item";
	}
}