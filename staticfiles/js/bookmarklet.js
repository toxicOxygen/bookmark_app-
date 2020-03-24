// (function(){
//     var jquery_version = '3.3.1';
//     var site_url = 'http://127.0.0.1:8000/'; 
//     var static_url = site_url + 'static/'; 
//     var min_width = 100;
//     var min_height = 100;

//     function bookmarklet(msg){
//         var css = JQuery('<link>');
//         css.attr({
//             rel: 'stylesheet',
//             type: 'text/css',
//             href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
//         });
//         jQuery('head').append(css);

//         box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a> <h1>Select an image to bookmark:</h1><div class="images"></div></div>';
//         jQuery('body').append(box_html);

//         jQuery('#bookmarklet #close').click(function(){
//             jQuery('#bookmarklet').remove();
//         });

//         jQuery.each(jQuery('img[src$="jpg"]'), function(index, image) {
//             if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height)
//             {
//                 image_url = jQuery(image).attr('src');
//                 jQuery('#bookmarklet .images').append('<a href="#"><img src="'+ image_url +'" /></a>');
//             } 
//         });
//     }

//     if(typeof window.JQuery != 'undefined'){
//         bookmarklet();
//     }else{
//         var conflict = typeof window.$ != 'undefined';
//         var script = document.createElement('script');
//         script.src = '//ajax.googleapis.com/ajax/libs/jquery/' +jquery_version + '/jquery.min.js';
//         document.head.appendChild(script);

//         var attempts = 15;

//         (function(){
//             if(typeof window.JQuery == 'undefined'){
//                 if(--attempts > 0){
//                     window.setTimeout(arguments.callee, 250);
//                 }else{
//                     alert('An error ocurred while loading jQuery');
//                 }
//             }else{
//                 bookmarklet();
//             }
//         })();
//     }

// })();



(function(){
    var min_width = 100;
    var min_height = 100;

    function myBookmarklet(msg=''){
        var bookmark_style = document.createElement('style');
        bookmark_style.innerHTML = `.modal{display:block;position:fixed;z-index:1;left:0;top:0;width:100%;height:100%;overflow:auto;background-color:#000;background-color:rgba(0,0,0,.4)}.modal-content{background-color:#fefefe;margin:15% auto;padding:20px;border:1px solid #888;width:80%}.close{color:#aaa;float:right;font-size:28px;font-weight:700}.close:focus,.close:hover{color:#000;text-decoration:none;cursor:pointer} #bookmarklet .images img{width: 15rem;height: auto;cursor:pointer;padding: 3px;border: solid 1px #EFEFEF;margin:2px;}`;
        
        var box_html  = document.createElement('div');
        box_html.id = 'bookmarklet';
        box_html.classList.add('modal');

        box_html.innerHTML = `<div class="modal-content"><span id="close" class="close">&times;</span> <h1>Select an image to bookmark:</h1><div class="images"></div></div>`;

        document.head.append(bookmark_style);
        document.body.append(box_html);

        var close_btn = document.querySelector('.modal-content #close');
        close_btn.addEventListener('click',e=>{
            box_html.remove();
            bookmark_style.remove();
        });

        // [src$="jpg"]
        site_images = document.querySelectorAll('img[src$="jpg"]');
        var imgs_container = document.querySelector('#bookmarklet .images');
        site_images.forEach(image => {
            if(image.width >= min_width && image.height >= min_height ){
                var i = document.createElement('img');
                i.src = image.src;
                imgs_container.appendChild(i);
                i.addEventListener('click',e=>{
                    //var site_url = `http://127.0.0.1:8000/images/create/?title=hello&url=${i.src}`;
                    var site_url = `https://bookmark-app-kkb.herokuapp.com/images/create/?title=hello&url=${i.src}`;
                    window.open(site_url);
                })
            }
        });
    }

    myBookmarklet();
})();