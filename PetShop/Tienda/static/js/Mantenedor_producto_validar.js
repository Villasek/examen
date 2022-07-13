$('#col').validate({ 
    "rules": {
        
        "Nombre": {
            required: true,
        },
        "Descripcion": {
            required: true,
            email: true,
        },
        "Precio": {
            required: true,
        },
        "Subscriptor": {
            required: true,
            
        },
        "Descuento por Oferta": {
            required: true,
           
        },
    },
    messages: {
        
        "nombre": {
            required: 'Debe ingresar el nombre del producto',
        },
        "Descripcion": {
            required: 'Debe agregar una descripcion',
        },
        "Precio": {
            required: 'Debe ingresar un precio',
            
        },
        "Subscriptor": {
            required: 'Debe ingresar un descuento',
        },
        "Descuento por Oferta": {
            required: 'Debe ingresar un descuento',
            
        },
    }
});
