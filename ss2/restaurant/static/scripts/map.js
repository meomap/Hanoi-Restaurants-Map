/**
 * Hanoi Restaurants Map
 * 
 * This application is for study purpose only.
 * Map interaction library: Leaflet. API at http://leaflet.cloudmade.com/reference.html
 * Base map: OpenStreetMap. More at http://www.openstreetmap.org
 *  
 * @author La Son Hai <shnt1221@gmail.com>
 * @version 1.0
 * @date 30.05.2012
 */

// custom categories - icons
var cat_image = {
		"ASIAN":"restaurant_red.png",
		"MIDDLE EASTERN":"cafetaria_red.png", "SINGAPOREAN":"restaurant_red.png",
		"SEAFOOD":"restaurant_thai.png", "KOREAN":"kebab.png",
		"THAI":"fishchips.png", "CZECH":"restaurant.png", 
		"SPANISH":"restaurant_breakfast.png", "PIZZA": "pizzaria.png",
		"VIETNAMESE":"restaurant_chinese.png", "CHINESE":"restaurant_korean.png",
		"MALAYSIAN":"restaurant_fish.png","INDIAN":"restaurant_indian.png",
		"JAPANESE":"japanese-food.png","MEXICAN":"restaurant_mexican.png",
		"MODERN EUROPEAN":"cafetaria.png","BRAZILIAN":"restaurant_african.png",
		"FRENCH":"restaurant_romantic.png","STEAK":"restaurant_steakhouse.png",
		"ITALIAN":"restaurant_italian.png", "GERMAN":"gourmet_0star.png", 
		"MOROCCAN": "restaurant_turkish.png", "UKRAINIAN": "restaurant_tapas.png",
		"MEDITERRANEAN": "restaurant_mediterranean.png", 
		"VEGETARIAN":"restaurant_vegetarian.png", "WESTERN": "restaurant.png"
		};

// customer markers	
var LeafIcon = L.Icon.extend({
	iconUrl: "../static/images/leaf-green.png" ,		
	iconSize: new L.Point(38, 95),
	shadowSize: new L.Point(68, 95),
	iconAnchor: new L.Point(22, 94),
	popupAnchor: new L.Point(-3, -76)
});
var FoodIcon = L.Icon.extend({
	iconSize: new L.Point(32, 37),
	shadowUrl: "../static/images/marker-shadow.png",
	shadowSize: new L.Point(41, 41),
	iconAnchor: new L.Point(22, 36),
	popupAnchor: new L.Point(-3, -36)
});	
	
// methods to display routes between two location
function route(x1, y1, x2, y2){
	$("#loading").show();
	var url = "route.json?locations=" + x1 + "," + y1 + "," 
									+ x2 + "," + y2;
	route_layer.clearLayers();
	
	$.getJSON(url, function(data) {
		$("#loading").hide();
		route_layer.addGeoJSON(data);									
	});
	
}

// get all selected categories
function cats_get() {
	var selectedCats = '';
    $("div#catpane :checkbox:checked").each(function() {
    	selectedCats += $(this).val()+",";
    	
    });
    return selectedCats;
}

// return html contents for point popup
function restaurant_details(attributes) {
	
	var output = "";
	output = "<div class='popup_custom'>";
	output += "<img class='popup_thumb' src='../static/images/thumbs/" 
					+ attributes.image +"'/>";
	output += "<div class='popup_main'>";
	output += "<span class='place_name'>" 
					+ attributes.name+ "</span><br />";
	output += "<span class='place_address'><b>Address: </b>" 
					+ attributes.address + "</span><br />";
	if (attributes.phone.length > 1) {
 		output += "<span class='place_phone'><b>Phone: </b>" 
 					+ attributes.phone + "</span><br />";
	}
	if (attributes.website.length > 1) {
		output += "<span class='place_website'><a target='_blank' href='http://" 
					+ attributes.website + "'>" + attributes.website 
					+ "</a></span><br />";	
	}
	if (attributes.email.length > 1) {
		output += "<span class='place_email'><a href='http://" 
					+ attributes.email + "'>" + attributes.email 
					+ "</a></span><br />";	
	}     	 					
	output +=  "<span class='description'>" + attributes.description 
					+ "</span><br />";
	output += "</div></div>";
	return output;
}