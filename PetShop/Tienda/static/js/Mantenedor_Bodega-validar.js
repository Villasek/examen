$('#form_bodega').validate({ 
    "rules": {
        "Cantidad": {
            required: true,
        },
    },
    messages: {
        "Cantidad": {
            required: 'La cantidad es un campo requerido',
        },
    }
});
