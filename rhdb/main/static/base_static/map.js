ymaps.ready(init);


function init () {


var  baseMap = new ymaps.Map('base-map', {
                             center: [43.0, 131.5],
                             zoom: 10,
                             controls: []
                             }),
                             objectManager = new ymaps.ObjectManager({
                             clusterize: true,
                             clusterDisableClickZoom: true
                             });



$(document).ready(function(){
$("#base-search-form").submit(function(e){
        $.get(recordUrl, $("#base-search-form").serialize(), renderMap);
        e.preventDefault();
        return false;
    });


})



function renderMap(data){ // evaluate the data and render it on map

        var objects = [];


        for(j in data){

          var objects[j] = new ymaps.GeoObject({
            geometry: {
                    type: "Point",
                coordinates: [data[j].latitude, data[j].longitude] // координаты точки
                        }
                    });
        }

        }

}





