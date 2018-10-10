ymaps.ready(init);

var  baseMap = new ymaps.Map('base-map', {
                             center: [55.751574, 37.573856],
                             zoom: 10,
                             controls: []
                             }),
                             objectManager = new ymaps.ObjectManager({
                             clusterize: true,
                             clusterDisableClickZoom: true
                             });


function init () {

    var myMap


    var coords = [
        [55.75, 37.50],
        [55.75, 37.71],
        [55.70, 37.70]
    ];


    for (var i = 0; i < coords.length; i++) {
        myCollection.add(new ymaps.Placemark(coords[i]));
    }

    myMap.geoObjects.add(myCollection);

    // При клике на карту все метки будут удалены.
    myCollection.getMap().events.add('click', function() {
        myCollection.removeAll();
    });
    // myMap.geoObjects.add(objectManager);
}



function renderMap(data){ // evaluate the data and render it on map
    var myCollection = new ymaps.GeoObjectCollection({}, {
        preset: 'islands#redIcon', //все метки красные
        draggable: true // и их можно перемещать
    });



}



$(document).ready(function(){
$("#base-search-form").submit(function(e){
        $.get(recordUrl, $("#base-search-form").serialize(), renderMap);
        e.preventDefault();
        return false;
    });


})