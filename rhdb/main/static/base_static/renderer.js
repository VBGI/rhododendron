function renderAlbum(name){
    $.get(albumUrl + name, function(html){
        $('*[class^="photoalbum-' + name '"]').html(html);
        })
        }

$(document).ready(function () {
    $('*[class^="photoalbum-]').each(function(){
        var albumName = this.className.split('-')[1];
        renderAlbum(albumName, albumUrl)
        })
        })



