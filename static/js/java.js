$(document).ready(function(){
    $('.boton-letra').click(modificar_letra);
    actualizar();
    grafica_bares();
    $('.me-gusta').click(me_gusta);
    $('.me-gusta').click(cambiar_boton);
    $('.no-me-gusta').click(me_gusta);
    $('.no-me-gusta').click(cambiar_boton);
});

window.onload = function() {


  actualizar();

}

window.onresize = function() {

  actualizar();
}

function modificar_letra(){
    id=$(this).attr('id');
    numero=parseInt(id.split('b')[1]);
    if(numero==1){
        $('body').css('font-size','18px');
    }
    if(numero==2){
        $('body').css('font-size','24px');
    }
    if(numero==3){
        $('body').css('font-size','12px');
    }
   
}


function actualizar(){
    if($('.easy-map-googlemap').length>0){
        $('.easy-map-googlemap').css('width','100%');
        $('.easy-map-googlemap').height(Math.floor($('.easy-map-googlemap').width()*0.5625));
    }
}

function grafica_bares(){  
     
             $.ajax({
                url: "/rango/reclamar_datos/",
                type: 'get',                        
                success: function(data){
                    Visualiza_datos(data);  
                },
                failure: function(data) { 
                    alert('esto no va');
                }
            });

            function Visualiza_datos(datos) {
               var bares=[];
               var visitas=[];
               
               for(i=0;i<Object.keys(datos).length;i++){
                   bares[i]=datos[i]['nombre'];
                   visitas[i]=parseInt(datos[i]['visitas']);
               }
                $('#contenido').highcharts({
                    chart: {
                        type: 'bar'
                    },
                    title: {
                        text: 'Visitas a Bares'
                    },
                    xAxis: {
                        categories: bares
                    },
                    yAxis: {
                        title: {
                            text: 'visitas'
                        }
                    },
                    series: [{
                        name: 'bares',
                        data: visitas,

                    }],
                });
            };

} 

function me_gusta(){
    ntapa=$(this).attr('data');
    slug=ntapa.replace(/ /g,"-");
    
    if($(this).hasClass('me-gusta')){
         var parametros={
            'opcion':1,
            'slug':slug
         };
    }else{
         var parametros={
            'opcion':2,
            'slug':slug
         };
    }
    votos=$(this).parent('.boton-gusto').siblings('.votos');
    $.ajax({
        url: "/rango/me_gusta/",
        type: 'get',
        data: parametros,
        success: function(data){
            votos.html(data);
        },
        failure: function(data) { 
            alert('esto no va');
        }
    });
    
}

function cambiar_boton(){
    if($(this).hasClass('me-gusta')){
        $(this).removeClass('btn-info').addClass('btn-danger');
        $(this).removeClass('me-gusta').addClass('no-me-gusta');
        $(this).html('anular voto');
    }else{
        $(this).removeClass('btn-danger').addClass('btn-info');
        $(this).removeClass('no-me-gusta').addClass('me-gusta');
        $(this).html('me gusta');
    }
    
}



